#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
プログラム概要:
このスクリプトは、Googleマップから取得したCSVファイルを読み取り、
各スポットの住所をもとに位置情報（緯度・経度）を取得し、
foliumを使って地図上にマーカーとして可視化します。
出力はHTML形式の地図ファイルです。

使用方法:
python plot_map.py --input 店舗情報.csv --output map.html --zoom 14

コマンドライン引数:
--input  : 入力CSVファイル（UTF-8、住所カラム 'address' を含む）
--output : 出力HTMLファイル名
--zoom   : 地図の初期ズームレベル（オプション、省略時は13）
"""

import pandas as pd
import folium
import jageocoder
import argparse
import re
from folium import IFrame

# 引数の設定
parser = argparse.ArgumentParser(description='住所付きCSVから地図を作成')
parser.add_argument('--input', required=True, help='入力CSVファイル')
parser.add_argument('--output', required=True, help='出力HTMLファイル名')
parser.add_argument('--zoom', type=int, default=13, help='初期ズームレベル（デフォルト: 13）')
args = parser.parse_args()

# jageocoderの初期化
jageocoder.init()

# CSVファイルの読み込み
df = pd.read_csv(args.input)

# 緯度・経度の取得
latitudes = []
longitudes = []

pattern = r"〒\d{3}-\d{4}\s*(.*)"
for address in df['address']:
    print(f'address: {address}')
    match = re.search(pattern, address)
    if match:
        address = match.group(1)
    
    result = jageocoder.search(address)
    print(f'result: {result}')
    if result['candidates']:
        candidate = result['candidates'][0]
        latitudes.append(candidate['y'])
        longitudes.append(candidate['x'])
    else:
        latitudes.append(None)
        longitudes.append(None)

df['latitude'] = latitudes
df['longitude'] = longitudes

# 地図の中心を設定（最初に有効な地点）
center_lat = df['latitude'].dropna().iloc[0]
center_lon = df['longitude'].dropna().iloc[0]
m = folium.Map(location=[center_lat, center_lon], zoom_start=args.zoom)

# マーカーを地図に追加
for _, row in df.iterrows():
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        # popup_text = f"""
        # {row['name']}<br>
        # 評価: {row['rating']} ({row['user_ratings_total']}件)<br>
        # 電話: {row['phone']}<br>
        # 住所: {row['address']}<br>
        # <a href="{row['url']}" target="_blank">Googleマップで見る</a>
        # """
        # popup = folium.Popup(popup_text, max_width=500, min_width=300, max_height=300, parse_html=True)

        # folium.Marker(
        #     location=[row['latitude'], row['longitude']],
        #     popup=popup,
        #     icon=folium.Icon(color='blue', icon='info-sign')
        # ).add_to(m)        
        popup_text = f"""{row['name']} <br>
        評価: {row['rating']} ({row['user_ratings_total']}件)<br> 
        電話: {row['phone']}<br>
        住所: {row['address']}<br>
        """
        iframe = IFrame(popup_text, width=300, height=200)
        popup = folium.Popup(iframe, max_width=500, min_width=300, max_height=300)
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

# HTMLファイルとして保存
m.save(args.output)
