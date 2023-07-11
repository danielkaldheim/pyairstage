import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyairstage",
    version="1.0.0",
    author="Daniel Rufus Kaldheim",
    author_email="daniel@kaldheim.org",
    description="Python library to control Fujitsu Airstage Airconditioners",
    long_description="Python library to control Fujitsu Airstage Airconditioners",
    url="https://github.com/danielkaldheim/pyairstage",
    license="MIT License",
    packages=["pyairstage"],
    install_requires=["requests", "certifi", "chardet", "idna", "urllib3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
