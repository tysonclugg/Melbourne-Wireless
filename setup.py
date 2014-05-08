'''
Melbourne Wireless Web Admin setup script
'''
from setuptools import setup

setup(
    name = 'melbwireless',
    version = '2012.03.07',
    packages = [
        'melbwireless',
    ],
    description = 'Melbourne Wireless Web Admin',
    zip_safe = False,
    Xinstall_requires = [
        'Django>=1.6,<1.7',
        'django-extensions>=1.2',
    ],
    scripts = [
    ],
)
