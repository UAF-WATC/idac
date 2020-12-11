import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="idac", # Replace with your own username
    version="0.0.1",
    author="Alex J.C. Witsil",
    author_email="ajwitsil@alaska.edu",
    description="Infrasound Data Augmentation and Classification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UAF-WATC/idac",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux, Mac OS",
    ],
    python_requires='>=3.6',
)
