from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lambda_cloud_client",
    version="0.1.0",
    author="Christian",
    author_email="cdreetz@gmail.com",
    description="A client for interacting with Lambda Cloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cdreetz/lambda_cloud_client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "lambda-toolio=lambda_toolio.client:main",
        ],
    },
)