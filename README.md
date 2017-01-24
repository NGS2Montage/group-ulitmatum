# Getting Started

1. To get started developing, run `pip install -r requirements/local.txt` first (probably in a virtualenv).

1. This project loads configuration from a `.env` file. Because this file might contain secrets it should be distributed separately from the git repository. If you just want to get running locally copy the provided `.env.sample` to `.env`.

1. Run `./manage.py migrate` to prepare the database. Also run `./manage.py createsuperuser` so you have a user to play around with.

1. Run the server with `./manage.py runserver`. In a browser open some URL that we serve, for instance `localhost:8000/phase2/public-goods`

    1. To list all the URLs we serve use `./manage.py show_urls` or inspect the `urls.py` files.


## Make more users

Run `./manage.py shell` then use these commands at the prompt:

```
from django.contrib.auth.models import User
User.objects.create_user("user_name", password="password")
```
