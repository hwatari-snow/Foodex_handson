#!/usr/bin/env python3
"""
お惣菜POSデータ生成スクリプト
季節性を考慮した売上データを生成します
"""

import csv
import random
from datetime import date, timedelta
import math

# 商品マスタを読み込み
products = []
with open('/Users/hirokiwatari/repo/Foodex/csv/product_master.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        products.append(row)

# 商品ごとの基本設定（価格と基準販売数）
product_config = {
    # 唐揚げ・揚げ物（通年人気）
    '4901001000011': {'price': 398, 'base_qty': 25, 'seasonality': 'all_year'},
    '4901001000028': {'price': 498, 'base_qty': 15, 'seasonality': 'all_year'},
    '4901001000035': {'price': 358, 'base_qty': 18, 'seasonality': 'all_year'},
    '4901001000042': {'price': 428, 'base_qty': 12, 'seasonality': 'all_year'},
    '4901001000059': {'price': 348, 'base_qty': 14, 'seasonality': 'all_year'},
    # とんかつ・肉惣菜
    '4901002000018': {'price': 498, 'base_qty': 20, 'seasonality': 'all_year'},
    '4901002000025': {'price': 598, 'base_qty': 12, 'seasonality': 'all_year'},
    '4901002000032': {'price': 458, 'base_qty': 10, 'seasonality': 'winter'},
    '4901002000049': {'price': 298, 'base_qty': 22, 'seasonality': 'all_year'},
    '4901002000056': {'price': 298, 'base_qty': 18, 'seasonality': 'all_year'},
    '4901002000063': {'price': 248, 'base_qty': 15, 'seasonality': 'all_year'},
    # 魚惣菜
    '4901003000015': {'price': 398, 'base_qty': 15, 'seasonality': 'all_year'},
    '4901003000022': {'price': 358, 'base_qty': 18, 'seasonality': 'all_year'},
    '4901003000039': {'price': 298, 'base_qty': 16, 'seasonality': 'all_year'},
    '4901003000046': {'price': 458, 'base_qty': 14, 'seasonality': 'all_year'},
    '4901003000053': {'price': 498, 'base_qty': 12, 'seasonality': 'winter'},  # 牡蠣は冬
    '4901003000060': {'price': 348, 'base_qty': 10, 'seasonality': 'all_year'},
    '4901003000077': {'price': 328, 'base_qty': 12, 'seasonality': 'all_year'},
    # サラダ（夏に人気）
    '4901004000012': {'price': 248, 'base_qty': 20, 'seasonality': 'summer'},
    '4901004000029': {'price': 228, 'base_qty': 15, 'seasonality': 'summer'},
    '4901004000036': {'price': 198, 'base_qty': 12, 'seasonality': 'all_year'},
    '4901004000043': {'price': 198, 'base_qty': 18, 'seasonality': 'summer'},
    '4901004000050': {'price': 218, 'base_qty': 14, 'seasonality': 'summer'},
    '4901004000067': {'price': 258, 'base_qty': 10, 'seasonality': 'summer'},
    # 和惣菜（通年）
    '4901005000019': {'price': 198, 'base_qty': 18, 'seasonality': 'all_year'},
    '4901005000026': {'price': 178, 'base_qty': 15, 'seasonality': 'all_year'},
    '4901005000033': {'price': 178, 'base_qty': 20, 'seasonality': 'all_year'},
    '4901005000040': {'price': 328, 'base_qty': 14, 'seasonality': 'winter'},
    '4901005000057': {'price': 298, 'base_qty': 12, 'seasonality': 'winter'},
    '4901005000064': {'price': 168, 'base_qty': 10, 'seasonality': 'all_year'},
    '4901005000071': {'price': 248, 'base_qty': 22, 'seasonality': 'all_year'},
    # 中華惣菜
    '4901006000016': {'price': 348, 'base_qty': 18, 'seasonality': 'all_year'},
    '4901006000023': {'price': 498, 'base_qty': 12, 'seasonality': 'all_year'},
    '4901006000030': {'price': 428, 'base_qty': 14, 'seasonality': 'all_year'},
    '4901006000047': {'price': 398, 'base_qty': 12, 'seasonality': 'all_year'},
    '4901006000054': {'price': 378, 'base_qty': 15, 'seasonality': 'all_year'},
    '4901006000061': {'price': 378, 'base_qty': 14, 'seasonality': 'all_year'},
    '4901006000078': {'price': 298, 'base_qty': 16, 'seasonality': 'all_year'},
    '4901006000085': {'price': 298, 'base_qty': 25, 'seasonality': 'all_year'},
    # 弁当
    '4901007000013': {'price': 398, 'base_qty': 30, 'seasonality': 'all_year'},
    '4901007000020': {'price': 498, 'base_qty': 25, 'seasonality': 'all_year'},
    '4901007000037': {'price': 498, 'base_qty': 28, 'seasonality': 'all_year'},
    '4901007000044': {'price': 548, 'base_qty': 22, 'seasonality': 'all_year'},
    '4901007000051': {'price': 598, 'base_qty': 20, 'seasonality': 'all_year'},
    '4901007000068': {'price': 598, 'base_qty': 18, 'seasonality': 'all_year'},
    '4901007000075': {'price': 498, 'base_qty': 24, 'seasonality': 'all_year'},
    # おにぎり（通年高回転）
    '4901008000010': {'price': 138, 'base_qty': 50, 'seasonality': 'all_year'},
    '4901008000027': {'price': 128, 'base_qty': 40, 'seasonality': 'all_year'},
    '4901008000034': {'price': 148, 'base_qty': 55, 'seasonality': 'all_year'},
    '4901008000041': {'price': 158, 'base_qty': 45, 'seasonality': 'all_year'},
    '4901008000058': {'price': 128, 'base_qty': 35, 'seasonality': 'all_year'},
    '4901008000065': {'price': 178, 'base_qty': 15, 'seasonality': 'spring'},  # 春のお祝い
    # 寿司
    '4901009000017': {'price': 198, 'base_qty': 20, 'seasonality': 'all_year'},
    '4901009000024': {'price': 398, 'base_qty': 18, 'seasonality': 'all_year'},
    '4901009000031': {'price': 698, 'base_qty': 12, 'seasonality': 'all_year'},
    '4901009000048': {'price': 598, 'base_qty': 15, 'seasonality': 'all_year'},
    '4901009000055': {'price': 698, 'base_qty': 14, 'seasonality': 'all_year'},
    # 季節商品
    '4902001000014': {'price': 798, 'base_qty': 0, 'seasonality': 'setsubun'},  # 恵方巻き（節分）
    '4902001000021': {'price': 298, 'base_qty': 0, 'seasonality': 'sakura'},    # 桜餅（春）
    '4902001000038': {'price': 298, 'base_qty': 0, 'seasonality': 'kodomo'},    # 柏餅（こどもの日）
    '4902001000045': {'price': 498, 'base_qty': 0, 'seasonality': 'summer_noodle'},  # 冷やし中華
    '4902001000052': {'price': 548, 'base_qty': 0, 'seasonality': 'summer_noodle'},  # 冷製パスタ
    '4902001000069': {'price': 398, 'base_qty': 0, 'seasonality': 'summer_noodle'},  # 素麺
    '4902001000076': {'price': 1280, 'base_qty': 0, 'seasonality': 'doyo'},     # うなぎ（土用の丑）
    '4902001000083': {'price': 258, 'base_qty': 0, 'seasonality': 'doyo'},      # 土用餅
    '4902001000090': {'price': 298, 'base_qty': 0, 'seasonality': 'ohigan'},    # おはぎ（お彼岸）
    '4902001000106': {'price': 498, 'base_qty': 0, 'seasonality': 'autumn'},    # 栗ご飯
    '4902001000113': {'price': 298, 'base_qty': 0, 'seasonality': 'tsukimi'},   # 月見団子
    '4902001000120': {'price': 398, 'base_qty': 0, 'seasonality': 'sanma'},     # さんま塩焼き
    '4902001000137': {'price': 698, 'base_qty': 0, 'seasonality': 'matsutake'}, # 松茸ご飯
    '4902001000144': {'price': 498, 'base_qty': 0, 'seasonality': 'oden'},      # おでん
    '4902001000151': {'price': 398, 'base_qty': 0, 'seasonality': 'yearend'},   # 年越しそば
    '4902001000168': {'price': 2980, 'base_qty': 0, 'seasonality': 'osechi'},   # おせち
    '4902001000175': {'price': 498, 'base_qty': 0, 'seasonality': 'newyear'},   # お雑煮
    '4902001000182': {'price': 298, 'base_qty': 0, 'seasonality': 'nanakusa'},  # 七草粥
    # 居酒屋惣菜
    '4903001000011': {'price': 398, 'base_qty': 12, 'seasonality': 'winter'},
    '4903001000028': {'price': 298, 'base_qty': 20, 'seasonality': 'all_year'},
    '4903001000035': {'price': 298, 'base_qty': 22, 'seasonality': 'all_year'},
    '4903001000042': {'price': 198, 'base_qty': 25, 'seasonality': 'summer'},   # 枝豆は夏
    '4903001000059': {'price': 298, 'base_qty': 8, 'seasonality': 'all_year'},
    '4903001000066': {'price': 198, 'base_qty': 15, 'seasonality': 'summer'},   # 冷奴は夏
    # 洋食
    '4904001000018': {'price': 458, 'base_qty': 18, 'seasonality': 'all_year'},
    '4904001000025': {'price': 428, 'base_qty': 16, 'seasonality': 'all_year'},
    '4904001000032': {'price': 498, 'base_qty': 14, 'seasonality': 'all_year'},
    '4904001000049': {'price': 548, 'base_qty': 20, 'seasonality': 'all_year'},
    '4904001000056': {'price': 498, 'base_qty': 12, 'seasonality': 'winter'},
    '4904001000063': {'price': 498, 'base_qty': 14, 'seasonality': 'winter'},
    '4904001000070': {'price': 498, 'base_qty': 22, 'seasonality': 'all_year'},
    # カレー
    '4905001000015': {'price': 498, 'base_qty': 20, 'seasonality': 'all_year'},
    '4905001000022': {'price': 498, 'base_qty': 18, 'seasonality': 'all_year'},
    '4905001000039': {'price': 458, 'base_qty': 15, 'seasonality': 'all_year'},
    '4905001000046': {'price': 498, 'base_qty': 16, 'seasonality': 'all_year'},
    '4905001000053': {'price': 548, 'base_qty': 14, 'seasonality': 'all_year'},
    '4905001000060': {'price': 548, 'base_qty': 10, 'seasonality': 'summer'},   # グリーンカレーは夏
}

def get_seasonal_multiplier(jan, sale_date):
    """季節性に基づく販売数の乗数を返す"""
    config = product_config.get(jan, {'seasonality': 'all_year'})
    seasonality = config['seasonality']
    month = sale_date.month
    day = sale_date.day
    
    if seasonality == 'all_year':
        # 週末は1.3倍、平日は1.0
        weekday_mult = 1.3 if sale_date.weekday() >= 5 else 1.0
        return weekday_mult
    
    elif seasonality == 'summer':
        # 6-8月がピーク
        if month in [6, 7, 8]:
            return 2.5
        elif month in [5, 9]:
            return 1.5
        elif month in [4, 10]:
            return 0.8
        else:
            return 0.3
    
    elif seasonality == 'winter':
        # 11-2月がピーク
        if month in [12, 1, 2]:
            return 2.5
        elif month in [11, 3]:
            return 1.5
        elif month in [10, 4]:
            return 0.8
        else:
            return 0.3
    
    elif seasonality == 'spring':
        # 3-4月
        if month in [3, 4]:
            return 3.0
        else:
            return 0.1
    
    elif seasonality == 'setsubun':
        # 節分（2月3日前後）
        if month == 2 and 1 <= day <= 3:
            return 50.0
        elif month == 1 and day >= 25:
            return 5.0
        else:
            return 0.0
    
    elif seasonality == 'sakura':
        # 桜餅（3月-4月上旬）
        if month == 3 or (month == 4 and day <= 10):
            return 15.0
        elif month == 2 and day >= 20:
            return 3.0
        else:
            return 0.0
    
    elif seasonality == 'kodomo':
        # 柏餅（5月5日前後）
        if month == 5 and 1 <= day <= 5:
            return 30.0
        elif month == 4 and day >= 25:
            return 5.0
        else:
            return 0.0
    
    elif seasonality == 'summer_noodle':
        # 冷やし中華・冷製パスタ・素麺（6-8月）
        if month in [7, 8]:
            return 20.0
        elif month == 6:
            return 10.0
        elif month in [5, 9]:
            return 3.0
        else:
            return 0.0
    
    elif seasonality == 'doyo':
        # 土用の丑（7月下旬-8月上旬）
        if month == 7 and day >= 20:
            return 30.0
        elif month == 8 and day <= 5:
            return 20.0
        else:
            return 0.0
    
    elif seasonality == 'ohigan':
        # お彼岸（3月・9月の中旬）
        if (month == 3 and 17 <= day <= 23) or (month == 9 and 20 <= day <= 26):
            return 30.0
        elif (month == 3 and 10 <= day <= 16) or (month == 9 and 15 <= day <= 19):
            return 5.0
        else:
            return 0.0
    
    elif seasonality == 'autumn':
        # 栗ご飯（9-10月）
        if month in [9, 10]:
            return 15.0
        elif month == 11:
            return 5.0
        else:
            return 0.0
    
    elif seasonality == 'tsukimi':
        # 月見団子（9月中旬）
        if month == 9 and 10 <= day <= 20:
            return 25.0
        else:
            return 0.0
    
    elif seasonality == 'sanma':
        # さんま（9-10月）
        if month in [9, 10]:
            return 20.0
        elif month == 11:
            return 5.0
        else:
            return 0.0
    
    elif seasonality == 'matsutake':
        # 松茸（9-10月）
        if month in [9, 10]:
            return 10.0
        else:
            return 0.0
    
    elif seasonality == 'oden':
        # おでん（10月-3月）
        if month in [11, 12, 1, 2]:
            return 18.0
        elif month in [10, 3]:
            return 8.0
        else:
            return 0.0
    
    elif seasonality == 'yearend':
        # 年越しそば（12月下旬）
        if month == 12 and day >= 28:
            return 50.0
        elif month == 12 and day >= 20:
            return 10.0
        else:
            return 0.0
    
    elif seasonality == 'osechi':
        # おせち（12月下旬）
        if month == 12 and day >= 25:
            return 30.0
        elif month == 12 and day >= 15:
            return 5.0
        else:
            return 0.0
    
    elif seasonality == 'newyear':
        # お雑煮（1月1日-7日）
        if month == 1 and 1 <= day <= 7:
            return 40.0
        elif month == 12 and day >= 28:
            return 10.0
        else:
            return 0.0
    
    elif seasonality == 'nanakusa':
        # 七草粥（1月7日）
        if month == 1 and 5 <= day <= 7:
            return 50.0
        else:
            return 0.0
    
    return 1.0

# POSデータ生成
start_date = date(2022, 1, 1)
end_date = date(2026, 2, 24)

pos_data = []

for product in products:
    jan = product['JANCODE']
    name = product['PRODUCT_NAME']
    maker = product['MAKER_NAME']
    
    config = product_config.get(jan, {'price': 398, 'base_qty': 10})
    price = config['price']
    base_qty = config['base_qty']
    
    current_date = start_date
    while current_date <= end_date:
        multiplier = get_seasonal_multiplier(jan, current_date)
        
        if multiplier > 0:
            # ランダム変動を加える（±30%）
            qty = int(base_qty * multiplier * random.uniform(0.7, 1.3))
            qty = max(0, qty)
            
            if qty > 0 or base_qty == 0:  # 季節商品は0でも記録
                amount = qty * price
                pos_data.append({
                    'SALE_DATE': current_date.isoformat(),
                    'JANCODE': jan,
                    'PRODUCT_NAME': name,
                    'MAKER_NAME': maker,
                    'SALES_QTY': qty,
                    'UNIT_PRICE': price,
                    'SALES_AMOUNT': amount
                })
        
        current_date += timedelta(days=1)

# CSVに書き出し
with open('/Users/hirokiwatari/repo/Foodex/csv/pos_data.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['SALE_DATE', 'JANCODE', 'PRODUCT_NAME', 'MAKER_NAME', 'SALES_QTY', 'UNIT_PRICE', 'SALES_AMOUNT']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(pos_data)

print(f"Generated {len(pos_data)} POS records")
