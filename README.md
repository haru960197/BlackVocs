# SERVICE
- `.env`を書き換えた場合、docker-imagesを再buildする必要あり
  - `$ docker-compose down && docker-compose build && docker-compose up`を`service/`直下で実行