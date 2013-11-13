### zrunner - platfrom independent wrapper for running and benchmarking Zonation

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

However, bat-files cannot be used on *nix platforms such as Linux. **zrunner**
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

### Install

### Quick usage