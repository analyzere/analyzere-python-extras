from codecs import open
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

install_requires = []
extras_require = {}

with open(path.join(here, 'requirements', 'install.txt'),
          encoding='utf-8') as f:

    for line in f:
        index_of_semicolon = line.find(';')
        if index_of_semicolon == -1:
            install_requires.append(line.strip())
        else:
            condition = ':' + line[index_of_semicolon + 1:].strip()
            packages = [line[:index_of_semicolon].strip()]
            extras_require[condition] = packages

setup(
    name='analyzerePythonTools',
    version='0.1.5',
    description='Python extras to support the analyzere package',
    long_description=readme,
    url='https://github.com/analyzere/analyzere-python-extras',
    author='Analyze Re',
    author_email='support@analyzere.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.8',

        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=[
        'analyzerePythonTools',
    ],
    install_requires=install_requires,
    extras_require=extras_require
)
