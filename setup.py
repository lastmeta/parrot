import setuptools

def get_long_description():
    with open("README.md", "r") as fh:
        return fh.read()

setuptools.setup(
    name='parrot',
    version='0.1',
    description='at home simple backup system',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['click', 'PyYaml', 'boxset'],
    python_requires='>=3.5.2',
    author='Jordan Miller',
    author_email="paradoxlabs@protonmail.com",
    url="https://github.com/lastmeta/parrot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "parrot = parrot.cli.parrot:main",
        ]
    },
)
