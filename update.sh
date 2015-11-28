#!/bin/bash

# need help figureing wich version and files gonna be upgrade it

TOMCATDIRVER="apache-tomcat-7.0.55"
OXIDP="/opt/CHANGEME/opt/idp/war"
OXCAS="/opt/CHANGEME/opt/dist"
OXTRUST="/opt/CHANGEME/opt/$TOMCATDIRVER/webapps"
OXAUTH="/opt/CHANGEME/opt/$TOMCATDIRVER/webapps"
UPDATER="/opt/CHANGEME/opt/CHANGEME-updater/$VER/dist"
GLUU_SERVER="/etc/init.d/CHANGEME"
GLUU_PATH="/opt/CHANGEME"

echo -e "Beggining of the upgrade process, Stoping CHANGEME..."
if [ -f $GLUU_SERVER ]; then
	`$GLUU_SERVER stop`
fi
if [ -d $GLUU_PATH ]; then
	echo -e "Upgrading the files..."
	if [ -f $UPDATER/idp.war ]; then
    		cp $UPDATER/idp.war $OXIDP/idp.war
	fi
	if [ -f $UPDATER/oxcas.war ]; then
    		cp $UPDATER/oxcas.war $OXCAS/oxcas.war
	fi
	if [ -f $UPDATER/identity.war ]; then
    		cp $UPDATER/identity.war $OXTRUST/identity.war
	fi
	if [ -f $UPDATER/oxauth.war ]; then
    		cp $UPDATER/oxauth.war $OXAUTH/oxauth.war
	fi
fi
echo -n "Starting CHANGEME..."
if [ -f $GLUU_SERVER ]; then
      `$GLUU_SERVER start`
fi


echo -n "Upgrade process ends successfully."
