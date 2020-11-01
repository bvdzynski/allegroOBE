from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="allegroOBE",
    version="0.0.1",
    description="Tool for Allegro offers batch editing.",
    py_modules=["allegroOBE"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    extras_require={"dev": []},
    url="",
    author="Maciej Budzowski",
    author_email="maciek.budzowski777@gmail.com",
)