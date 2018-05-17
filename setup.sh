#!/bin/bash

TRACKER='/srv/ISS_TRACKER'
CODE='https://github.com/jerrington/ISS-Tracker.git'

code_setup() {

    if [ -d $TRACKER ]
    then
        mkdir -p $TRACKER
    fi
    cd $TRACKER 
    git clone $CODE

}

update_check() {

    #check for updates
    cd $TRACKER 
    git pull master

}

if [ ! -d "$TRACKER" || ! -f "$TRACKER/ISS_TRACKER.py" ]
then
    code_setup
else
    
    update_check


    