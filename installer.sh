#!/usr/bin/env bash

EXTRA_PACKAGES_LOCATION='./extra_packages'
REQUIREMENTS_FILE='requirements.txt'
RESULT=0

if [ -d "$EXTRA_PACKAGES_LOCATION" ]; then
  if [ -n "$(ls $EXTRA_PACKAGES_LOCATION)" ]; then
    pip install $EXTRA_PACKAGES_LOCATION/*
    RESULT=$?
  else
    echo "no extra packages found (in 'extra_packages')"
  fi
else
  echo "'extra_packages' folder not existing … skipping"
fi

exit $RESULT
