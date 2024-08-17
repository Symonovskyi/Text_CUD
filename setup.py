from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="text_cud",
    version="2024.08.17",
    description="A Python module for creating, updating, and deleting attributes in XML/HTML content.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Symonovskyi",
    author_email="github@Symonovskyi.pp.ua",
    url="https://github.com/Symonovskyi/Text_CUD",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.9.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="html xml markup processing async multithreading",
)
