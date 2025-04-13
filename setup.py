import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyairstage",
    author="Daniel Rufus Kaldheim",
    author_email="daniel@kaldheim.org",
    description="Python library to control Fujitsu Airstage Airconditioners",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielkaldheim/pyairstage",
    license="MIT License",
    packages=["pyairstage"],
    install_requires=["aiohttp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
