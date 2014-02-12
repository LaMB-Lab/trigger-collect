# trigger-collect.py

A Python script for aggregating times from several trigger channels such that the binary representation of a byte-sized trigger is represented across the input channels. Currently hard-coded to work only with 8 bit triggers. Primarly for use to fake multiple-channel trigger epochs in MEG160.

## Author Information
_Author:_ Matthew A. Tucker

_Affiliations:_ NYUAD Department of Psychology; Language, Mind, and Brain Laboratory; Neurolinguistics of Language Laboratory (Abu Dhabi)

_Email:_ matt.tucker@nyu.edu

## Usage

`% python trigger-collect.py input`

### Required Arguments

* `input` - a trigger-collect input file (see below)

### Usage Comments

#### General Usage

`trigger-collect.py` takes a single input file which is specially formatted (see below) which contains a list of files corresponding to events on trigger channels in a binary trigger signal system and a list of decimal trigger codes. `trigger-collect.py` then creates an `output/` directory that contains files for each decimal trigger containing only those times for which the proper channels have events given the binary representation of that trigger. It also creates `triggers-ordered.txt`, a file containing a sequential list of every decimal trigger event sent to the system.

*Note* that `trigger-collect.py` rounds to the nearest tenth of a millisecond (0.0001 seconds) because it assumes that anything more precise is subject to slight asynchronies in the latencies of the DAQ system which records the triggers. This is done because of experience at the NYUAD Neurolinguistics of Language Lab which showed that smaller round-offs created left slight asynchronies in the trigger times. Contact the maintainers if this rounding is too imprecise for your needs.

#### Trigger-Collect Input Formatting

`trigger-collect.py` expects an input file, specified as `input`, which has exactly two lines, formatted as follows:

```
Files: f1 f2 f3 f4 ... f8
Triggers: t1 t2 ... t3 ... tn
```

That is, `trigger-collect.py` expects `input` to have no more than two lines which contain the following infformation:

1. The string `Files: ` followed by a list of up to 8 files separated by spaces. The files should contain a list of trigger event times for the trigger channels, and should be arranged in the order _least significant_-_most significant_. See below for an example from the NYUAD NeLLab trigger box.
2. The string `Triggers: ` followed by a list of any number of decimal triggers separated by spaces.

Deviations from this input file format will lead to errors or bad behavior. Note especially that the trigger channel files must be ordered properly on this list, or the results will be nonsense (but not look like nonsense unless you do the math by hand).

#### Example Usage

In Abu Dhabi, the trigger channels are 224-231, meaning that `f1` through `f8` are usually `224.txt` through `231.txt` in `input`. An example of use is then:

```
% python trigger-collect.py sample-inputs/input.txt
Parsing input file... Done.
Populating trigger times...
...from file: sample-inputs/224.txt
...from file: sample-inputs/225.txt
...from file: sample-inputs/226.txt
...from file: sample-inputs/227.txt
...from file: sample-inputs/228.txt
...from file: sample-inputs/229.txt
...from file: sample-inputs/230.txt
...from file: sample-inputs/231.txt
Done
Getting trigger times now...
Getting times for trigger: 12
Written to file: ./outputs/12-out.txt
Getting times for trigger: 23
Written to file: ./outputs/23-out.txt
Done getting trigger times.
Ordering triggers now... Done.
```

In this example the contents of `input.txt` are:

```
Files: sample-inputs/224.txt sample-inputs/225.txt sample-inputs/226.txt sample-inputs/227.txt sample-inputs/228.txt sample-inputs/229.txt sample-inputs/230.txt sample-inputs/231.txt
Triggers: 12 23
```

These input files are included in the download in the `sample-inputs` folder.

#### Return Codes

* 0 - Success (or presumed success)
* 1 - File IO error
* 2 - Improperly formatted input file
* 3 - Too many trigger channels error
* 4 - Trigger decimal integer overflow
* 5 - Not enough triggers error

## Revision History

* 8-2-2014: Initial commit
* 12-2-2014: v.2.0, which takes only one input file and can do multiple triggers at once.