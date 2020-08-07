import os
from os.path import join, dirname

from setuptools import setup, find_packages

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirementPath = lib_folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name='extracticle',
    description='Websites article extractor',
    author='Pavel Danilov',
    license='',
    author_email='PavelDanilov.76@yandex.com',
    url='https://github.com/paveldanilov76/extracticle',
    version=1.0,
    install_requires=install_requires,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'console_scripts':
            [
                'extracticle = extracticle.main:run',
            ]
    }
)
