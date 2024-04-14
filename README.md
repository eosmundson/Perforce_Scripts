# Perforce_Scripts
## Scripts to simplify working with a Perforce server for uncommon tasks.

This will include scripts to facilitate user management, replica/edge server creation, dealing with corrupt or missing file revisions, etc.

### p4_obliterate_missing.py
This script searches the given depot path for missing file revisions and gives the user the option of obliterating those revisions.
Usage of the script is expected to be:
$ ./p4_obliterate_missing.py //depot/path/to/file/...

It can take revision numbers and HEAD options at the end of the path as well.
