#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(test_args)
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
