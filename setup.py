from setuptools import setup, find_packages

import admin2

LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='django-admin2',
    version=admin2.__version__,
    description="An introspective interface for Django's ORM.",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='django,admin',
    author=mongonaut.__author__,
    author_email='pydanny@gmail.com',
    url='http://github.com/pydanny/django-admin2',
    license='MIT',
    packages=find_packages(exclude=['examples']),
    include_package_data=True,
    install_requires=['django>=1.5.0', 'django-braces=='],
    zip_safe=False,
)