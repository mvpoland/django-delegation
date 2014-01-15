from setuptools import setup, find_packages

import django_delegation

setup(
    name = "cl_payments",
    version = django_delegation.__version__,
    url = 'http://github.com/vikingco/django-delegation',
    license = 'mit',
    description = "City Live Payments",
    long_description = open('README.md','r').read(),
    author = 'Jef Geskens, VikingCo NV',
    packages = find_packages(),
    package_data = {'cl_payments': [
                    'templates/*.html', 'templates/*/*.html', 'templates/*/*/*.html'
                ],},
    zip_safe=False, # Don't create egg files, Django cannot find templates in egg files.
    include_package_data=True,
    classifiers = [
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
