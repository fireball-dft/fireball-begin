#!/usr/bin/env python
#
# Program will read in an .eig file generated by BEGIN's looprc function
# and determine which values of the cutoff radius are closest to the
# goal delta, which is the difference between the eigenvalue and the
# eigenvalue for the infinite cutoff radius condition.
#
# Usage: glean_looprc ###.eig

import sys
from optparse import OptionParser

# Parses a string and returns a list of words 
def parseString(s):
    list = []
    temp = ''
    for i in s:
        if i == ' ' or i == '\t' or i == '\n' or i == '\r':
            if temp != '':
                list = list + [temp]
            temp = ''
        elif i != ' ' or i != '\t' or i != '\n' or i != '\r':
            temp = temp + i
    if temp != '':
        list = list + [temp]
    return list

def GleanEig (argv):
    # Parse our arguments
    usage = "usage: %prog [options] ###.eig"
    parser = OptionParser(usage)
    parser.set_defaults(delta='0.15', ignorep=False)
    parser.add_option('-e', dest='delta', metavar='Ryd',
                      help='desired excitation (default is 0.15 Ryd)')
    parser.add_option('--ignorep', dest='ignorep', action='store_true',
                      help='ignore the p shell (good for transition metals)')
    (options, args) = parser.parse_args(argv)
    if len(args) != 2:
        parser.error('incorrect number of arguments')
    delta = float(options.delta)

    f = open(args[1])
    # Ignore the first 5 lines
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()

    # The rest of the lines we want the 3rd, 7th, and 11th values
    # The score is determined by how close the deltas are to delta
    # We put eveything in a dictionary
    scores = []
    associations = {}
    for line in f:
        line = parseString(line)
        if(len(line) == 11) and options.ignorep:
            score = abs(delta - float(line[2]))
            score = score + abs(delta - float(line[10]))
            rcutoffs = [line[0], line[8]]
        if(len(line) == 11) and not options.ignorep:
            score = abs(delta - float(line[2]))
            score = score + abs(delta - float(line[6]))
            score = score + abs(delta - float(line[10]))
            rcutoffs = [line[0], line[4], line[8]]
        elif( len(line) == 8):
            score = abs(delta- float(line[2]))
            score = score + abs(delta - float(line[6]))
            rcutoffs = [line[0], line[4]]
        elif( len(line) == 4):
            score = abs(delta - float(line[2]))
            rcutoffs = line[0]
        scores.append(score)
        if score in associations:
            print 'warning: duplicate scores for:',
            print associations[score],
            print rcutoffs,
            print score
        associations[score] = rcutoffs

    # Close the file
    f.close( )

    # Sort the scores
    scores.sort( )

    # Print out the results
    print
    print 'Printing out the top 10 scoring values for the cutoff radius: '
    for i in range(0, 10):
        print associations[scores[i]],
        print '   Score: ',
        print scores[i]
    print

    # Return the best score
    return associations[scores[0]]


# Call glean on the file
if __name__ == "__main__":
    GleanEig(sys.argv)
