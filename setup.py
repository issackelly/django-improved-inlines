import os
from setuptools import setup

setup(
    name = "django-improved-inlines",
    version = "0.2.2",
    url = 'http://github.com/issackelly/django-improved-inlines',
    license = 'BSD',
    description = "Inline object rendering for django, based on django-basic-apps + filters + templates",
    long_description=open("README.rst").read(),
    author = 'Issac Kelly',
    author_email = 'issac@kellycreativetech.com',
    packages = [
        'improved_inlines',
        'improved_inlines.templatetags',
    ],
    requires = [
        'BeautifulSoup',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    
    install_requires=['beautifulsoup>=3.2.0',],
    
)