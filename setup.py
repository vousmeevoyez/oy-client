import io
import os

from setuptools import setup, find_packages

dir_path = os.path.abspath(os.path.dirname(__file__))
readme = io.open(os.path.join(dir_path, 'README.md'), encoding='utf-8').read()


setup(
    name='oy-client',
    version='0.1',
    author='Kelvin Desman',
    author_email='kelvindsmn@gmail.com',
    description='Unofficial Oy Client library for Python',
    long_description=readme,
    url='https://github.com/vousmeevoyez/oy-client',
    license='MIT',
    packages=find_packages(exclude=["temp*.py", "test"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
    ],
)
