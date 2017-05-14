=============================
django-json-widget
=============================

.. image:: https://badge.fury.io/py/django-json-widget.svg
    :target: https://badge.fury.io/py/django-json-widget

.. image:: https://travis-ci.org/jmrivas86/django-json-widget.svg?branch=master
    :target: https://travis-ci.org/jmrivas86/django-json-widget

.. image:: https://codecov.io/gh/jmrivas86/django-json-widget/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jmrivas86/django-json-widget

An alternative widget that makes it easy to edit the new Django's field JSONField (PostgreSQL specific model fields)


Quickstart
----------

Install django-json-widget::

    pip install django-json-widget

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_json_widget',
        ...
    )

Add the widget in your admin.py:

.. code-block:: python

    from django.contrib import admin
    from django.contrib.postgres import fields
    from django_json_widget.widgets import JSONEditorWidget
    from .models import YourModel


    @admin.register(YourModel)
    class YourModelAdmin(admin.ModelAdmin):
        formfield_overrides = {
            fields.JSONField: {'widget': JSONEditorWidget},
        }

JSONEditorWidget widget
-----------------------

Before:

.. image:: https://raw.githubusercontent.com/jmrivas86/django-json-widget/master/imgs/jsonfield_0.png

After:

.. image:: https://raw.githubusercontent.com/jmrivas86/django-json-widget/master/imgs/jsonfield_1.png


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
