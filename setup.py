#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

here = path.abspath(path.dirname(__file__))
README = open(path.join(here, 'README.md')).read()
CONFIG_FILE = path.join(here, 'config.ini')
requires = [
  'ConfigParser', 
  'python-dateutil', 
  'requests',
  'SQLAlchemy',
  'psycopg2',
  'python-daemon'
]

# Taken from:
# http://www.niteoweb.com/blog/setuptools-run-custom-code-during-install
def config_file(command_subclass):
  """A decorator for classes subclassing one of the setuptools commands.

  It modifies the run() method so that the paths in CONFIG_FILE are correctly 
  set
  """
  orig_run = command_subclass.run

  def modified_run(self):
    import ConfigParser
    config = ConfigParser.ConfigParser()
    with open(CONFIG_FILE) as fp:
      config.readfp(fp)
    config.set('project', 'base_dir', here)
    config.set('project', 'db', here + '/data')
    config.set('project', 'pictures', here + '/data/pictures')
    config.set('project', 'documentation', here + '/doc')
    config.set('project', 'source_code', here + '/biflorica-recorder')
    connection_string = 'postgresql+psycopg2://{0}:{1}@localhost/{2}'\
      .format(
        config.get('db', 'user'), config.get('db', 'password'),
        config.get('db', 'name')
      )
    config.set('db', 'url', connection_string)
    with open(CONFIG_FILE, 'wb') as configfile:
      config.write(configfile)
    orig_run(self)
  
  command_subclass.run = modified_run
  return command_subclass

@config_file
class CustomDevelopCommand(develop):
  pass

@config_file
class CustomInstallCommand(install):
  pass

setup(
  name='biflorica-recorder', 
  version='0.0.1', 
  description='Biflorica trading data recorder',
  long_description=README,
  classifiers=[
    "Programming Language :: Python",
    "Topic :: Database :: Database Engines/Servers",
    "Topic :: Internet :: WWW/HTTP :: Indexing/Search"
  ],
  author='Néstor Bohórquez',
  author_email='tca7410nb@gmail.com',
  url='',
  keywords='Biflorica trading data record',
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  test_suite='biflorica-recorder',
  install_requires=requires,
  cmdclass={
    'install': CustomInstallCommand,
    'develop': CustomDevelopCommand
  },
  entry_points={
    'console_scripts': [
      'setup = biflorica-recorder.scripts.setup:main',
      'record = biflorica-recorder.scripts.record:main'
    ],
  }
)
