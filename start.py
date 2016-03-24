#!/usr/bin/python

import os
import sys
import shutil

def main(args):
    if len(args) != 2:
        print "Usage: start.py TEAMNAME"
        sys.exit(1)

    teamname = args[1].lower()

    src = 'bbagent_template.py'
    files = ['bb', 'budget']

    
    for f in files:
        dst = "%s%s.py" % (teamname, f)
        print "Copying %s to %s..." % (src, dst)
        shutil.copyfile(src, dst)

    print "All done.  Code away!"

if __name__ == "__main__":
    main(sys.argv)
