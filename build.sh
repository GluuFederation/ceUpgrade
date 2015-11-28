#!/bin/bash

GLUU_VER=$1
RELEASE=$2

RELEASE_DIR="1"
if [ -n "${RELEASE}" ]; then
    RELEASE=$RELEASE_DIR
fi

if [ $VER == 24]; then
	mkdir -p build/
	mkdir -p build/opt/gluu-server24/opt/gluu-server-updater/$RELEASE
	cp -r dist build/opt/gluu-server24/opt/gluu-server-updater/$RELEASE/
	cp update-24.sh build/opt/gluu-server/opt/gluu-server-updater/$RELEASE/bin/update.sh 
	cp -r debian24 build/debian
	cat build/debian/postinst | sed -e 's/CHANGEME/$RELEASE/' > build/debian/postinst
else
        mkdir -p build/
        mkdir -p build/opt/gluu-server/opt/gluu-server-updater/$RELEASE/bin
        cp -r dist build/opt/gluu-server/opt/gluu-server-updater/$RELEASE/
	cp update-23.sh build/opt/gluu-server/opt/gluu-server-updater/$RELEASE/bin/update.sh 
	cp -r debian23 build/debian
	cat build/debian/postinst | sed -e 's/CHANGEME/$RELEASE/' > build/debian/postinst
fi

pushd build
dpkg-buildpackage -us -uc
popd
