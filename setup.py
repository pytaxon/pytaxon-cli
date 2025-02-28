#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as arq:
    readme = arq.read()

setup(
    name='pytaxon',
    version='v0.2.6',
    setup_requires=['wheel'],
    license='MIT License',
    author='Marco Aurélio Proença Neto, Marcos Paulo Alves de Sousa',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='desousa.mpa@gmail.com',
    keywords='pytaxon',
    description=u'Pytaxon é uma aplicação open source de auxílio à pesquisa para identificação de erros e correção de nomenclatura taxonômica das espécies da biodiversidade',
    packages=['pytaxon'],
    package_data={'pytaxon': ['assets/pytaxon_logo.png']},
    entry_points={
        'console_scripts': [
            'pytaxon = pytaxon.main:main',
            'pytaxonGUI = pytaxon.pytaxon_gui:pytaxon_gui'
        ],
    },
<<<<<<< Updated upstream
    install_requires=['pandas', 'openpyxl', 'tqdm', 'xlrd', 'requests', 
                      'argparse', 'ttkthemes', 'tk', 'matplotlib', 'customtkinter', 
                      'CTkMessagebox', 'pytest'],
=======
    install_requires=[
    'certifi==2022.12.7',
    'cffi==1.15.1',
    'charset-normalizer==3.1.0',
    'et-xmlfile==1.1.0',
    'idna==3.4',
    'Jinja2==3.1.2',
    'MarkupSafe==2.1.2',
    'numpy==1.24.2',
    'openpyxl==3.1.2',
    'packaging==23.1',
    'pandas==1.5.3',
    'pycparser==2.21',
    'python-dateutil==2.8.2',
    'pytz==2022.7.1',
    'pytz-deprecation-shim==0.1.0.post0',
    'requests==2.28.2',
    'rpy2==3.5.11',
    'six==1.16.0',
    'tzdata==2023.3',
    'tzlocal==4.3',
    'urllib3==1.26.15'
],
>>>>>>> Stashed changes
    url='https://github.com/pytaxon-cli'
)
