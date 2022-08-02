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
        order_df = pd.read_csv(request.FILES['csv'], encoding='shift-jis', dtype={'ShipZipCode': 'object', 'ShipPhoneNumber': 'object'})

        normal = order_df[order_df['PayMethod'] != 'payment_d1'].reset_index(drop=True)
        daibiki = order_df[order_df['PayMethod'] == 'payment_d1'].reset_index(drop=True)

        output_df = pd.DataFrame() # CSV出力用のデータフレーム。処理が終わったものを順番に足していく
        
        if normal.shape[0] == 0:
            pass
        else:
            nekopos_df = normal[normal['ShipMethod'] == 'postage2'].reset_index(drop=True)
            hatsubarai_df = normal[normal['ShipMethod'] != 'postage2'].reset_index(drop=True)

            if nekopos_df.shape[0] == 0:
                pass
        
            else:
                output_nekopose_df = yahoo_okurijyou.create_import_data(
                    order_df=nekopos_df, 
                    output_df_shape=[nekopos_df.shape[0], template.shape[1]],
                    ship_type='ネコポス'
                )
                output_df = pd.concat([output_df, output_nekopose_df], axis=0)

            if hatsubarai_df.shape[0] == 0:
                pass
            else:
                output_hatsubarai_df = yahoo_okurijyou.create_import_data(
                    order_df=hatsubarai_df, 
                    output_df_shape=[hatsubarai_df.shape[0], template.shape[1]],
                    ship_type='発払い'
                )
        
                # 日付が指定されていない注文は最短日に設定する
                output_hatsubarai_df[5] = output_hatsubarai_df[5].fillna('最短日')
                output_df = pd.concat([output_df, output_hatsubarai_df], axis=0)

        if daibiki.shape[0] == 0:
            pass

        else:
            output_daibiki = yahoo_okurijyou.create_import_data(order_df=daibiki, 
                                                            output_df_shape=[daibiki.shape[0], template.shape[1]],
                                                            ship_type='代引き')

            # 日付が指定されていない注文は最短日に設定する      
            output_daibiki[5] = output_daibiki[5].fillna('最短日')                                                 
            output_df = pd.concat([output_df, output_daibiki], axis=0)

        output_df[1] = output_df[1].astype(int)

        response = HttpResponse(
                content_type='text/csv',
            )
        response['Content-Disposition'] = 'attachment; filename="okurijyou.csv"'

        output_df.to_csv(path_or_buf=response, index=False)
        return response
    return render(request, 'okurijyou/create_csv.html')