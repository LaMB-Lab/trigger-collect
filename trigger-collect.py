#########################################
# trigger-collect.py                    #
# Author: Matthew A. Tucker             #
# NYUAD Language, Mind, and Brain Lab   #
# Email: matt.tucker@nyu.edu            #
# Revision 2.0/ 12 February 2014        #
#########################################

################### RETURN CODES #####################
# 0 - Success (or presumed success)
# 1 - File IO error
# 2 - Improperly formatted input file
# 3 - Too many trigger channels error
# 4 - Trigger decimal integer overflow
# 5 - Not enough triggers error

import argparse
import sys
import os

def compute_triggers(epochs, trigger, byte_representation):
    """Compute a list of times which correspond to trigger given byte_representation and epochs."""
    
    includes = []           #lists from epochs to include in this trigger
    excludes = []           #lists from epochs to exclude from this trigger
    
    # we only want to use the lists from byes which are set
    for i in range(0, len(byte_representation)):
        if byte_representation[i] == "1":
            includes.append(epochs[i])
        else:
            excludes.append(epochs[i]) # and we need to remove those from bytes which are not set.
    
    #get the union of the includes
    includes = list(set.intersection(*map(set, includes)))
    
    #and take the complement of the excludes in the includes
    excludes = sum(excludes,[])
    ret_val = [x for x in includes if x not in excludes]
    
    #return this new list of epochs sorted.
    return sorted(ret_val)

def get_and_write_trigger_for_time(epochs, outfile):
    """Compute the trigger number for all times given the input set epochs and output outfile."""
    
    # flatten the epochs
    flattened_epochs = [item for sublist in epochs for item in sublist]
    # get a sorted list of unique times in the resulting list
    epochs_sorted = sorted(list(set(flattened_epochs)))
    
    for t in epochs_sorted:
        #we'll sequentially build a byte reprensetation of the triggers we find and store them here.
        byte_representation = ""
        
        for i in range(0,len(epochs)):      #loop over each channel and set the bit if t is in this channel
            if t in epochs[i]:
                byte_representation = "1" + byte_representation
            else:
                byte_representation = "0" + byte_representation
            
        outfile.write(str(int(byte_representation,2)) + "\n") #write the decimal version of the byte to disk

def main():
    """Main entry point for trigger-collect.py. """
    
    ## ------ argument setups ------
    
    #initialize the argument parser
    parser = argparse.ArgumentParser(description='A script for collecting trigger files from MEG160 in order to find trigger times which appear in all the files. See https://github.com/LaMB-Lab/trigger-collect for documentation.') 
    parser.add_argument("input", help="a trigger-collect input file (see documentation for formatting)", type=file)
    
    #parse the arguments and throw a nice error message if one isn't a real file
    try:
        args = parser.parse_args() # parse the arguments
    except IOError as e:
        print "There was an input problem: {0}".format(e.strerror) + "."
        print "Probably, there is no file named " + format(e.filename) + "; you should make sure it exists."
        return 1
        
    ## ----- basic variable definitions -----
    #do some basic i/o setup
    infile = args.input                                         #the name of the input file

    channel_files = []                                          #the channel files being used
    triggers = []                                               #the triggers being used
    
    ## ------ parse the input file -----
    print("Parsing input file..."),
    line_no = 1
    for l in infile:
        if line_no == 1:
            channel_files = l.split()[1:]                       #read in the trigger channels
        else:
            if line_no == 2:
                triggers = l.split()[1:]                        #read in the triggers used in this experiment
            else:
                print "There are too many lines in the input file. There should be only two."
                print "Files: l1 l2 ... (a list of channel files)"
                print "Triggers: t1 t2 ... (a list of triggers)"
                return 2
        line_no += 1
    
    infile.close()
        
        
    ## ------ some consistency checking on the input file's contents -----
    # we only support up to 8-bit triggers, so there'd better not be more than 8 channels.
    if len(channel_files) > 8:
        print "There are too many channel files listed. trigger-collect only supports up to 8-but triggers. Please write the maintainer if you need support for more."
        return 3
    
    if len(triggers) < 1:
        print "Well, you probably want to collect at least one trigger, right?"
        print "Make sure the Triggers: line contains at least one integer."
        return 5
    
    # we only support 8-bit triggers, which we assume are unsigned.
    for t in triggers:
        try:
            if int(t) > 255 or int(t) < 0:
                print "One of your triggers is wrong: " + str(t)
                print "We only support 8-bit triggers which are unsigned. So you must have 0 < t < 255 for every trigger."
                return 4
        except ValueError as e:
            print "One of your triggers isn't a number: " + e.args[0]
            return 4
            
    print("Done.")
            
    ## ------ populate the list of lists of epoch times ------
    
    print("Populating trigger times...")
    
    channel_trigger_epochs = [[] for i in range(0, len(channel_files))]                #array to hold the list of trigger times for each channel
    
    for channel in channel_files:
        try:
            f_channel = open(channel, 'r')
        except IOError as e:
            print "There was an input problem: {0}".format(e.strerror) + "."
            print "Probably, there is no file named " + format(e.filename) + "; you should make sure it exists."
            return 1
        
        print("...from file: " + channel)
        
        # populate each member of the channel list from LSB to HSB - we round because computers aren't accurate to 0.01 milliseconds
        for l in f_channel:
            channel_trigger_epochs[channel_files.index(channel)].append(round(float(l.strip()),1))
            
    print("Done")
    
    ## ------ iterate over each trigger and get the times that that trigger fired during ------
    print("Getting trigger times now...")
    
    for trigger in triggers:
        print("Getting times for trigger: ") + trigger
        
        byte_trigger = str(bin(int(trigger))[2:])                    # convert the trigger to a binary representation without the leading 0b and then cast to a string, because we'll loop over each bit later on.
        
        # we assume that higher bits are zero for low numbers
        while(len(byte_trigger) < len(channel_files)):
            byte_trigger = "0" + byte_trigger
        
        # reverse the byte string because we'll want to work from LSB to HSB.
        byte_trigger = byte_trigger[::-1]    

        trigger_epochs = compute_triggers(channel_trigger_epochs, trigger, byte_trigger)    #get the trigger times that correspond to this trigger
        
        ## write this trigger to an output file in the outputs directory
        # check to see if the outputs directory exists and create if need be
        if not os.path.isdir("./outputs"):
            os.makedirs("./outputs")
        
        # set up the output file name for this trigger
        out_file_name = "./outputs/" + trigger + "-out.txt"
            
        #open a file and write the output to disk.
        f_out = open(out_file_name, 'w')

        for i in trigger_epochs:
            f_out.write(str(i) + "\n")
    
        #file maintenence.
        f_out.close()
        
        print("Written to file: " + out_file_name)
    
    print("Done getting trigger times.")
    print("Ordering triggers now..."),
        
    ## ------ create an ordered list of each trigger event -----
    #we'll write the triggers in order to this file
    out_file_name = "./outputs/triggers-ordered.txt"
    f_out = open(out_file_name, 'w')
    
    #actually get the trigger list and write them to disk in the order they appear
    get_and_write_trigger_for_time(channel_trigger_epochs, f_out)
    
    f_out.close()
    
    print("Done.")
            
    return 0
    

main()