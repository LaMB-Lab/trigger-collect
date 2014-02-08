# trigger-collect.py

A Python script for aggregating times from several trigger channels such that the binary representation of a byte-sized trigger is represented across the input channels. Currently hard-coded to work only with 8 bit triggers. Primarly for use to fake multiple-channel trigger epochs in MEG160.

## Author Information
_Author:_ Matthew A. Tucker
_Affiliations:_ NYUAD Department of Psychology; Language, Mind, and Brain Laboratory; Neurolinguistics of Language Laboratory (Abu Dhabi)
_Email:_ matt.tucker@nyu.edu

## Usage

`% python trigger-collect.py outfile includes excludes file1 file2 file3 file4 file5 file6 file7 file8`

### Required Arguments

* `outfile` - the name of the output file to create (or overwrite)
* `includes` - the name of a file containing the list of files1-8 to include (i.e., the files whose channels are set for the trigger in question)
* `excludes` - the name of a file containing the list of files1-8 to exclude (i.e., the files whose channels are cleared for the trigger in question)
* `file1` - the name of a file containing the trigger times for the least significant (i.e., lowest-numbered) trigger channel
* `file2` - `file7` - the name of a file containing the trigger times for the next trigger channels, from lowest- to highest-numbered.
* `file8` - the name of a file containing the trigger times for the most significant (i.e., highest-numbered) trigger channel

### Usage Comments

`trigger-collect.py` takes a sequential list of files, `file1` through `file8` which contain a list of times for triggers sent on these channels. It expects that `file1` represents the least significant bit and `file8` the most significant bit. It also assumes that the times on these files are syncrhonous; `trigger-collect.py` will not operate sensibly if there is any asynchrony.

The goal of `trigger-collect.py` is to create a file, `outfile`, which contains only the times which overlap in the subset of `file1`-`file8` specified in `includes` and which do not appear in `excludes`. Therefore, `includes` should be a list of the files which have their associated channels set and `excludes` should be a list of the files which have their associated channels cleared. `outfile` will then be created and can be re-imported into MEG160 to fool MEG160 into thinking the multiple channels are in fact a single, 8-bit channel.

### Example Usage

In Abu Dhabi, the trigger channels are 224-231, meaning that `file1` through `file8` are usually `224.txt` through `231.txt`. An example of use is then:

```
% python trigger-collect.py 12-epochs.txt 12-incls.txt 12-excls.txt 224.txt 225.txt 226.txt 227.txt 228.txt 229.txt 230.txt 231.txt`

Including the following files:
226-2.txt
227-2.txt
Excluding the following files:
224-2.txt
225-2.txt
228-2.txt
229-2.txt
230-2.txt
231-2.txt
This should be trigger number 12.
If you don't agree, then something is wrong, and no guarantees are made on the output's integrity.
Done.
```

## Revision History

* 8-2-2014: Initial commit