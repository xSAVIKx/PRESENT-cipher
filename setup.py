from distutils.core import setup

setup(
    name='present',
    version='0.0.2',
    packages=['present', 'gmac', 'gmac/util'],
    url='https://github.com/xSAVIKx/present',
    license='Apache License, Version 2.0',
    author='Iurii Sergiichuk',
    author_email='iurii.sergiichuk@gmail.com',
    description='python implementation of PRESENT cipher and minified version with 16-bit key and 8-bit block, implementation of GMAC using minified python algorithm as cipher'
)
