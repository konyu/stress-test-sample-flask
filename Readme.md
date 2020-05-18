負荷テストをツールの使い方をテストするためのシンプルなログイン機能を持つFlask製のWebアプリケーションを構築し、
Zappaを用いてAWSにデプロイする。

このデプロイしたWebアプリをサンプルとして負荷テストを実行する手順を説明する

本資料で利用する負荷テストツール

- [Appache bench](https://httpd.apache.org/docs/2.4/programs/ab.html) 
- [Artillery](https://artillery.io/)
- serverless-artilley`AWS環境でLambdaを用いて大規模な負荷テストを実行できる`Artilleryのサーバレス版


実装機能
- [x] 未ログインでGETでアクセス可能なページ(ログイン画面)
- [x] Cookieを使ったログイン必須のGETでアクセス可能なページ(TOP画面)
- [x] ログイン機能(フォームから)
- [x] フォーム送信機能
- [ ] JWTを利用したログイン
- [ ] JWTでのログイン必須なページ
- [ ] JSONのPOSTするページ

# Flaskセットアップ

## Pythonバージョン
3.7での動作確認を確認している
## viurtualenvを用いたFlask環境セットアップ

### virturlenv環境を作成
viurtualenvの作成するディレクトリ名を`venv`とし、viurtualenv環境を作成

```sh
python -m venv venv
```

### virturlenv環境に入る

```shell script
source venv/bin/activate
```

### virturlenv環境から出る

```shell script
deactivate
```

### Pythonライブラリのインストール
venv環境に入ってから、requirements.txtに記載されたライブラリをインストール

```shell script
pip install -r requirements.txt

```

### virturlenv環境の削除

```shell script
python -m venv --clear venv
```

----
## Zappaを使ってAWSにデプロイ
[Zappa](https://github.com/Miserlou/Zappa) を用いてAWSにFlaskを展開する。
ZappaはAmazon API GatewayとAWS Lambdaで構成されている。

Zappaで起動したアプリは一つのAPI Gatewayで受けてすべてFlaskが動いているLambdaに転送するという極めてシンプルな構成になる。

以下にZappaの初期化からAWS CloudFormationを使ったデプロイまで記載するが、下記のBlog記事を参考にするとZappaの入力項目など一読しておくと迷わないだろう
[Zappaを使ってFlask appをAWS Lambda と API Gatewayにデプロイしてみた \| Developers.IO](https://dev.classmethod.jp/articles/deploy-flask-app-aws-lambda-api-gateway-ja/)

### 前提条件
AWS CLIのインストールと実行ユーザの設定を`aws configure`で設定しておく必要がある。
設定ではではアドミン権限のあるIAMユーザまたは、API GatewayやAWS CloudFormationなど適切な権限を付与したユーザを用意する。

初期化

初期化の際にaws cliのどのプロファイルを利用するか、どのリージョンを使うかなど回答していき、zappa_settings.jsonファイルが作成される。

```shell script
zappa init 
```


(dev環境へ)デプロイ
```shell script
zappa deploy dev
```

再デプロイ
```shell script
zappa update dev
```

zappaの削除の仕方、このコマンドでAWS CloudFormationでスタックを削除する

```shell script
zappa undeploy dev
```

-----

# 負荷テスト方法
以下 各ツールで負荷テストをする方法を記載する(随時更新予定)

# Curl
## ログインが必要なHTTPアクセスの場合

事前にブラウザでログインしてみてDevtoolsでリクエストヘッダを確認し、Cookieの箇所で送信しているセッションの項目.sessionをパラメタとして付与する。

CurlのCookieをつけるパラメタは  -b オプションを付けてる
  
### GETの例

```  
curl "http://servert_url:port/top" -b "session=SESSION_DATA"
```
 
### FormデータをPOSTする例
FormのデータをPostする場合は-F オプションを付ける。大抵のウェブサービスの処理でPost後に別の画面にリダイレクトするので-Lオプションを付けてあげると、Post->Redirect->GetとCurlが動いてくれる
  
```  
curl -L "http://servert_url:port/put" -d -F 'value="FOOBAR"' -b "session=SESSION_DATA"  
```
# Apache Benchを用いた負荷テスト
apache benchは各自インストールすること。mac osの場合はhomebrewでインストールするのが簡単

## ログインが必要なHTTPアクセスの場合

## GETの例
-Cオプションでクッキーを添付する
```
ab -n 10 -c 2 -C "session=SESSION_DATA" http://servert_url:port/top
```

## FormデータをPOSTする例

Postdata.txtにフォームで送るデータを対応するように フォームの要素名=値の組を送る複数ある場合は&でつないでいく
value=FooBar&value2=HogeHoge

```
» ab -c 2 -n 10 -p postdata.txt -T "application/x-www-form-urlencoded"  -C "session=SESSION_DATA" http://servert_url:port/put
```

## その他Apache benchの注意点
- サーバでエラーが発生してもエラー画面など何らかのレスポンスがある場合はComplete requestsとして扱われFailed Requestsにならないので必ずブラウザで動作確認する必要がある

# serverless-artilleryを用いた負荷テスト
artilleryはnode製の負荷テストツール。これをAWSのサーバレス環境利用するのがserverless-artilleryである。

## インストール方法
インストールにはnodeが必要、ここではmac osにnpmを利用したインストール方法を記載する

### nodeの動作確認バージョン
node: v13.7.0
npm: 6.13.7

### serverless-artilleryのインストール

serverlessとserverless-artilleryをインストールする

```shell script
npm install -g serverlss serverless-artillery
```

## severless-artilleryのセットアップ

### テストファイル雛形作成作成

下記コマンドでテストシナリオの雛形script.ymlが作成される。

サンプルとしてartillery-testディレクトリ下にサンプルのテストコード`script.sample.yml`がある
targetの項目にある`TARGET_URL_PLEASE_CHANGE`を適宜変更するして利用すること

```shell script
slsart script
```

## artilleryで負荷テストをローカル実行する
artilleryをインストールする

```shell script
npm install -g artillery
```

ローカル実行
```shell script
artillery run artillery-test/script.sample.yml
```

## AWSにデプロイ
下記コマンドを実行するとAWS CloudFormationでテストサービスがデプロイされる。
--stageオプションでステージを指定する(serverless frameworkの概念なのでわかりにくいがAWSで展開しているカタマリのこと)

注意: デプロイしただけではテストは実行されない

```shell script
slsart deploy --stage test1
```

## AWS上でテスト実行
 
実行したカレントディレクトリにあるテストシナリオファイルscript.ymlを使ってAWS上でテストを実行する

```shell script
slsart invoke --stage test1
```

独自のテストシナリをファイルを利用して、デフォルトのテストシナリオファイルscript.ymlを使わない場合

```shell script
slsart invoke --stage test1 -p artillery-test/other_script.yml
```

## AWSから削除

```shell script
slsart remove --stage test1
```