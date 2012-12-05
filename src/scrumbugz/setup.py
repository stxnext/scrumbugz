from setuptools import setup, find_packages
import os

name = "scrumbugz"
version = "0.1"


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

requires = [
    'django>=1.4.0',
    'psycopg2==2.4.5',
    'Django==1.4.2',
    'Unipath',
    'django-floppyforms',
    'python-dateutil==1.5',
    'simplejson',
    'django-jsonfield==0.8.10',
    'django-storages==1.1.4',
    'boto==2.3.0',
    'South==0.7.5',
    'Jinja2==2.6',
    'jingo==0.4',
    'jinja-bootstrap',
    'Markdown==2.2.0',
    'nose==1.2.1',
    'django-nose==1.1',
    'nose-progressive==1.3',
    'pytz==2012d',
    'django-cronjobs==0.2.3',
    'django-model-utils==1.1.0',
    'celery==3.0.9',
    'django-celery==3.0.9',
    'django-cache-machine',
    'requests==0.14.1',
    'django-auth-ldap==1.1.2',
]

dependency_links = [
    'https://github.com/jbalogh/django-cache-machine/tarball/master#egg=django-cache-machine',
    'https://github.com/auzigog/jinja-bootstrap/tarball/master#egg=jinja-bootstrap',
]

setup(
    name=name,
    version=version,
    description="",
    long_description=read('README'),
    classifiers=[],
    keywords="",
    author="",
    author_email='',
    url='',
    license='',
    package_dir={'': '.'},
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    dependency_links=dependency_links,
    entry_points="""
    """,
)
