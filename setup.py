from setuptools import setup, find_packages

setup(
    name='cyaron',
    version='0.1.1',
    keywords='cyaron luogu',
    description='CYaRon: Yet Another Random Olympic-iNformatics test data generator, A library for automatically generating test data for Online Judge, Olympic Informatics or automatic application testing',
    license='GPLv3',
    url='https://www.luogu.org/',
    author='Luogu Development Team',
    author_email='k@luogu.org',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[],
)
