#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "networkx>=2.5",
    "numpy>=1.19.5",
    "rich>=11.2.0",
    "tqdm>=4.48.2"
]

test_requirements = ["pytest>=3", ]

setup(
    author="Hrishikesh Terdalkar",
    author_email='hrishikeshrt@linuxmail.org',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Wordle -- Game, Solver and Helper!",
    entry_points={
        'console_scripts': [
            'wordle=wordle.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='python-wordle,wordle,wordle-solver,wordle-helper,wordle-game',
    name='python-wordle',
    packages=find_packages(include=['wordle', 'wordle.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hrishikeshrt/python-wordle',
    version='0.1.3',
    zip_safe=False,
)
