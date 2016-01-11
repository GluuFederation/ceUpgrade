#!/bin/bash

if [ -z "$1" ]; then
    echo "You should specify update version"
    exit 1
fi

VER=$1
SCRIPT_NAME=gluu-update-$VER.sh

rm -rf gluu-update24

mkdir -p gluu-update24/bin
mkdir -p gluu-update24/log
mkdir -p gluu-update24/bkp

rm -rf gluu-update24/update
mkdir -p gluu-update24/update

cp update.py gluu-update24/bin/.
cp LICENSE gluu-update24/.
cp README.md gluu-update24/.

cp -r dist gluu-update24/.

pushd gluu-update24
tar -cjf ./update/gluu-update.tar.bz2 .

pushd update

base64 gluu-update.tar.bz2 > gluu-update.tar.bz2.b64

cat > $SCRIPT_NAME << EOF
#!/bin/sh

base64 -d << BASE64_FILE_END | tar xj
EOF

cat gluu-update.tar.bz2.b64 >> $SCRIPT_NAME

echo 'BASE64_FILE_END' >> $SCRIPT_NAME

cat >> $SCRIPT_NAME << EOF
while true; do
    read -p "Do you wish to install this program? " yn
    case \$yn in
        [Yy]* ) cd bin; ./update.py; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
EOF

md5sum $SCRIPT_NAME > $SCRIPT_NAME.md5sum

popd
popd
