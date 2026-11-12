# Wagtail JSON widget demo

This local-only demo uses a separate SQLite database. It exercises a JSON field
on the Home page and JSON fields in a Wagtail InlinePanel, including new rows.

From the repository root, set up and run it:

```sh
python3.11 -m venv /tmp/django-json-widget-wagtail-venv
/tmp/django-json-widget-wagtail-venv/bin/pip install 'wagtail~=7.2.0' 'django~=5.2.0'
cd example/wagtail_demo
export PYTHONPATH="$(pwd)/../.."
/tmp/django-json-widget-wagtail-venv/bin/python manage.py migrate
/tmp/django-json-widget-wagtail-venv/bin/python manage.py createsuperuser
/tmp/django-json-widget-wagtail-venv/bin/python manage.py runserver 127.0.0.1:8766
```

Open http://127.0.0.1:8766/admin/, log in, then go to Pages → Home → Edit.
Change **Settings json**, add a **JSON item**, and edit its **Data**. Save a
draft, reload the editor, and check both values. Try invalid JSON and clearing
the fields as well.