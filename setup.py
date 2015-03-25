from setuptools import setup
import sys

pkgversion = '0.1'

setup(
    name='urlsync',
    version=pkgversion,
    description='Download a file from the interwebs and stash it locally...ONCE!',
    author='Adam Kaufman',
    author_email='kaufman.blue@gmail.com',
    url='https://github.com/ajk8/python-urlsync',
    download_url='https://github.com/ajk8/python-urlsync/tarball/' + pkgversion,
    license='MIT',
    entry_points={'console_scripts': ['urlsync=urlsync:main']},
    test_suite='tests',
    install_requires=[
        'docopt>=0.6.2',
        'funcy>=1.4',
        'requests>=2.6.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development'
    ],
    keywords='rsync download'
)
