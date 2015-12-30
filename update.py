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

import os, shutil, sys, time, hashlib, traceback

version = "2.4.1"
#base_dir = "."
base_dir = "/var/lib/gluu-update/%s" % version
src_dir = "%s/dist" % base_dir
bu_folder = "%s/bu" % base_dir
log_folder = "%s/log" % base_dir
log = "%s/update.log" % log_folder
logError = "%s/update.error" % log_folder

find = "/usr/bin/find"
mkdir = "/bin/mkdir"
unzip = "/usr/bin/unzip"
chown = "/bin/chown"
cp = "/bin/cp"

tomcatFolder = "/opt/apache-tomcat-7.0.55"
idpFolder = "%s/webapps/idp" % tomcatFolder
oxauthFolder = "%s/webapps/oxauth" % tomcatFolder
identityFolder = "%s/webapps/identity" % tomcatFolder
setupFolder = "/install/community-edition-setup"

def logIt(msg, errorLog=False):
    if errorLog:
        f = open(logError, 'a')
        f.write('%s %s\n' % (time.strftime('%X %x'), msg))
        f.close()
    f = open(log, 'a')
    f.write('%s %s\n' % (time.strftime('%X %x'), msg))
    f.close()

def backupCustomizations(war):
    base = war.split(".")[0]
    modified_dir = "%s/webapps/%s" % (tomcatFolder, base)
    original_dir = "/tmp/%s" % base
    bu_folder = "%s/%s" % (bu_folder, base)
    if not os.path.exists(bu_folder):
        os.mkdir(bu_folder)
    if not os.path.exists(original_dir):
        os.mkdir(original_dir)
    output = getOutput([unzip, "%s/webapps/%s" % (tomcatFolder, war), '-d', original_dir])
    files = getOutput([find, modified_dir], True)
    for modified_file in files:
        modified_file = modified_file.strip()
        original_file = modified_file.replace(modified_dir, original_dir)
        if not os.path.isdir(modified_file):
            if not os.path.exists(original_file):
                logIt("Found new file: %s" % modified_file)
                copyFileWithParentDir(modified_file, bu_folder)
            else:
                modified_hash = hash_file(modified_file)
                original_hash = hash_file(original_file)
                if not modified_hash == original_hash:
                    logIt("Found changed file: %s" % modified_file)
                    copyFileWithParentDir(modified_file, bu_folder)
    shutil.rmtree(original_dir)

# This copy method maintains the parent folder.
def copyFileWithParentDir(fn, dir):
    parent_Dir = os.path.split(fn)[0]
    bu_dir = "%s/%s" % (bu_folder, parent_Dir[1:])
    if not os.path.exists(bu_dir):
        output = getOutput([mkdir, "-p", bu_dir])
    bu_fn = os.path.join(bu_dir, os.path.split(fn)[-1])
    shutil.copyfile(fn, bu_fn)
    logIt("Copied %s to %s" % (fn, bu_dir))

def hash_file(filename):
    # From http://www.programiz.com/python-programming/examples/hash-file
    h = hashlib.sha1()
    with open(filename,'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()

def getOutput(args, return_list=False):
        try:
            logIt("Running command : %s" % " ".join(args))
            output = None
            if return_list:
                output = os.popen(" ".join(args)).readlines()
                logIt("\n".join(output))
            else:
                output = os.popen(" ".join(args)).read().strip()
                logIt(output)
            return output
        except:
            logIt("Error running command : %s" % " ".join(args), True)
            logIt(traceback.format_exc(), True)
            sys.exit(1)

def walk_function(a, dir, files):
    for file in files:
        fn = "%s/%s" % (dir, file)
        targetFn = fn.replace(bu_folder, "/")
        if os.path.isdir(fn):
            if not os.path.exists(targetFn):
                os.mkdir(targetFn)
                logIt("Walk: Creating Folder %s" % targetFn)
        else:
            # It's a file...
            try:
                logIt("Walk: Copying %s" % targetFn)
                shutil.copyfile(fn, targetFn)
            except:
                logIt("Walk: Error copying %s" % targetFn, True)
                logIt(traceback.format_exc(), True)

def restoreCustomizations(dir):
    os.path.walk (dir, walk_function, None)

def updateSetup():
    setupDir = os.path.split(setupFolder)[-1]
    setup_bk_dir = "%s/%s" % (bu_folder, setupDir)

    # Backup current setup
    cpdir(setupFolder, setup_bk_dir)
    rmdir(setupFolder)

    # Install new setup
    new_setup_path = "%s/%s" % (src_dir, setupDir)
    cpdir(new_setup_path, setupFolder)

def cpfile(src, dst):
    getOutput([cp, src, dst])

def cpdir(src, dst):
  if os.path.exists(src):
      shutil.copytree(src, dst)
      logIt("Copied folder %s to %s" % (src, dst))

def rmdir(src):
    try:
        if os.path.exists(src):
            shutil.rmtree(src)
            logIt("Removed folder %s" % src)
    except:
        logIt("Error removing folder %s" % src, True)
        logIt(traceback.format_exc(), True)

def serviceinit(servicename, action):
    cmd = ["service", servicename, action]
    getOutput(cmd)

def changeown(path, owner):
    getOutput([chown, "-R", "%s:%s" % (owner, owner), path])
    logIt("Changing ownership for folder %s to owner %s" % (path, owner))

def copyRenderedTemplate(srcPath, dstPath, substituteDict):
    try:
        logIt("Rendering template %s using dictionary %s" % (srcPath, substituteDict))
        f = open(srcPath)
        try:
            template_text = f.read()
        finally:
            f.close()

        newFn = open(dstPath, 'w+')
        try:
            newFn.write(template_text % substituteDict)
        finally:
            newFn.close()
    except:
        logIt("Error writing template %s to %s" % (srcPath, dstPath), True)
        logIt(traceback.format_exc(), True)

def generate_random(len):
    return os.urandom(len).encode('hex') 

def applyOxAuthSessionStatePath():
    oxAuthContextXmlFileName = "oxauth.xml"

    oxauth_jsf_salt = generate_random(16)
    substituteDict = {"oxauth_jsf_salt" : oxauth_jsf_salt }

    oxAuthContextXmlFileSrc = "%s/templates/%s" % (setupFolder, oxAuthContextXmlFileName)
    oxAuthContextXmlFileDest = "%s/conf/Catalina/localhost/%s" % (tomcatFolder, oxAuthContextXmlFileName)
    copyRenderedTemplate(oxAuthContextXmlFileSrc, oxAuthContextXmlFileDest, substituteDict)

# Create log and backup folders
if not os.path.exists(bu_folder):
    os.mkdir(bu_folder)
if not os.path.exists(log_folder):
    os.mkdir(log_folder)

# Stop Gluu services
serviceinit("tomcat", "stop")
serviceinit("opendj", "stop")

# Backup Changed Stuff
backupCustomizations("oxauth.war")
backupCustomizations("identity.war")
cpfile("/opt/opendj/config/schema/101-ox.ldif", "%s/101-ox.ldif" % bu_folder)

# Copy distribution
cpfile("%s/idp.war" % src_dir, "/opt/idp/war/idp.war")
cpfile("%s/oxcas.war" % src_dir, "/opt/dist/oxcas.war")
cpfile("%s/oxauth.war" % src_dir, "%s/webapps/oxauth.war" % tomcatFolder)
cpfile("%s/identity.war" % src_dir, "%s/webapps/identity.war" % tomcatFolder)
cpfile("%s/community-edition-setup/static/opendj/101-ox.ldif" % src_dir, "/opt/opendj/config/schema/101-ox.ldif")

# Remove expanded folders
rmdir(oxauthFolder)
rmdir(identityFolder)

# Unzip Files
os.mkdir(oxauthFolder)
os.mkdir(identityFolder)
getOutput([unzip, "%s/webapps/oxauth.war" % tomcatFolder, '-d', oxauthFolder])
getOutput([unzip, "%s/webapps/identity.war" % tomcatFolder, '-d', identityFolder])

# Restore customized files
restoreCustomizations(bu_folder)

# Backup current setup and install new setup script 
updateSetup()

# Backup current setup and install new setup script 
applyOxAuthSessionStatePath()

# Change permissions
changeown(tomcatFolder, "tomcat")
changeown("/opt/idp", "tomcat")
changeown("/opt/opendj", "ldap")

# Start services
serviceinit("opendj", "start")

print "Waiting 10 seconds to allow OpenDJ start up"
time.sleep(10)

serviceinit("tomcat", "start")
