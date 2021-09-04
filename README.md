# chibawest-gamecenter-bot

## 概要

botの中の人です。  
[main.py](main.py)の `ChibawestGamecenterBot` が本体。

discordのトークンはGCPの[Secret Manager](https://cloud.google.com/secret-manager/docs)に保存してます。  
アプリケーションはgkeで動いてて、その中であればトークンをダウンロードできる仕組み。

アプリ:  
<https://github.com/mytk0u0/chibawest-gamecenter-apps>

インフラまわり:  
<https://github.com/mytk0u0/chibawest-gamecenter-infra>  
<https://github.com/mytk0u0/chibawest-gamecenter-manifest>

## 動作確認

以下をやればOK。

```bash
poetry run start
```

## デプロイ

`upload.sh` でDocker Hubにアップロード。あとはdiscord botのインスタンスを再起動すればOK。
