import argparse
import sys

#initialize the argument parser
parser = argparse.ArgumentParser(description='A script for collecting trigger files from MEG160 in order to find trigger times which appear in all the files.') 
parser.add_argument("outfile", help="a name for the output file")
parser.add_argument("includes", help="a list of files to include in the output file", type=file)
parser.add_argument("excludes", help="a list of files to exclude from the output file", type=file)
parser.add_argument("files", nargs=8, help="a list of trigger files", type=file)


#parse the arguments and throw a nice error message if one isn't a real file
try:
    args = parser.parse_args() # parse the arguments
except IOError as e:
    print "There was an input problem: {0}".format(e.strerror) + "."
    print "Probably, there is no file named " + format(e.filename) + "; you should make sure it exists."
    sys.exit()
    

#do some basic i/o setup
outfile = args.outfile      #the name of the output file
infiles = args.files        #the name of the input files
includes = args.includes    #a file containing the file names to include
excludes = args.excludes    #a file containing the file names to exclude
theFiles = []               #array to hold input file names
theNotFiles = []            #array to hold exclude file names

#get the include file names as an list -- I don't know why it doesn't work without this at present.
for l in includes:
    theFiles.append(l.strip())

includes.close()

print("Including the following files:") #helpful output

for l in theFiles:
    print l

# we need a multidimensional list to store one list for each file containing the epochs
accumulator = [[] for i in range(len(theFiles))]

#we need a count of which file we're in, zero-indexed, to get into the right row on the accumulator
fileCount = 0

#loop over each include file and add all the epochs to the apporpriate dimension in the list
for f in theFiles:
    try:
        file = open(f, "r")
        
        #actually write the epoch to the list
        for l in file:
            accumulator[fileCount].append(float(l.strip()))
        
        #file and loop maintenence
        file.close()
        fileCount += 1
        
    except IOError as e:
        print "There was an input problem: {0}".format(e.strerror) + "."
        print "Probably, there is no file named " + format(e.filename) + " or it could not be opened successfully."
        sys.exit()
        
#we're only interested in epochs that appear in all three files, so we take the intersection of the sub-lists in accumulator        
output = list(set.intersection(*map(set, accumulator)))      

#get the exclude files into a list -- I don't know why it doesn't work without this.
for l in excludes:
    theNotFiles.append(l.strip())

excludes.close()

print("Excluding the following files:") #more helpful output

for l in theNotFiles:
    print l
    
    
#check that the user agrees that this is the correct trigger number
binTrigger = ""
for f in infiles:
    if getattr(f,"name") in theFiles:
        binTrigger = "1" + binTrigger
    else:
        binTrigger = "0" + binTrigger

print "This should be trigger number " + str(int(binTrigger,2)) + "."
print "If you don't agree, then something is wrong, and no guarantees are made on the output's integrity."

#reset the accumulator for holding epochs in the excluded files
accumulator = [[] for i in range(len(theNotFiles))]
#reset the file count
fileCount = 0

#loop over the excluded files, adding all contained epochs to the accumulator
for f in theNotFiles:
    try:
        file = open(f, "r")
        
        for l in file:
            accumulator[fileCount].append(float(l.strip()))
            
        #file and loop maintenence
        file.close()
        fileCount += 1
            
    except IOError as e:
        print "There was an input problem: {0}".format(e.strerror) + "."
        print "Probably, there is no file named " + format(e.filename) + " or it could not be opened successfully."
        sys.exit()
            
#we're about to take the complement of the accumulator in output, so we need to flatten accumulator
accumulator = sum(accumulator,[])

#this is where the magic happens -- remove all the epochs in accumulator from the list in output.
epochs = [x for x in output if x not in accumulator]

epochs = sorted(epochs)

#open a file and write the output to disk.
fileOut = open(outfile, 'w')

for i in epochs:
    fileOut.write(str(i) + "\n")
    
#file maintenence.
fileOut.close()

print "Done."