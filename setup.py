from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='Memorsy!',
    version='0.1.0',
    description='Memorsy!',
    long_description=readme,
    author='Kate Rymsza',
    author_email='rymszakasia@gmail.com',
    packages=find_packages(exclude=('src', 'components', 'keys', 'store', 'utils'))
)