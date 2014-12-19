from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

version = '0.1'

setup(name='zrunner',
      version=version,
      description="Utilities for running and benchmarking Zonation",
      long_description="""\
""",
      classifiers=[],
      keywords='zonation test cbig',
      author='Joona Lehtom\xc3\xa4ki',
      author_email='joona.lehtomaki@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
                  "pyyaml"
      ],
      dependency_links = ['https://github.com/jlehtoma/slackpy/tarball/master#egg=slackpy-0.1.4'],
      entry_points={'console_scripts': [
                    'zrunner = zrunner.runner:main',
                    'zreader = zrunner.reader:main'
                    ]
                    },
      )
