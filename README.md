## zrunner 
#### platfrom independent wrapper for running and benchmarking Zonation

[Zonation](http://cbig.it.helsinki.fi/software/zonation/) conservation 
prioritization software can be run using both a GUI and command line interface. 
Often when running analyses runs in batch, repeating runs, or running the 
analysis in headless environments (such as Linux  servers/computational units) 
it is useful to use Zonation's command line interface instead of the GUI. One 
way to build these CLI scripts is to use 
[batch files](http://en.wikipedia.org/wiki/Batch_file) - or bat-files - as 
suggested in the Zonation manual. Bat-files are also the foundation of Zonation
"projects" as they define the necessary configuration files and parameters
for a particular run.

However, bat-files cannot be used on other platforms such as Linux. **zrunner**
solves this problem by providing simple wrapper utilities for running Zonation
bat-files independent of the platform. Furthermore, the package records 
additional information such as system information and time used for each run and
outputs the information in a simple [YAML](http://yaml.org/)-file. In a 
nutshell, zrunner is meant for:

1. Running Zonation runs in a platform independent way
2. Providing additional information on the run (Was the run successful? How long 
did the different stages take? What's the system configuration?)
3. Benchmarking Zonation on different hardware/software/OS configurations

zrunner package includes two command line utilities:

1. `zrunner` for running the Zonation-files and generating records of the run 
1. `zreader` for reporting the results produced by `zrunner`

## Install

#### Dependencies

* Python 2.7+ (may work with older version as well, untested)
* [pip](http://www.pip-installer.org/en/latest/) (needed only if installing using pip).
* [PyYAML](http://pyyaml.org/). NOTE: pip/setuptools will try to install this as 
well so this stage is optional. On some platforms `libyaml-dev` or similar is needed.

#### Using pip

1. Install `zrunner` directly from [GitHub](https://github.com/cbig/zrunner) 
using the following command (may need administrative privileges):  

```
pip install https://github.com/cbig/zrunner/archive/master.zip
```

#### Using git

1. Clone the repository:
```
git clone https://github.com/cbig/zrunner.git
```
2. In the package folder, install the `zrunner` with the following command:

```
python setup.py install
```

#### Using bootstrapped setuptools

This option is not very well tested. 

1. Download the package from https://github.com/cbig/zrunner/archive/master.zip
2. Unzip the folder
3. In the package folder, install the `zrunner` with the following command:

```
python setup.py install
```

## Quick usage
