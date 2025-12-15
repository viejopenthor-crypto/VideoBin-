from setuptools import setup, find_packages

setup(
    name="videobin-plus",
    version="2.0.0",
    packages=find_packages(),
    install_requires=["opencv-python", "reedsolo", "pycryptodome", "click"],
    entry_points={"console_scripts": ["videobin=videobin.cli:cli"]},
)
