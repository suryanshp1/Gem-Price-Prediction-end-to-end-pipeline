from setuptools import find_packages,setup
from typing import List

setup(
    name='GemPricePrediction',
    version='0.0.1',
    author='Suryansh Pandey',
    author_email='suryanshp1@gmail.com',
    install_requires=["scikit-learn","pandas","numpy"],
    packages=find_packages()
)