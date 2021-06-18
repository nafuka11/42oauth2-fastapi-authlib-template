# 42oauth2-fastapi-authlib-template

fastapi + authlibで42のoauth2認証をするためのテンプレートです。

## 使い方

### 環境変数の設定（.env）

`.env.example` を `.env` にリネームし、値を変更してください。

|環境変数名|説明|
|--|--|
|CLIENT_ID|42 APIのUID|
|CLIENT_SECRET|42 APIのSecret|
|SESSION_SECRET_KEY|Cookieベースのsessionを暗号化するキーとなる文字列|

### lint & format

```bash
# black, flake8, mypy, isort
pipenv run lint
# black isort
pipenv run format
```

### サーバの起動

開発環境
```bash
pipenv run dev
```

ローカルで動かす場合は、[ngrok](https://ngrok.com/) を使うとoauth2認証の確認ができます。
```bash
ngrok http 8000
```

## Herokuへのデプロイ

### 環境変数の設定

```
heroku config:set CLIENT_ID=""
heroku config:set CLIENT_SECRET=""
heroku config:set SESSION_SECRET_KEY=""
```

### Procfile

```
web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}
```

## その他

- デフォルトだとセッションの有効期限が2週間なので少し長いかもしれません。
