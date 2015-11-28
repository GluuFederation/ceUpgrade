#!/bin/bash

VER=$1
DIST="dist"

if [ -n "${VER}" ]; then
	curl -LSs http://ox.gluu.org/maven/org/xdi/oxidp/$VER/oxidp-$VER.war -o $DIST/idp.war
	curl -LSs http://ox.gluu.org/maven/org/xdi/ox-cas-server-webapp/$VER/ox-cas-server-webapp-$VER.war -o $DIST/oxcas.war
	curl -LSs http://ox.gluu.org/maven/org/xdi/oxtrust-server/$VER/oxtrust-server-$VER.war -o $DIST/identity.war
	curl -LSs http://ox.gluu.org/maven/org/xdi/oxauth-server/$VER/oxauth-server-$VER.war -o $DIST/oxauth.war
fi
