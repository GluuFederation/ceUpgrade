#!/bin/bash

RELEASE=1
UPDATER="gluu-updater24"

mkdir -p gluu-updater/opt/$UPDATER/$RELEASE/bin
cp prepare_update.py gluu-updater/opt/$UPDATER/$RELEASE/bin/.
cp update.properties gluu-updater/opt/$UPDATER/$RELEASE/bin/.
cp update.py gluu-updater/opt/$UPDATER/$RELEASE/bin/.
cp LICENSE gluu-updater/opt/$UPDATER/$RELEASE/.
cp README.md gluu-updater/opt/$UPDATER/$RELEASE/.
cp -r dist gluu-updater/opt/$UPDATER/$RELEASE/
cp -r debian gluu-updater/.

pushd gluu-updater
debuild clean
dpkg-buildpackage -us -uc
popd
