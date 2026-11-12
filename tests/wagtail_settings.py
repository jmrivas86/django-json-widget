from .settings import *  # noqa: F403

INSTALLED_APPS += [  # noqa: F405
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'modelcluster',
    'wagtail',
    'wagtail.admin',
    'wagtail.users',
    'wagtail.images',
    'wagtail.documents',
    'wagtail.snippets',
    'wagtail.search',
]
STATIC_URL = '/static/'
WAGTAILADMIN_BASE_URL = 'http://localhost'

