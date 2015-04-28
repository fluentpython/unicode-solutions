#!/bin/bash

if make doctest; then
    echo 'OK!'
    make html
else
    echo 'NOT ok!'
    exit 1
fi
