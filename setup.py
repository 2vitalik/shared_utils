import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shared-utils",
    version="0.0.17",
    author="Vitalik",
    author_email="2vitalik@gmail.com",
    description="Shared utils for different projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/2vitalik/shared_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
