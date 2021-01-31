# Censusarea

このプロジェクトでは、H27国勢調査小地域のデータから行政界ベクトルタイルを生成することができます。

## 概要

[総務省の統計GISデータ](https://www.e-stat.go.jp/gis/statmap-search?page=1&type=2&aggregateUnitForBoundary=A&toukeiCode=00200521&toukeiYear=2015&serveyId=A002005212015&coordsys=1&format=shape)のシェープファイルをmbtilesに変換します。小地域ポリゴンを結合して県および市区町村ポリゴンデータも生成します。
具体的には、以下のように処理します。
+ 47都道府県分のシェープファイルをダウンロード
+ spatialite_toolを使ってシェープファイルをspatialiteデータベースにインポート
+ spatialite上で県ポリゴン、市区町村ポリゴンを生成
+ spatialite_toolを使ってシェープファイルを出力
+ GeoJSON形式に変換
+ tippecanoeを使ってmbtilesに変換

## 利用方法
mbtilesの作成は以下のように行います。
```
$ git clone https://github.com/geolonia/censusarea  
$ cd censusarea  
$ ./gencensusarea.sh
```

## 動作条件および注意点
動作には以下のプロダクトが必要です。
+ spatialite-tools（バージョン5を推奨）
+ python3.6以上
+ 以下のpython拡張モジュール（pipにてインストール）
  + pyyaml
  + fiona
  + shapely

spatialite-toolsのバージョン4以前では、日本語が文字化けする可能性があります。リポジトリにパッケージがない場合はソースからのビルドとなります。以下を参考にしてください。  
https://www.gaia-gis.it/fossil/spatialite-tools/index  
なお、MacOS（Big Sur）の場合は、homebrewを使えばspatialite-tools5がインストールされます。


### 変換結果表示URL

[https://labo.takamoto.biz/censusarea](https://labo.takamoto.biz/censusarea)
