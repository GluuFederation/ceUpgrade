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

if os.path.exists(/etc/init.d/gluu-server24): 
  subprocess.call(["service", "gluu-server24", "stop"])
  p = subprocess.Popen(["service", "gluu-server24", "stop"], stdout=subprocess.PIPE)
  output, err = p.communicate()
  print "Beggining of the upgrade process, Stopping gluu-server...\n", output
elif os.path.exists(/etc/init.d/gluu-server): 
  subprocess.call(["service", "gluu-server", "stop"])
  p = subprocess.Popen(["service", "gluu-server", "stop"], stdout=subprocess.PIPE)
  output, err = p.communicate()
  print "Beggining of the upgrade process, Stopping gluu-server...\n", output

print "Upgrading the files..."

dest_dir_ls = os.listdir("/opt")
dest_dir = ""

for dir in dest_dir_ls:
  if dir.index("gluu")>=0:
    dest_dir = dir

#NOT SURE HOW TO DO THAT UPDATER="/opt/CHANGEME/opt/CHANGEME-updater/$VER/dist"
if os.path.exists(UPDATER/idp.war) and os.path.exists(DEST_DIR/opt/idp/war):
  shutil.copy2('$UPDATER/idp.war', 'dest_dir/opt/idp/war/idp.war')
if os.path.exists(UPDATER/idp.war) and os.path.exists(DEST_DIR/opt/dist):
  shutil.copy2('$UPDATER/oxcas.war', 'dest_dir/opt/dist/oxcas.war')
if os.path.exists(UPDATER/identity.war) and os.path.exists(DEST_DIR/opt/tomcat/webapps):
  shutil.copy2('$UPDATER/identity.war', 'dest_dir/opt/tomcat/webapps/identity.war')
if os.path.exists(UPDATER/oxauth.war) and os.path.exists(DEST_DIR/opt/tomcat/webapps):
  shutil.copy2('$UPDATER/oxauth.war', 'dest_dir/opt/tomcat/webapps/oxauth.war')

if os.path.exists(/etc/init.d/gluu-server24): 
  subprocess.call(["service", "gluu-server24", "start"])
  p = subprocess.Popen(["service", "gluu-server24", "start"], stdout=subprocess.PIPE)
  output, err = p.communicate()
  print "Files updated, Starting gluu-server...\n", output
elif os.path.exists(/etc/init.d/gluu-server): 
  subprocess.call(["service", "gluu-server", "start"])
  p = subprocess.Popen(["service", "gluu-server", "start"], stdout=subprocess.PIPE)
  output, err = p.communicate()
  print "Files updated, Starting gluu-server...\n", output

print "Upgrade process ends successfully."
