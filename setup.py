"""
Flask-Less
-------------

A Flask extension to add lesscpy support to the template, and
recompile less file if changed.

"""
from setuptools import setup

setup(
    name='Flask-Less',
    version='0.1',
    url='https://github.com/mrf345/flask_less/',
    download_url='https://github.com/mrf345/flask_less/archive/0.1.tar.gz',
    license='MIT',
    author='Mohamed Feddad',
    author_email='mrf345@gmail.com',
    description='less compiler flask extension',
    long_description=__doc__,
    py_modules=['lessc'],
    packages=['flask_less'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'hashlib',
        'lesscpy'
    ],
    keywords=['flask', 'extension', 'less', 'compiler', 'lesscpy',
              'css'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
