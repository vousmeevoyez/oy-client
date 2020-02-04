import io
import os

from setuptools import setup, find_packages

def getRequires():
    deps = [
        'requests>=2.22.0',
        'marshmallow>=3.4.0'
    ]
    return deps

dir_path = os.path.abspath(os.path.dirname(__file__))
readme = io.open(os.path.join(dir_path, 'README.md'), encoding='utf-8').read()


setup(
    name='oy-client',
    version='0.1',
    author='Kelvin Desman',
    author_email='kelvindsmn@gmail.com',
    url='https://github.com/vousmeevoyez/oy-client',
    packages=find_packages(exclude=["temp*.py", "test"]),
    include_package_data=True,
    license='MIT',
    description='Unofficial Oy Client library for Python',
    long_description=readme,
    install_requires=getRequires(),
)
