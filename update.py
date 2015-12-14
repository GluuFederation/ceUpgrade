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

def cpdir(src, dst):
  if os.path.exists(src) and os.path.exists(dst):
      shutil.copytree(src, dst)

def serviceinit(servicename, action):
    cmd = ["service", servicename, action]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, err = p.communicate()
    if err:
        print "Error running %s" % " ".join(cmd)
        print err
        sys.exit(1)
    print output

def changeown(warfile):
    shutil.chown(warfile, user=tomcat, group=tomcat)

src_dir = "/opt/%s/1/dist" %updater_ver
serviceinit("tomcat6", "stop")
cpfile("%s/idp.war" % src_dir, "/opt/idp/war/idp.war")
cpfile("%s/oxcas.war" % src_dir, "/opt/dist/oxcas.war")
cpfile("%s/identity.war" % src_dir, "/opt/tomcat/webapps/identity.war")
cpfile("%s/oxauth.war" % src_dir, "/opt/tomcat/webapps/oxauth.war")
cptree("%s/community-edition-setup" % src_dir, "/opt/install/")
changeown("/opt/idp/war/idp.war")
changeown("/opt/dist/oxcas.war")
changeown("/opt/tomcat/webapps/identity.war")
changeown("/opt/tomcat/webapps/oxauth.war")
serviceinit("tomcat6", "start")
