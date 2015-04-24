#!/usr/bin/env python2.7
# coding: utf-8

u = u'El Niño'
for codec in ['latin_1', 'utf_8', 'utf_16']:
    print codec + '\t' + u.encode(codec)
