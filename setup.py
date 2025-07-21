# setup.py
from setuptools import setup, find_packages

setup(
    name="ecommerce_helper",
    version="0.1.0",
    packages=find_packages(exclude=["tests", "deploy", ".*"]),
    install_requires=[
        # Add your dependencies here, if you use requirements.txt, you can leave it empty
    ],
    include_package_data=True,
)
