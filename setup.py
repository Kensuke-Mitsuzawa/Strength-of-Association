__author__ = 'kensuke-mi'


from setuptools import setup, find_packages
import sys

sys.path.append('./SoA/')
sys.path.append('./test')


install_requires = []


setup(
    author='Kensuke Mitsuzawa',
    name = 'SoA',
    version='0.1',
    test_suite='test_soa.suite',
    install_requires = install_requires,
    packages=[
        "SoA"
    ],

)