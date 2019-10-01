import json
from pprint import pprint
from optparse import OptionParser
import os, sys

failedserverlsit = []

def failedServer(hostname):
    failedserverlsit.append(hostname)

def displayFailedServer():
    print("The following servers failed")
    for x in range(len(failedserverlsit)): 
        print failedserverlsit[x]

def getCmdLine():
    """Sets up OptParse to fetch cmd line options and
    returns the (options, args) tuple"""
    usage = "accparse.py -f <filename> -o <opperation> -s <searchstring>"
    parser = OptionParser(usage)
    parser.add_option("-f", "--filename", help="JSAON output file")
    parser.add_option("-o", "--opperation", help="host = search by host, account = search by account")
    parser.add_option("-s", "--searchstring", help="The Hostname or PowerBroker Account you want to find")
    return parser.parse_args()

if __name__ == '__main__':
    print "Gathering cmd line options"
    (options, args) = getCmdLine()
    if options.filename is None:
        print "Error: No input file supplied"
        sys.exit()
    inputfile = options.filename
    if options.opperation is None:
        print "Error: No opperation supplied"
        sys.exit()
    opperation = options.opperation
    if options.searchstring is None:
        print "Error: No search string supplied"
        sys.exit()
    searchstring = options.searchstring

    print ("Searching " + inputfile + " for " + searchstring + " by " + opperation)

    with open(inputfile) as json_file:
        data = json.load(json_file)
        if "host" in opperation:
            for p in data['items']:
                if searchstring in p['node']:
                    if "failure" in p['status']:
                        failedServer(p['node'])
                    else:    
                        data2 = json.dumps(p['result'])  
                        data3 = json.loads(data2)
                        for key, value in data3.items():
                            mylist = value.split(",")
                            for x in range(len(mylist)): 
                                print mylist[x] + "\n", 
        elif 'account'in opperation:
            for p in data['items']:
                if "failure" in p['status']:
                    failedServer(p['node'])
                else:                
                    data2 = json.dumps(p['result'])  
                    data3 = json.loads(data2) 
                    for key, value in data3.items():
                        mylist = value.split(",")
                        if searchstring in mylist:
                            print(p['node'])
        displayFailedServer()
