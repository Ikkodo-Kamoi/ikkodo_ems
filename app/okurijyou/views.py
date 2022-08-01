import os

import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from .src import yahoo_okurijyou

# Create your views here.
def create_csv(request):
    if request.method == 'POST':
        template = pd.read_csv(os.path.join(settings.BASE_DIR, 'config/data/okurijyou/template.csv'))
        order_df = pd.read_csv(request.FILES['csv'], encoding='shift-jis', dtype={'ShipPhoneNumber': 'object'})

        normal = order_df[order_df['PayMethod'] != 'payment_d1'].reset_index(drop=True)
        daibiki = order_df[order_df['PayMethod'] == 'payment_d1'].reset_index(drop=True)

        if normal.shape[0] == 0:
            pass
        else:
            output_normal = yahoo_okurijyou.create_import_data(order_df=normal, 
                                                            output_df_shape=[normal.shape[0], template.shape[1]],
                                                            ship_type='発払い')

        if daibiki.shape[0] == 0:
            pass

        else:
            output_daibiki = yahoo_okurijyou.create_import_data(order_df=daibiki, 
                                                            output_df_shape=[daibiki.shape[0], template.shape[1]],
                                                            ship_type='代引き')

        try:
            okurijyou = pd.concat([output_normal, output_daibiki], axis=0)

        except:
            okurijyou = output_normal

        okurijyou[1] = okurijyou[1].astype(int)

        response = HttpResponse(
                content_type='text/csv',
            )
        response['Content-Disposition'] = 'attachment; filename="okurijyou.csv"'

        okurijyou.to_csv(path_or_buf=response, index=False)
        return response
    return render(request, 'okurijyou/create_csv.html')