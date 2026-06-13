# Installing the required dependencies for the project.
from setuptools import setup, find_packages
with open ('req.txt') as f:
    req = f.read().splitlines()

setup(
    name = 'medical_project',
    packages= find_packages(),
    install_requires=req,
)
