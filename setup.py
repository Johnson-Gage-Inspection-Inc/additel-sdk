import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyAdditel",
    use_scm_version=True,
    author="Jeff Hall",
    author_email="rhythmatician5@gmail.com",
    description="A Python SDK to communicate with Additel devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Johnson-Gage-Inspection-Inc/additel-sdk",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
