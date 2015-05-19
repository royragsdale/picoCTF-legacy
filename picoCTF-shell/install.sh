#!/bin/bash

fakeroot dpkg-deb --build shell_manager shell_manager-1.0.deb
dpkg -i shell_manager-1.0.deb
