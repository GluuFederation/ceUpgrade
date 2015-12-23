#!/bin/bash

RELEASE=1
UPDATE="gluu-update24"

mkdir -p gluu-update24/opt/$UPDATE/$RELEASE/bin
mkdir -p gluu-update24/opt/$UPDATE/$RELEASE/log
mkdir -p gluu-update24/opt/$UPDATE/$RELEASE/bkp
cp update.py gluu-update24/opt/$UPDATE/$RELEASE/bin/.
cp prepare_update.py gluu-update24/opt/$UPDATE/$RELEASE/bin/.
cp update.properties gluu-update24/opt/$UPDATE/$RELEASE/bin/.
cp LICENSE gluu-update24/opt/$UPDATE/$RELEASE/.
cp README.md gluu-update24/opt/$UPDATE/$RELEASE/.
cp -r dist gluu-update24/opt/$UPDATER/$RELEASE/
cp -r debian gluu-update24/.

pushd gluu-update24
debuild clean
dpkg-buildpackage -us -uc
popd
