# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from tutorials.catalog.models import Product
from north.dbutils import babel_values

def P(en,de,fr):
    return Product(**babel_values('name',en=en,de=de,fr=fr))

def objects():
    yield P("Chair","Stuhl","Chaise")
    yield P("Table","Tisch","Table")
    yield P("Monitor","Bildschirm","Écran")
    yield P("Mouse","Maus","Souris")
    yield P("Keyboard","Tastatur","Clavier")
    yield P("Consultation","Beratung","Consultation")
