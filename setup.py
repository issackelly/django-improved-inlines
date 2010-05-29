import os
from distutils.core import setup
 
#f = open(os.path.join(os.path.dirname(__file__), 'README.markdown'))
#readme = f.read()
#f.close()
 
setup(
    name = "django-improved-inlines",
    version = "0.1.3a",
    url = 'http://github.com/issackelly/django-improved-inlines',
    license = 'BSD',
    description = "Inline object rendering for django, based on django-basic-apps + filters + templates",
    author = 'Issac Kelly',
    author_email = 'issac@kellycreativetech.com',
    packages = [
        'inlines',
        'inlines.templatetags',
    ],
    #long_description=readme,
    package_data={'inlines': ['*.markdown']},
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