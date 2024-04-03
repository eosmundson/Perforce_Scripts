# Note: this script doesn't actually obliterate file revisions yet.
# It is for testing of #verification and finding files with "MISSING!" revisions.
# The user would then be asked if they want the file obliterated.
# An additional prompt to actually obliterate files and additional statements would need to be added.
# 
# An even better idea is to store all missing file revisions in a list and then prompt the user for obliteration
# then iterate through the list all at once to reduce repetitive user interaction.
#
# The script takes an argument for verification, such as 
# $ python ./p4_obliterate_missing.py //depot/path/to/file

import sys
import os
from P4 import P4, P4Exception

p4 = P4()

# Set p4 environment variables
p4.port = os.environ['P4PORT']
p4.user = os.environ['P4USER']
#p4.client = "client-eosmundson"

def main():
    try:
        # Connect to p4 server
        p4.connect()
        
        # Run p4 verify command and get the number of file results that are stored as dicts in a list
        verified = p4.run("verify", sys.argv[1])
        res = len([ele for ele in verified if isinstance(ele, dict)])
        
        # Call function to verify Perforce file revisions
        verify_files(res, verified)
    
    # Catch and print any P4 exceptions that are raised.
    except P4Exception:
        for e in p4.errors:
            print(e)

    finally:
        p4.disconnect()


# Function to verify P4 file revisions
def verify_files(res, verified):
    # Set counter to zero as that will determine which verified file dictionary is being iterated through    
    count = 0
    while count < int(res):
        if verified[count].get("status") == None:
            print("Revision" , verified[count]["depotFile"] + "#" + verified[count]["rev"], "is fine.", sep=" ")
            count += 1
            continue
        # If the file is missing, store the file and revision in a string and prompt user to obliterate the file. If user enters "yes" to obliterate, then run "p4 obliterate" command.
        if verified[count]["status"] == "MISSING!":
            print("Found a missing revision")
            problem_file = str(verified[count]["depotFile"] + "#" + verified[count]["rev"])
            print(problem_file)
            answer = input("Do you want to obliterate the missing revision: yes or no? ")
            if answer == "yes":
                p4.run_obliterate(problem_file)
                p4.run("verify", problem_file)
                print(problem_file, "obliterated.")
                count += 1
                continue
            else:
                print(problem_file, "not obliterated.")
                count += 1
                continue
        if count == res:
            break


if __name__ == "__main__":
    main()