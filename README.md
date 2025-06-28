# 開発環境

- Raspberry Pi Zero 2 W
- Raspberry Pi Pico 2 W
- Ubuntu Server 24.04.2 LTS (64-bit)
- Docker 28.3.0
- Python 3.12.10
- Django 5.2.1
- PostgreSQL 17

# Home の初期設定

途中で Django と PostgreSQL の環境変数を `/smart-home/.env` に保存するため、DEBUG（Ture か False） と USERNAME と PASSWORD を入力してください。

```
curl -o setup.sh https://raw.githubusercontent.com/Yaaamashiro/smart-home/refs/heads/main/home/setup.sh
bash setup.sh
```

# 参考文献

- [Django ドキュメント](https://docs.djangoproject.com/ja/5.2/ "Django ドキュメント | Django document")

- [Django アプリを Docker 化する方法: 初心者向けのステップバイステップガイド](https://www.docker.com/ja-jp/blog/how-to-dockerize-django-app/ "アプリを Docker 化する方法: 初心者向けのステップバイステップガイド | Docker")

- [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/ "Ubuntu | Docker Docs")
