# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import setuptools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name='hotfn',
    version='0.0.2',
    description='Library to provide HTTP over STDIN/STDOUT',
    long_description=read('README.md'),
    url='https://hotfn.readthedocs.org',
    author='Denis Makogon',
    author_email='lildee1991@gmail.com',
    packages=setuptools.find_packages(exclude=["hotfn.tests", ]),
    install_requires=[],
    license='License :: OSI Approved :: Apache Software License',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Environment :: No Input/Output (Daemon)',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: '
        'Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
    keywords=['functions', 'lambdas', 'python API'],
    platforms=['Linux', 'Mac OS-X', 'Unix'],
    tests_require=[
        "flake8==2.5.0",
        "hacking<0.11,>=0.10.0",
        "testtools>=1.4.0",
        "pytest-cov==2.4.0",
        "pytest-cov",
    ],
    zip_safe=True,
)
