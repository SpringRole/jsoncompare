#!/usr/bin/env python

from setuptools import setup


def read_readme(fname):
    try:
       import pypandoc
       return pypandoc.convert('README.md', 'rst')
    except (IOError, ImportError):
       return ''


setup(
    name = 'json-evaluator',
    version = '0.1',
    description = 'Json Evaluation tool',
    author = 'SpringRole',
    author_email = '',
    url = '',
    packages = ['jsoncompare', 'jsoncompare.test'],
    test_suite = "jsoncompare.test.test_jsoncompare",
    keywords = 'json comparison compare order',
    long_description = read_readme('README.md'), install_requires=['sklearn']
)
