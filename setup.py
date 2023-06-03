from setuptools import setup, find_packages

setup(
    name="opendigger",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "plotext",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "opendigger = opendigger:main",
        ],
    },
    author="TOMYUE",
    author_email="tomyue2002@gmail.com",
    description="A CLI tool for fetching OpenDigger metrics",
    url="https://github.com/TOMYUE/opendigger-cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)