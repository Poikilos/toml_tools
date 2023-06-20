try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import tomli

with open("README.md") as readme_file:
    readme_string = readme_file.read()

setup(
    name="tomli",
    version=tomli.__version__,
    description="Tomli and Tomli-W for Python 2 and Iron Python",
    author="Taneli Hukkinen",
    author_email="poikilos@users.noreply.github.com",
    url="https://github.com/Poikilos/toml_tools",
    packages=['tomli'],
    license="MIT",
    long_description=readme_string,
    long_description_content_type = 'text/markdown',
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: IronPython',
    ]
)
