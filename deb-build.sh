#!/bin/bash

GLUU_VER=$1
RELEASE=$2

RELEASE_DIR="1"
if [ -n "${RELEASE}" ]; then
    RELEASE=$RELEASE_DIR
fi

if [ $VER == 24]; then
	mkdir -p build/
	mkdir -p build/opt/gluu-server24/opt/gluu-server-updater24/$RELEASE

	cp -r dist build/opt/gluu-server24/opt/gluu-server-updater24/$RELEASE/
	cp update.sh build/opt/gluu-server24/opt/gluu-server-updater24/$RELEASE/bin/
	cp -r debian build/debian

	cat build/debian/changelog | sed -e 's/gluu-server-updater/gluu-server-updater24/' > build/debian/changelog
	cat build/debian/control | sed -e 's/gluu-server-updater/gluu-server-updater24/' > build/debian/control
	cat build/debian/control | sed -e 's/CHANGEME/gluu-server24/' > build/debian/control
	cat build/debian/copyright | sed -e 's/gluu-server-updater/gluu-server-updater24/' > build/debian/copyright
	cat build/debian/postinst | sed -e 's/CHANGEME/$RELEASE/' > build/debian/postinst
	cat build/debian/rules | sed -e 's/gluu-server-updater/gluu-server-updater24/' > build/debian/rules
	cat build/opt/gluu-server24/opt/gluu-server-updater24/$RELEASE/bin/update.sh | sed -e 's/CHANGEME/gluu-server24/' > build/opt/gluu-server/opt/gluu-server-updater/$RELEASE/bin/update.sh

else
        mkdir -p build/
        mkdir -p build/opt/gluu-server/opt/gluu-server-updater/$RELEASE/bin

        cp -r dist build/opt/gluu-server/opt/gluu-server-updater/$RELEASE/
	cp update.sh build/opt/gluu-server/opt/gluu-server-updater/$RELEASE/bin/
	cp -r debian build/debian

	cat build/debian/control | sed -e 's/CHANGEME/gluu-server/' > build/debian/control
	cat build/debian/postinst | sed -e 's/CHANGEME/$RELEASE/' > build/debian/postinst
	cat build/opt/gluu-server/opt/gluu-server-updater/$RELEASE/bin/update.sh | sed -e 's/CHANGEME/gluu-server/' > build/opt/gluu-server/opt/gluu-server-updater/$RELEASE/bin/update.sh

fi

pushd build
dpkg-buildpackage -us -uc
popd
