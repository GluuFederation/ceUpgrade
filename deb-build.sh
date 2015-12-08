#!/bin/bash

pushd gluu-updater
debuild clean
dpkg-buildpackage -us -uc
popd
