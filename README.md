## SERVICE
- `.env`を書き換えた場合、docker-imagesを再buildする必要あり
  - `$ docker compose down -v && docker compose build --no-cache && docker-compose up`を`service/`直下で実行

### DBの構造、Modelsの使い方について

![DB structure](https://private-user-images.githubusercontent.com/106721539/492382633-fb434f56-449a-49b7-85dc-d96bfe6c5f01.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTg4MTQxMjAsIm5iZiI6MTc1ODgxMzgyMCwicGF0aCI6Ii8xMDY3MjE1MzkvNDkyMzgyNjMzLWZiNDM0ZjU2LTQ0OWEtNDliNy04NWRjLWQ5NmJmZTZjNWYwMS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwOTI1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDkyNVQxNTIzNDBaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yZTY0NDdhNzE0ZTFkNzRhMTFmMzI1ZjQwNjE0NDNhMmI0NzIyZGE4NTM5ZGI3NTExY2YzMzFhMDZhYjRiYWM1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.oMQiYvCbYROxXO0LG82g21JURdpRzHKib9_9eF1PMoI)

Modelsは以下の通り
- `word.py`: wordテーブルに保存するフィールドの指定
- `user.py`: userテーブルに保存するフィールドの指定
- `user_word.py`: wordテーブルに保存するフィールドの指定
- `common.py`: これらにまたがって使われたり、service層で使うモデルの定義


## WEB

- バックエンドのAPIを修正したときは，フロントエンド側のクライアントコードを修正する必要があるので，`web`直下で，`$npm run openapi-ts`を実行する
  - クライアントのコードは`@/lib/api`配下に生成される
  - ただし，これらはgit管理対象外

## ブランチ運用

- Git Flowに従って，developブランチから切って作業をする
- releaseブランチの変更はdevelopブランチにも反映させる

### ブランチ名

`type/issue-num/description`

- `type`
    - `feature`
    - `fix`
- `issue-num`
    - issueの番号
    - `#33`なら，`feature/33/~~`
- `description`
    - そのブランチに関する簡単な説明

## その他

- 以下を作成するときは，Labelを付与
    - issue
    - pull request
