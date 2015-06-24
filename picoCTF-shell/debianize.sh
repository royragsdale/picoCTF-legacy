#!/bin/bash

REQUIRED="debhelper devscripts python3-all-dev"
for package in $REQUIRED; do
  if [ -z "`dpkg -s $package`" ]; then
    echo $package is required for running debianize.
    exit 1
  fi
done
pip3 install stdeb --upgrade

PACKAGE=/tmp/shell.tar.gz
DIST=/tmp/deb_dist
dir=`readlink -e $(dirname BASH_SOURCE)`
cd $dir && git archive --format=tar.gz --prefix=shell_manager/ master > $PACKAGE
cd `dirname $PACKAGE`
py2dsc -m 'Nihil Hacker <nihil@hacker.com>' $PACKAGE
cd deb_dist/hacksport-shell*
python setup.py sdist
for package in `cat hacksport_shell_manager.egg-info/requires.txt`; do
  echo $package python3-pip >> debian/py3dist-overrides
  echo pip3 install $package --upgrade >> debian/postinst
done
rm -rf hacksport_shell* dist

ls debian && pwd
debuild

cp -v $DIST/python3-*.deb $dir/
rm -rf $DIST $PACKAGE
