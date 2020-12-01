import setuptools

VERSION = 0.1


def get_description():
    with open("README.md", "r") as md:
        long_description = md.read()
    return long_description


def get_requirements():
    with open("requirements.txt") as f:
        requirements = f.readlines()
    return [i.replace(r"\n", "") for i in requirements]


setuptools.setup(
    name="safe-regex",
    version=VERSION,
    author="Steven Ensslen",
    author_email="steven@claritycloudworks.com",
    description="Embeds unit tests with regular expressions",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/ensslen/safe-regex",
    keywords=["test", "regular expression"]
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=get_requirements(),
)
