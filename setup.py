from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='Memorsy!',
    version='0.1.0',
    description='Memorsy! Game',
    long_description=readme,
    author='Kate Rymsza',
    author_email='rymszakasia@gmail.com',
    packages=find_packages(exclude=('clientServer', 'components', 'keys', 'store', 'utils'))
)