from setuptools import setup

long_description = None
with open("README.md", 'r') as fp:
    long_description = fp.read()

setup(
    name = 'pyGinlong',
    packages = ['ginlong'],
    install_requires=['aiohttp', 'async_timeout'],
    version='0.0.1',
    description='A python3 library to communicate with Ginling',
    long_description=long_description,
    python_requires='>=3.5.3',
    author='Aleksander Lyse',
    author_email='aleksander.lyse@gmail.com',
    url='https://github.com/alekslyse/ginlong/',
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
)