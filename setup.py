from distutils.=jedi#complete_opened()
ore import setup
from setuptools import find_packages

setup(
    name='pyrelate',
    version='1.0.0',
    author='sendwithus',
    author_email='matt@sendwithus.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/sendwithus/pyrelate',
    license='LICENSE.txt',
    description='Python API client for relateiq',
    long_description=open('README.md').read(),
    test_suite="relate.test",
    install_requires=[
        "requests >= 1.1.0"
    ]
)
