# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-naremitimg',
    version='0.1.3',
    author=u'Jon Combe',
    author_email='pypi@joncombe.net',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/naremit/NaremitIMG',
    license='BSD licence, see LICENCE file',
    description='A tiny Django app for performing image manipulations on the fly.',
    long_description='NaremitIMG is tiny Django app which enables dynamic image manipulation on the fly. This could be used, for example, in conjunction with an online image editing tool, or to create thumbnails or to serve responsive images via a CDN.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Graphics',
    ],
    zip_safe=False,
)
