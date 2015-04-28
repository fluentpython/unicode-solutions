#!/bin/bash

if python2.7 snippets.py; then
    echo 'OK!'
    make html
else
    echo 'NOT ok!'
    exit 1
fi
