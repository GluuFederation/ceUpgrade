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


import os.path
import Properties
import random
import shutil
import socket
import string
import time
import uuid
import json
import traceback
import subprocess
import sys
import getopt
import hashlib

class PrepareUpdate(object):
    def __init__(self, update_dir=None):
        self.update_dir = update_dir

        self.oxVersion = '3.0.3-SNAPSHOT'
        self.oxUpdateVersion = '1'

        self.oxtrust_war = 'https://ox.gluu.org/maven/org/xdi/oxtrust-server/%s/oxtrust-server-%s.war' % (self.oxVersion, self.oxVersion)
        self.oxauth_war = 'https://ox.gluu.org/maven/org/xdi/oxauth-server/%s/oxauth-server-%s.war' % (self.oxVersion, self.oxVersion)
        self.oxauth_rp_war = 'https://ox.gluu.org/maven/org/xdi/oxauth-rp/%s/oxauth-rp-%s.war' % (self.oxVersion, self.oxVersion)
        self.idp_war = 'http://ox.gluu.org/maven/org/xdi/oxidp/%s/oxidp-%s.war' % (self.oxVersion, self.oxVersion)
        self.asimba_war = "http://ox.gluu.org/maven/org/xdi/oxasimba-proxy/%s/oxasimba-proxy-%s.war" % (self.oxVersion, self.oxVersion)
        self.cas_war = "http://ox.gluu.org/maven/org/xdi/ox-cas-server-webapp/%s/ox-cas-server-webapp-%s.war" % (self.oxVersion, self.oxVersion)

        self.components = {'oxauth':  {'enabled': True},
                           'oxtrust': {'enabled': True},
                           'saml':    {'enabled': False},
                           'cas':     {'enabled': False},
                           'oxauth_rp':  {'enabled': False}
        }

        self.updateFolder = "/opt/udpdate/" % self.oxUpdateVersion
        self.setup_properties_fn = "%s/prepare_update.properties" % self.update_dir
        self.log = '%s/prepare_update.log' % self.update_dir
        self.logError = '%s/prepare_update_error.log' % self.update_dir


    def copyFile(self, inFile, destFolder):
        try:
            shutil.copy(inFile, destFolder)
            self.logIt("Copied %s to %s" % (inFile, destFolder))
        except:
            self.logIt("Error copying %s to %s" % (inFile, destFolder), True)
            self.logIt(traceback.format_exc(), True)

    def createDirs(self, name):
        try:
            if not os.path.exists(name):
                os.makedirs(name, 0700)
                self.logIt('Created dir: %s' % name)
        except:
            self.logIt("Error making directory %s" % name, True)
            self.logIt(traceback.format_exc(), True)
    
    def makeFolders(self):
        try:
            print "Creating update folder structure..."
            self.createDirs(self.updateFolder)
        except:
            self.logIt("Error making folders", True)
            self.logIt(traceback.format_exc(), True)
        

    def downloadWarFiles(self):
        if self.components['oxauth']['enabled']: 
            print "Downloading oxAuth war file..."
            self.run(['/usr/bin/wget', self.oxauth_war, '-O', '%s/oxauth.war' % self.self.updateFolder])

        if self.components['oxtrust']['enabled']: 
            print "Downloading oxTrust war file..."
            self.run(['/usr/bin/wget', self.oxtrust_war, '-O', '%s/identity.war' % self.updateFolder])

        if self.components['saml']['enabled']: 
            print "Downloading Shibboleth IDP war file..."
            self.run(['/usr/bin/wget', self.idp_war, '-O', '%s/idp.war' % self.updateFolder])

        if self.components['cas']['enabled']: 
            print "Downloading CAS war file..."
            self.run(['/usr/bin/wget', self.cas_war, '-O', '%s/oxcas.war' % self.updateFolder])

        if self.components['oxauth_rp']['enabled']: 
            print "Downloading oxAuth war file..."
            self.run(['/usr/bin/wget', self.oxauth_rp_war, '-O', '%s/oxauth-rp.war' % self.self.updateFolder])

        print "Finished downloading latest war files"

    def load_properties(self, fn):
        self.logIt('Loading Properties %s' % fn)
        p = Properties.Properties()
        try:
            p.load(open(fn))
            properties_list = p.keys()
            for prop in properties_list:
#                update components[] here according to the properties
                print ""
#                try:
#                    self.__dict__[prop] = p[prop]
#                except:
#                    self.logIt("Error loading property %s" % prop)
#                    prepareUpdateObject.logIt(traceback.format_exc(), True)
        except:
            self.logIt("Error loading properties", True)
            self.logIt(traceback.format_exc(), True)


############################   Main Loop   #################################################

if __name__ == '__main__':
    updateOptions = {
        'update_dir': '.',
        'update_properties': 'update.properties',
        'updateOxAuth': True,
        'updateOxTrust': True,
        'updateSAML': False,
        'updateAsimba': False,
        'updateCAS': False,
        'updateOxAuthRP': False
    }

    prepareUpdateObject = PrepareUpdate(updateOptions['update_dir'])

    prepareUpdateObject.components['oxauth']['enabled'] = updateOptions['updateOxAuth']
    prepareUpdateObject.components['oxtrust']['enabled'] = updateOptions['updateOxTrust']
    prepareUpdateObject.components['saml']['enabled'] = updateOptions['updateSAML']
    prepareUpdateObject.components['cas']['enabled'] = updateOptions['updateCAS']
    prepareUpdateObject.components['oxauth_rp']['enabled'] = updateOptions['updateOxAuthRP']

    print "\Preparing update for Gluu Server...\n\nFor more info see:\n  %s  \n  %s\n" % (prepareUpdateObject.log, prepareUpdateObject.logError)
    try:
        os.remove(prepareUpdateObject.log)
        prepareUpdateObject.logIt('Removed %s' % prepareUpdateObject.log)
    except:
        pass
    try:
        os.remove(prepareUpdateObject.logError)
        prepareUpdateObject.logIt('Removed %s' % prepareUpdateObject.logError)
    except:
        pass

    prepareUpdateObject.logIt("Preparing update for Gluu Server", True)

    try:
        prepareUpdateObject.load_properties(updateOptions['setup_properties'])
        prepareUpdateObject.makeFolders()
        prepareUpdateObject.downloadWarFiles()

        print "\n\n Prepare update for Gluu Server has been successful!"
    except:
        prepareUpdateObject.logIt("***** Error caught in main loop *****", True)
        prepareUpdateObject.logIt(traceback.format_exc(), True)

# END
