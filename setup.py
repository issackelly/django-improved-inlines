import os
from distutils.core import setup
 
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
 
README = read('README.markdown')
 
setup(
    name = "django-improved-inlines",
    version = "0.1.0a",
    url = 'http://github.com/issackelly/django-improved-inlines',
    license = 'BSD',
    description = "Inline object rendering for django, based on django-basic-apps + filters + templates",
    long_description=README,
    author = 'Issac Kelly',
    author_email = 'issac@kellycreativetech.com',
    packages = [
        'inlines',
        'inlines.templatetags',
    ],
    requires = [
        'BeautifulSoup',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)