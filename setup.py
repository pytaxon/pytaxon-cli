#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as arq:
    readme = arq.read()

setup(
    name='pytaxon',
    version='3.0.0',
    setup_requires=['wheel'],
    license='MIT License',
    author='Marco Aurélio Proença Neto, Marcos Paulo Alves de Sousa',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='desousa.mpa@gmail.com',
    keywords='pytaxon',
    description=u'Pytaxon é uma aplicação open source de auxílio à pesquisa para identificação de erros e correção de nomenclatura taxonômica das espécies da biodiversidade',
    packages=['pytaxon'],
    entry_points={
        'console_scripts': [
            'pytaxon = pytaxon.main:main',
        ],
    },
    install_requires=['pandas', 'openpyxl', 'tqdm', 'xlrd', 'thefuzz', 'requests', 'argparse'],
    url='https://github.com/pytaxon'
)
