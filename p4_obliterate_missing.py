#!/usr/bin/python3

'''
This script is designed to look for missing file revisions in the desired depot path. The path can be set after the script name. The depot path will be searched and any file revision status that is 'MISSING!' will be placed into a list for review and subsequent obliteration from the depot. Be warned that this action is PERMANENT and will result in the loss of the data.

This script takes an argument for the depot path, such as:
$ ./p4_obliterate_missing.py //depot/path/to/file

Make sure to make the script executable before running.
'''
import sys
import os
import re
from P4 import P4, P4Exception

p4 = P4()

try:
    # Set p4 environment variables
    p4.port = os.environ['P4PORT']
    p4.user = os.environ['P4USER']
    #p4.client = "client-eosmundson"

    # Connect to p4 server
    p4.connect()
    # Run p4 verify command and get the number of file results that are stored as dicts in a list
    verified = p4.run("verify", sys.argv[1])
    res = len([ele for ele in verified if isinstance(ele, dict)])

    # Set "counter" to zero as that will determine which verified file dictionary is being iterated through
    # Set "missing" variable to keep track of whether or not any missing revisions have been found.

    count = 0
    missing = False
    missing_files = []
    while count < int(res):
        if verified[count].get("status") == None:
            count += 1
            continue
        # If the file is missing, store the file and revision in a string and prompt user to obliterate the file. If user enters "yes" to obliterate, then run "p4 obliterate" command.
        if verified[count]["status"] == "MISSING!":
            if missing == False: print("Found at least one missing revision.\n")
            missing = True
            problem_file = str(verified[count]["depotFile"] + "#" + verified[count]["rev"])
            # print(problem_file)
            missing_files.append(problem_file)
            count += 1
            continue
            #answer = input("Do you want to obliterate the missing revision: yes or no? ")
            #if answer == "yes" or "y":
            #    p4.run_obliterate(problem_file)
            #    p4.run("verify", problem_file)
            #    print(problem_file, "obliterated.")
            #    count += 1
            #    continue
            #else:
            #    print(problem_file, "not obliterated.")
            #    count += 1
            #    continue

    # if no missing file revisions have been found print a message to let the user know.
    if missing == False:
        sys.exit("No missing file revisions were found.")

    # Preview a list of files and their revision numbers to be obliterated.
    view_missing = input("Do you want to see a list of missing files? Y/N: ").lower()
    if view_missing == "yes" or view_missing == "y":
        print()
        for file in missing_files:
            print(f"{file}")
            continue
        print()

    else:
        pass

    # Obliterate missing file revisions
    oblit_missing = input("Are you ready to obliterate missing file revisions? Y/N: ").lower()
    if oblit_missing == "yes" or oblit_missing == "y":
        for file in missing_files:
            p4.run_obliterate("-y", "-a", file)
            # p4.run("verify", file)
            continue
        
        print("\nFile revisions have been obliterated.")
        
    else:
        print("\n\nWARNING: None of the missing file revisions have been obliterated.\n")

# Catch and print any P4 exceptions that are raised.
except P4Exception:
    for e in p4.errors:
        print(e)

finally:
    p4.disconnect()