from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='ztests',
      version=version,
      description="Testing harness for Zonation outputs",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='zonation test cbig',
      author='Joona Lehtom\xc3\xa4ki',
      author_email='joona.lehtomaki@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            "pyyaml",
            "numpy",
            "scipy",
            "gdal"
      ],
      entry_points={
            'console_scripts': [
                  'zrunner = ztests.runner:main'
            ]
      },
)
