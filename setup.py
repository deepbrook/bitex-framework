from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="bitex-framework",
    version="1.2.1",
    author='Nils Diefenbach',
    author_email='nlsdfnbch.foss@kolabnow.com',
    description="Core Module of the Bitcoin Exchange (BitEx) REST API Framwork",  # Optional
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/crypto-toolbox/bitex-framework',

    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['requests', 'pluggy'],
    extras_require={
        'dev': ['black', 'isort', 'flake8'],
        'test': ['pytest', 'pytest-cov', 'tox'],
        'ci': ['twine'],
    },

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='bitcoin rest api http exchange',
    project_urls={
        'Bug Reports': 'https://github.com/crypto-toolbox/bitex-framework/issues',
        'Source': 'https://github.com/crypto-toolbox/bitex-framework',
    },
)
