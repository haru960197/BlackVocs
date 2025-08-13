## SERVICE
- `.env`を書き換えた場合、docker-imagesを再buildする必要あり
  - `$ docker compose down -v && docker compose build --no-cache && docker-compose up`を`service/`直下で実行

## WEB

- バックエンドのAPIを修正したときは，フロントエンド側のクライアントコードを修正する必要があるので，`web`直下で，`$npm run openapi-ts`を実行する
  - クライアントのコードは`@/lib/api`配下に生成される
  - ただし，これらはgit管理対象外
