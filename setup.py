# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
setup(
    name='django-tesla-client',
    version='0.1',
    author=u'Azamat Tokhtaev',
    author_email='krik123@gmail.com',
    url='https://github.com/ITAttractor/Tesla-Client',
    license='BSD License',
    description='sends notificaiton to tesla service and installs to demo when build is successful',
    long_description=open('README.md').read(),
    zip_safe=False,
    packages=find_packages(),
)
