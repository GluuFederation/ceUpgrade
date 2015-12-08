#!/bin/bash

VER=$1
INSTALL_VER=$2

mkdir -p dist
OXIDP="dist"
OXCAS="dist"
OXTRUST="dist"
OXAUTH="dist"
COMMUNITY="dist"



INSTALL="master"
if [ -n "${INSTALL_VER}" ]; then
    INSTALL=$INSTALL_VER
fi

if [ -n "${VER}" ]; then
    wget -nv http://ox.gluu.org/maven/org/xdi/oxidp/$VER/oxidp-$VER.war -O $OXIDP/idp.war
    wget -nv http://ox.gluu.org/maven/org/xdi/ox-cas-server-webapp/$VER/ox-cas-server-webapp-$VER.war -O $OXCAS/oxcas.war
    wget -nv http://ox.gluu.org/maven/org/xdi/oxtrust-server/$VER/oxtrust-server-$VER.war -O $OXTRUST/identity.war
    wget -nv http://ox.gluu.org/maven/org/xdi/oxauth-server/$VER/oxauth-server-$VER.war -O $OXAUTH/oxauth.war
    rm -rf $COMMUNITY/community-edition-setup*
    curl -LkSs https://codeload.github.com/GluuFederation/community-edition-setup/zip/$INSTALL -o $COMMUNITY/community-edition-setup.zip
    unzip $COMMUNITY/community-edition-setup.zip -d $COMMUNITY
    mv -nv $COMMUNITY/community-edition-setup-$INSTALL $COMMUNITY/community-edition-setup
    rm -rf $COMMUNITY/community-edition-setup.zip
fi
