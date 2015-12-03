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

import os
import subprocess
import shutil


def cpfile(src,dst):
  if os.path.exists(src) and os.path.exists(dst):
   shutil.copy2(src, dst)

def serviceinit(startstop,initpath):
    p = subprocess.Popen(["service", initpath, startstop], stdout=subprocess.PIPE)
    output, err = p.communicate()
    print "Stopping or starting initfile...\n", output

def check_ver():
  if os.path.exists("/etc/init.d/gluu-server24"):
    initpath = "/etc/init.d/gluu-server24"
    dest_dir = "/opt/gluu-server24"
    return initpath
    return dest_dir
  elif os.path.exists("/etc/init.d/gluu-server"): 
    initpath = "/etc/init.d/gluu-server"
    dest_dir = "/opt/gluu-server"
    return initpath
    return dest_dir

#NEED HELP WITH UPDATER VARIABLE
check_ver()
serviceinit("start",initpath)
cpfile("$UPDATER/idp.war", "dest_dir/opt/idp/war/idp.war")
cpfile("$UPDATER/oxcas.war", "dest_dir/opt/dist/oxcas.war")
cpfile("$UPDATER/identity.war", "dest_dir/opt/tomcat/webapps/identity.war")
cpfile("$UPDATER/oxauth.war', 'dest_dir/opt/tomcat/webapps/oxauth.war")
serviceinit("stop",initpath)
