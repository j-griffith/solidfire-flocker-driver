import os

from setuptools import find_packages
from setuptools import setup

DESCRIPTION = "SolidFire Storage Plugin/Agent for Flocker."

if os.path.exists('README.rst'):
    with open('README.rst', 'r', 'utf-8') as readme_file:
        LONG_DESCRIPTION = readme_file.read()
else:
    LONG_DESCRIPTION = DESCRIPTION

setup(
    name='solidfire-flocker-driver',
    version='0.0.1',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='John Griffith',
    author_email='john.griffith@solidfire.com',
    packages=find_packages(),
    license='Apache 2.0',
    zip_safe=False,
    url='http://github.com/solidfire/solidfire-flocker-driver',
    install_requires=[
        'six >= 1.7.0',
        'requests >= 2.7.0',
    ],
    keywords=['solidfire', 'flocker', 'docker', 'driver', 'python'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache 2.0',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 2.7',
    ],
)
