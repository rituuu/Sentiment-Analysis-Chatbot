from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="SENTIMENT ANALYSIS CHATBOT",
    version="0.1",
    author="RITU GUJELA",
    packages=find_packages(),
    install_requires = requirements,
)