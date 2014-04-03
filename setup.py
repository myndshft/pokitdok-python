"""
pokitdok
--------------------

PokitDok Platform API Client for Python
"""
from setuptools import setup


setup(
    name='PokitDok-Python',
    version='0.0.1',
    url='https://github.com/PokitDokInc/pokitdok-python',
    license='Other/Proprietary License',
    author='PokitDok, Inc.',
    author_email='dev@pokitdok.com',
    description='PokitDok Platform API Client for Python',
    long_description=__doc__,
    packages=['pokitdok'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests>=2.0.1'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)