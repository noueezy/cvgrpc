# cvgrpc
Jetson Nanoカメラサーバ

## Description
- Jetson Nanoに接続したRaspberry Piカメラで画像を撮影
- 撮影した画像データをメモリ上でJpeg圧縮（OpenCV使用）
- 圧縮した画像データを配信するgrpcサーバ
- 圧縮した画像データを取得・デコードするクライアント側のサンプルコード

