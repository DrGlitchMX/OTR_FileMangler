#!/bin/bash

OTR_MANGLER_BASE="/share/MD0_DATA/qnapconfig_persistent/python/OTR_FileMangler/otr"
TIME=`date +'%Y-%m-%d'`

if [ -d $OTR_MANGLER_BASE ]; then
    [ -d $OTR_MANGLER_BASE/log ] || mkdir $OTR_MANGLER_BASE/log
    ( cd $OTR_MANGLER_BASE
      /usr/bin/env python otr_file_mangler.py >> log/"$TIME"_otr_mangler.log )
else
    echo "Cannot execute $0: directory \"$OTR_MANGLER_BASE\" does not exist."
fi


