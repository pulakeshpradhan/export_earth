from setuptools import setup, find_packages

setup(
    name='gee_export_utils',
    version='0.1.0',
    description='A package for exporting and downloading Earth Engine images.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'earthengine-api',
        'geemap',
    ],
)
