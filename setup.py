import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="additel_sdk",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python SDK to communicate with Additel devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourname/additel_sdk",  # Update to your project URL
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or your chosen license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
