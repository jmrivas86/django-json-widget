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
    from django.db.models import JSONField
    from django_json_widget.widgets import JSONEditorWidget
    from .models import YourModel


    @admin.register(YourModel)
    class YourModelAdmin(admin.ModelAdmin):
        formfield_overrides = {
            JSONField: {'widget': JSONEditorWidget},
        }

You can also add the widget in your forms.py:

.. code-block:: python

    from django import forms
    from django_json_widget.widgets import JSONEditorWidget
    from .models import YourModel


    class YourForm(forms.ModelForm):
        class Meta:
            model = YourModel

            fields = ('jsonfield',)

            widgets = {
                'jsonfield': JSONEditorWidget
            }

Configuration
-------------

You can customize the JSONEditorWidget with the following options:

* **width**: Width of the editor as a string with CSS size units (px, em, % etc). Defaults to ``90%``.
* **height**: Height of the editor as a string CSS size units. Defaults to ``550px``.
* **options**: A dict of options accepted by the `JSON editor`_. Options that require functions (eg. onError) are not supported.
* **mode (deprecated)**: The default editor mode. This argument is redundant because it can be specified as a part of ``options``.  Preserved for backwards compatibility with version 0.2.0.
* **attrs**: HTML attributes to be applied to the wrapper element. See the `Django Widget documentation`_.

.. _json editor: https://github.com/josdejong/jsoneditor/blob/master/docs/api.md#configuration-options
.. _Django Widget documentation: https://docs.djangoproject.com/en/2.1/ref/forms/widgets/#django.forms.Widget.attrs


JSONEditorWidget widget
-----------------------

Before:

.. image:: https://raw.githubusercontent.com/jmrivas86/django-json-widget/master/imgs/jsonfield_0.png

After:

.. image:: https://raw.githubusercontent.com/jmrivas86/django-json-widget/master/imgs/jsonfield_1.png


Development Guide
-----------------

This section provides instructions for setting up a development environment and contributing to django-json-widget.

Setting up Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Clone the repository**::

    git clone https://github.com/jmrivas86/django-json-widget.git
    cd django-json-widget

2. **Create a virtual environment** (recommended)::

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install development dependencies**::

    pip install -r requirements_dev.txt

4. **Install test dependencies**::

    pip install -r requirements_test.txt

5. **Install the package in development mode**::

    pip install -e .

Running Tests
~~~~~~~~~~~~~

The project includes several ways to run tests:

**Using the runtests.py script** (recommended)::

    python runtests.py

This will run all tests using Django's test runner with the test settings.

**Using tox for multiple environments**::

    tox

This will run tests against multiple Python and Django version combinations as defined in ``tox.ini``.

**With coverage reporting**::

    coverage run --source django_json_widget runtests.py
    coverage report
    coverage html  # Generates HTML coverage report

Test Structure
~~~~~~~~~~~~~~

The test suite is organized as follows:

* ``tests/test_widgets.py`` - Core widget functionality tests
* ``tests/test_widget_security.py`` - Security-focused tests
* ``tests/settings.py`` - Test-specific Django settings

The tests cover:

* Widget initialization and configuration
* Media file handling (CSS/JS)
* Template rendering and context generation
* Form integration
* Security aspects (XSS prevention, safe JSON handling)
* Performance with large datasets
* Edge cases and error handling

Code Quality
~~~~~~~~~~~~

**Run linting with auto-fix**::

    ruff check --fix

**Check test coverage**::

    coverage run --source django_json_widget runtests.py
    coverage report --show-missing

Aim for maintaining or improving test coverage.

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
