負荷テストをツールの使い方をテストするためのシンプルなログイン機能を持つFlask製のWebアプリケーション

実装機能
- [x] 未ログインでGETでアクセス可能なページ(ログイン画面)
- [x] Cookieを使ったログイン必須のGETでアクセス可能なページ(TOP画面)
- [x] ログイン機能(フォームから)
- [x] フォーム送信機能
- [ ] JWTを利用したログイン
- [ ] JWTでのログイン必須なページ
- [ ] JSONのPOSTするページ



# CURLの場合
 事前にブラウザでログインしてみてDevtoolsでリクエストヘッダを確認しCookieの後もs区で送信しているセッションの項目.sessionをパラメタとして付与する。
 CurlのCookieをつけるパラメタは  -b オプションを付けてる
  
## GETの例

```  
curl "http://127.0.0.1:5000/top" -b "session=.eJwdzjEOwzAIAMC_eO4A2MaQz0TGgNo1aaaqf2_U6db7lD2POJ9lex9XPMr-8rIVrxUtkrVFVGpC7J6OOhLmdIKuIabpYMnGbYGHrMEign1WFGmDR0hG6FCGnDDjBrBaYGefbgRtrUQn62ZYBYFXLGVqplTuyHXG8d_g9weuxC_A.XrTerw.ZZu3AVm1f2curQAkHAplWfA-tUU"
```
 
 ## POSTの例
FormのデータをPostする場合は-F オプションを付ける。大抵のウェブサービスの処理でPost後に別の画面にリダイレクトするので-Lオプションを付けてあげると、Post->Redirect->GetとCurlが動いてくれる
  
```  
curl -L "http://127.0.0.1:5000/put" -d -F 'value="FOOBAR"' -b "session=.eJwdzjEOwzAIAMC_eO4A2MaQz0TGgNo1aaaqf2_U6db7lD2POJ9lex9XPMr-8rIVrxUtkrVFVGpC7J6OOhLmdIKuIabpYMnGbYGHrMEign1WFGmDR0hG6FCGnDDjBrBaYGefbgRtrUQn62ZYBYFXLGVqplTuyHXG8d_g9weuxC_A.XrTerw.ZZu3AVm1f2curQAkHAplWfA-tUU"  
```


# Apache Bench

## GETの例

```
abの場合は-Cオプションでクッキーを添付する
ab -n 10 -c 2 -C "session=.eJwdzjEOwzAIAMC_eO4A2MaQz0TGgNo1aaaqf2_U6db7lD2POJ9lex9XPMr-8rIVrxUtkrVFVGpC7J6OOhLmdIKuIabpYMnGbYGHrMEign1WFGmDR0hG6FCGnDDjBrBaYGefbgRtrUQn62ZYBYFXLGVqplTuyHXG8d_g9weuxC_A.XrTerw.ZZu3AVm1f2curQAkHAplWfA-tUU" http://127.0.0.1:5000/top
```

## POSRの例

Postdata.txtにフォームで送るデータを対応するように フォームの要素名=値の組を送る複数ある場合は&でつないでいく
value=FooBar&value2=HogeHoge

```
» ab -c 2 -n 10 -p postdata.txt -T "application/x-www-form-urlencoded"  -C "session=.eJwdzjEOwzAIAMC_eO4A2MaQz0TGgNo1aaaqf2_U6db7lD2POJ9lex9XPMr-8rIVrxUtkrVFVGpC7J6OOhLmdIKuIabpYMnGbYGHrMEign1WFGmDR0hG6FCGnDDjBrBaYGefbgRtrUQn62ZYBYFXLGVqplTuyHXG8d_g9weuxC_A.XrTerw.ZZu3AVm1f2curQAkHAplWfA-tUU" http://127.0.0.1:5000/put
```
- apache benchの注意点
  - サーバでエラーが発生してもエラー画面など何らかのレスポンスがある場合はComplete requestsとして扱われFailed Requestsにならないので必ずブラウザで動作確認する必要がある

