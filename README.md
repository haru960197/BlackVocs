## How to develop

1. `$ git clone https://github.com/haru960197/BlackVocs.git`
2. `$ git config commit.template .commit_template` 
3. `.env.example`ファイルをコピーして`.env`ファイルを作成
4. `$ git checkout develop`;
5. `$ git pull` (もしdevelopブランチが更新されない場合，`$ git reset --hard origin/develop`を実行)
6. `$ git checkout -b branch_name`
7. serviceを起動
    1. `$ cd ./service`
    2. `$ docker compose up` (docker-desktopを立ち上げた状態で行う) 
8. webを起動
    1. `$ cd ../web/`
    2. `$ npm install`
    3. `$ npm run dev` (失敗する場合は，`$ npm run openapi-ts`を実行)

### 注意点

- serviceを先に起動しないと，`localhost:4000/openapi.json`へのフェッチが失敗し，openapiによるクライアント生成ができないことに注意．

## SERVICE
### General 
- `.env`を書き換えた場合、docker-imagesを再buildする必要あり
-> `$ docker compose down -v && docker compose build --no-cache && docker-compose up`を`service/`直下で実行

### Database 
- データベース名：`.env`に記載
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

