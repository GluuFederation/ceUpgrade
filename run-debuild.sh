#!/bin/bash

#RELEASE=
#UPDATE="gluu-update24"

mkdir -p gluu-update24/opt/gluu-server24/var/lib/gluu-update/2.4.1/bin
mkdir -p gluu-update24/opt/gluu-server24/var/lib/gluu-update/2.4.1/log
mkdir -p gluu-update24/opt/gluu-server24/var/lib/gluu-update/2.4.1/bkp
cp update.py gluu-update24/opt/gluu-server24/var/lib/gluu-update/2.4.1/bin/.
cp LICENSE gluu-update24/opt/gluu-server24/var/lib/gluu-update/2.4.1/.
cp README.md gluu-update24/opt/gluu-server24/var/lib/gluu-update/2.4.1/.
rm -rf gluu-update24/opt/gluu-server24/var/lib/gluu-update/2.4.1/dist
cp -r dist gluu-update24/opt/gluu-server24/var/lib/gluu-update/2.4.1/.
rm -rf gluu-update24/debian
cp -r debian gluu-update24/.

pushd gluu-update24
debuild clean
dpkg-buildpackage -us -uc
popd
