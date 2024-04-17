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

def main():
    try:
        # Set p4 environment variables
        p4.port = os.environ['P4PORT']
        p4.user = os.environ['P4USER']
        

        # Connect to p4 server
        p4.connect()
        
        # Check command-line argument for provided depot path. Set a default P4 depot path to search if one is not provided in the command.
        if len(sys.argv) == 1:
            depot_path = '//depot/...'
        elif m := re.search(r'\d+$', sys.argv[1]):
            if m:
                depot_path = sys.argv[1]
        else:
            depot_path = sys.argv[1]
            
        print(f"Looking for librarian errors here:\n{depot_path}")
                
        # Run p4 verify command and get the number of file results that are stored as dicts in a list.
        verified = p4.run("verify", depot_path)
        res = len([ele for ele in verified if isinstance(ele, dict)])

        # Set "counter" to zero as that will determine which verified file dictionary is being iterated on.
        # Create boolean "missing" to keep track of whether or not any missing revisions have been found. If not then the program will exit after 'p4 verify' completes. Boolean value will start as 'False'.

        counter = 0
        missing = False
        missing_files = []
        while counter < int(res):
            if verified[counter].get("status") == None:
                counter += 1
                continue
            # If the file is missing, store the file and revision as a string in the 'missing_files' list.
            if verified[counter]["status"] == "MISSING!":
                # The first time a missing revision is found, script will print a notification.
                if missing == False: print("Found at least one missing revision.\n")
                # Since a missing revision has been found, change boolean value to 'True'.
                missing = True
                # Concatenate depotFile name and revision number and store in missing_files list. Increase counter by one and move to next file in verified list
                problem_file = str(verified[counter]["depotFile"] + "#" + verified[counter]["rev"])
                missing_files.append(problem_file)
                counter += 1
                continue
                

        # If no missing file revisions have been found print a message to let the user know and exit the script.
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
                continue
            # Print successful obliteration of revisions.
            print("\nFile revisions have been obliterated.")
            
        else:
            print("\n\nWARNING: None of the missing file revisions have been obliterated.\n")

    # Catch and print any P4 exceptions that are raised.
    except P4Exception:
        for e in p4.errors:
            print(e)

    finally:
        p4.disconnect()

if __name__ == "__main__":
    main()