#!/bin/bash

# need help figureing wich version and files gonna be upgrade it

TOMCATDIRVER="apache-tomcat-7.0.55"
OXIDP="/opt/gluu-server/opt/idp/war"
OXCAS="/opt/gluu-server/opt/dist"
OXTRUST="/opt/gluu-server/opt/$TOMCATDIRVER/webapps"
OXAUTH="/opt/gluu-server/opt/$TOMCATDIRVER/webapps"
UPDATER="/opt/gluu-server/opt/gluu-server-updater/$VER/dist"
GLUU_SERVER="/etc/init.d/gluu-server"
GLUU_PATH="/opt/gluu-server"

echo -e "Beggining of the upgrade process, Stoping gluu-server..."
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
echo -n "Starting gluu-server..."
if [ -f $GLUU_SERVER ]; then
      `$GLUU_SERVER start`
fi


echo -n "Upgrade process ends successfully."
