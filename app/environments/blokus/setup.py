from setuptools import setup, find_packages

setup(
    name='blokus',
    version='0.1.0',
    description='Blokus Gym Environment',
    packages=find_packages(),
    install_requires=[
        'gym>=0.9.4',
        'numpy>=1.13.0',
        'opencv-python>=3.4.2.0',
    ]
)


