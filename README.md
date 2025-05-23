# plot\_map

このプロジェクトは、CSVファイルに記載された日本国内の施設情報を地図上にプロットする Python スクリプトです。

## 特徴

* CSVファイルから店舗情報（名称、住所、評価、電話番号など）を読み込み
* 日本語住所を緯度・経度に変換（ジオコーディング）
* Foliumを用いてHTML形式の地図に出力

## 使用方法

### 前提条件

* Python 3.7 以降
* 以下のPythonライブラリのインストールが必要です：

  ```bash
  pip install pandas folium jageocoder tqdm
  ```

### jageocoderの辞書インストール

`jageocoder`を使用するには、住所辞書データのインストールが必要です。以下のコマンドを実行してください：

```bash
jageocoder download-dictionary https://www.info-proto.com/static/jageocoder/latest/jukyo_all_v21.zip
jageocoder install-dictionary jukyo_all_v21.zip

```

インストール後、自動的にデフォルトの辞書ディレクトリが設定され、住所を緯度経度に変換できるようになります。

### 実行コマンド

```bash
python scripts/plot_map.py --input ./input/input.csv --output ./output/output.html --zoom 16
```

* `--input`：CSVファイルのパス
* `--output`：生成される地図HTMLファイルの保存先
* `--zoom`：（オプション）地図の初期ズームレベル（デフォルト: 15）

## CSVフォーマット例

CSVファイルは以下のような形式を想定しています：

```csv
name,rating,user_ratings_total,phone,address,url
店舗名,4.8,123,03-XXXX-XXXX,日本、〒XXX-XXXX 東京都○○区○○X-X-XX,https://...
```

## 出力

* 指定された[HTMLファイル](./output/sample.html)に、各店舗の位置を示すインタラクティブなマップを出力します。
* マーカーをクリックすると、店舗名・評価・レビュー数・電話番号がポップアップ表示されます。

ライセンス

このプロジェクトは [MITライセンス](.LICENSE) の下で公開されています。
