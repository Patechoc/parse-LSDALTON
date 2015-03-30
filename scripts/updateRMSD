#!/usr/bin/env python 

import subprocess as subproc


## The DbConnector directory is there, but empty.
## You must run two commands: 'git submodule init' to initialize your local configuration file,
## and 'git submodule update' to fetch all the data from that project and check out the appropriate commit listed in your superproject:


cmd = "git submodule init; git submodule update"
out = subproc.check_output(cmd, shell=True)
