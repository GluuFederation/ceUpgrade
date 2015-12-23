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

#def check_ver():
#    dest_dir = None
#    service_name = None
#    updater_ver = None
#    if os.path.exists("/etc/init.d/gluu-server24"):
#        dest_dir = "/opt/gluu-server24"
#        service_name = "gluu-server24"
#        updater_ver = "gluu-updater24"
#    elif os.path.exists("/etc/init.d/gluu-server"):
#        dest_dir = "/opt/gluu-server"
#        service_name = "gluu-server"
#        updater_ver = "gluu-updater23"
#    else:
#        print "Gluu Server not found. Exiting..."
#        sys.exit(2)
#    return dest_dir, service_name, updater_ver
#
#dest_dir, service_name, updater_ver = check_ver()
#src_dir = "%s/%s/1/dist" % (dest_dir, updater_ver)
#src_dir = "/opt/%s/1/dist" %updater_ver
#serviceinit(service_name, "stop")
#cpfile("%s/idp.war" % src_dir, "%s/opt/idp/war/idp.war" % dest_dir)
#cpfile("%s/oxcas.war" % src_dir, "%s/opt/dist/oxcas.war" % dest_dir)
#cpfile("%s/identity.war" % src_dir, "%s/opt/tomcat/webapps/identity.war" % dest_dir)
#cpfile("%s/oxauth.war" % src_dir, "%s/opt/tomcat/webapps/oxauth.war" % dest_dir)
#cptree("%s/community-edition-setup" % src_dir, "%s/opt/install/" % dest_dir)
#serviceinit(service_name, "start")

src_dir = "/opt/%s/1/dist" %updater_ver
serviceinit("tomcat6", "stop")
cpfile("%s/idp.war" % src_dir, "/opt/idp/war/idp.war")
cpfile("%s/oxcas.war" % src_dir, "/opt/dist/oxcas.war")
cpfile("%s/identity.war" % src_dir, "/opt/tomcat/webapps/identity.war")
cpfile("%s/oxauth.war" % src_dir, "/opt/tomcat/webapps/oxauth.war")
cptree("%s/community-edition-setup" % src_dir, "/opt/install/")
serviceinit("tomcat6", "start")
