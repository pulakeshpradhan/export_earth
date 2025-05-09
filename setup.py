from setuptools import setup, find_packages

setup(
    name='export_earth',
    version='0.1.0',
    description='A package for exporting and downloading Earth Engine images.',
    author='Pulakesh Pradhan',
    author_email='pulakesh.mid@gmail.com',
    packages=find_packages(),
    install_requires=[
        'earthengine-api',
        'geemap',
    ],
)
