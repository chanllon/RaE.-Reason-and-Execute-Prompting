from setuptools import setup, find_packages

setup(name='RaE',
      version='0.1',
      description='RaE',
      packages=['RaE', 'RaE.core', 'RaE.prompt'],
      install_requires=['openai', 'python-dateutil'],
)