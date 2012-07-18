# -*- coding: utf-8 -*-
"""
    Autor: Jorge A. Toro
"""
import sys
import DB.pgSQL

print "MODULOS:", sys.modules

print "LOCALS:", locals()
print "GLOBALS:", globals()

#import 
d = sys.modules['datetime']
print d.datetime.now()
