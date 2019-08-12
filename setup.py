#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import (setup, find_packages)

__version__ = '1.0.3'

setup(
    name='django-address-model',
    version=__version__,
    packages=find_packages(exclude=["*demo"]),
    include_package_data=True,
    zip_safe=False,
    description='Django Address Model',
    url='https://github.com/agusmakmun/django-address-model',
    download_url='https://github.com/agusmakmun/django-address-model/tarball/v%s' % __version__,
    keywords=['django address', 'django address model'],
    long_description=open('README.rst').read(),
    license='MIT',
    author='Agus Makmun (Summon Agus)',
    author_email='summon.agus@gmail.com',
    install_requires=['django'],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
    ]
)
