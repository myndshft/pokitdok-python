"""
PokitDok Platform API Client for Python
---------------------------------------

DESCRIPTION
The PokitDok Platform API Client makes it easy it interact with the
PokitDok Platform APIs when writing client applications in Python.

See https://platform.pokitdok.com for more information.

LICENSE
The PokitDok Platform API Client for Python is distributed under the MIT License
"""
from setuptools import setup


setup(
    name="pokitdok",
    version="0.1",
    license="MIT",
    author="PokitDok, Inc.",
    author_email="support@pokitdok.com",
    url="https://platform.pokitdok.com",
    description="PokitDok Platform API Client",
    long_description=__doc__,
    packages=["pokitdok", "pokitdok.api"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=[
        "requests>=2.3.0", "requests-oauthlib>=0.4.0"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)