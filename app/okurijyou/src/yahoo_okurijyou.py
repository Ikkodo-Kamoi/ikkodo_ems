import os

import datetime as dt
import math

import pandas as pd
import numpy as np

from django.conf import settings

def ship_request_time(order_df):
    ship_request_time = []

    for i in order_df['ShipRequestTime']:
        if type(i) == str:
            ship_request_time.append(settings.DELIVERY_TIME[i])
        else:
            ship_request_time.append(np.nan)
    return ship_request_time

def ship_address(order_df):
    ship_address = []

    for i,j,k in zip(order_df['ShipPrefecture'], order_df['ShipCity'], order_df['ShipAddress1']):
        ship_address.append(i + j + k)
    return ship_address

def create_import_data(order_df, output_df_shape, ship_type):
    data = np.full(output_df_shape, np.nan)
    output_df = pd.DataFrame(data=data)

    if ship_type == '発払い':
        output_df.iloc[:, [1]] = 0
        output_df.iloc[:, [27]] = '精密機械'
        output_df.iloc[:, [30]] = '精密機器'

    elif ship_type == 'ネコポス':
        output_df.iloc[:, [1]] = 7
        output_df.iloc[:, [27]] = 'バンド'

    elif ship_type == '代引き':
        output_df.iloc[:, [1]] = 2
        output_df.iloc[:, [33]] = order_df['Total']
        output_df.iloc[:, [27]] = '精密機械'
        output_df.iloc[:, [30]] = '精密機器'

    output_df.iloc[:, [4]] = dt.date.today().strftime('%Y/%m/%d')
    output_df.iloc[:, [5]] = order_df['ShipRequestDate']
    output_df.iloc[:, [6]] = ship_request_time(order_df)
    output_df.iloc[:, [8]] = order_df['ShipPhoneNumber']
    output_df.iloc[:, [10]] = order_df['ShipZipCode']
    output_df.iloc[:, [11]] = ship_address(order_df)
    output_df.iloc[:, [12]] = order_df['ShipAddress2']
    output_df.iloc[:, [15]] = order_df['ShipName']
    output_df.iloc[:, [19]] = os.environ.get('DELIV_ORNER_PHONENUMBER')
    output_df.iloc[:, [21]] = os.environ.get('DELIV_ORNER_ZIPCODE')
    output_df.iloc[:, [22]] = os.environ.get('DELIV_ORNER_ADDRESS')
    output_df.iloc[:, [24]] = os.environ.get('DELIV_ORNER_NAME')
    output_df.iloc[:, [31]] = '水濡厳禁'
    output_df.iloc[:, [32]] = '転送不可'
    output_df.iloc[:, [39]] = os.environ.get('DELIV_ORNER_PAYCODE')

    return output_df