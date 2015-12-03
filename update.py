#!/usr/bin/python
# The MIT License (MIT)
#
# Copyright (c) 2014 Gluu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, subprocess, shutil, sys

def cpfile(src, dst):
  if os.path.exists(src) and os.path.exists(dst):
      shutil.copy2(src, dst)

def serviceinit(startstop, initpath):
    cmd = ["service", initpath, startstop]
    p = subprocess.Popen(["service", initpath, startstop], stdout=subprocess.PIPE)
    output, err = p.communicate()
    if err:
        print "Error running %s" % " ".join(cmd)
        print err
        sys.exit(1)
    print output

def check_ver():
    initpath = None
    dest_dir = None
    if os.path.exists("/etc/init.d/gluu-server24"):
        initpath = "/etc/init.d/gluu-server24"
        dest_dir = "/opt/gluu-server24"
    elif os.path.exists("/etc/init.d/gluu-server"):
        initpath = "/etc/init.d/gluu-server"
        dest_dir = "/opt/gluu-server"
    if (initpath==None) | (dest_dir==None):
        print "Init file or gluu-server folder not found. Exiting..."
        sys.exit(2)
    return initpath, dest_dir

#NEED HELP WITH UPDATER VARIABLE
initpath, dest_dir = check_ver()
serviceinit("stop", initpath.split("/")[-1])
cpfile("%s/idp.war" % initpath, "%s/opt/idp/war/idp.war" % dest_dir)
cpfile("%s/oxcas.war" % initpath, "%s/opt/dist/oxcas.war" % dest_dir)
cpfile("%s/identity.war" % initpath, "%s/opt/tomcat/webapps/identity.war" % dest_dir)
cpfile("%s/oxauth.war" % initpath, "%s/opt/tomcat/webapps/oxauth.war" % dest_dir)
serviceinit("start", initpath.split("/")[-1])
