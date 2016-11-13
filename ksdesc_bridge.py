#!/usr/bin/env python3.5

import os
from glob import glob
from rdflib.namespace import SKOS
from parcellation import OntMeta, TODAY
from utils import makeGraph, makePrefixes

PREFIXES = makePrefixes('SCR', 'NIFMOL', 'NIFNEURON', 'NIFCELL', 'NIFGA', 'UBERON', 'PR', 'NIFNEURMOR', 'skos', 'owl')

ont = OntMeta('http://ontology.neuinfo.org/NIF/ttl/generated/',
              'ksdesc-defs',
              'Knolwedge Space Defs',
              'KSDEFS',
              'Definitions from knowledge space descriptions. Generated by pyontutils/ksdesc_bridge.py',
              TODAY)

ontid = ont.path + ont.filename + '.ttl'
g = makeGraph(ont.filename, prefixes=PREFIXES)
g.add_ont(ontid, *ont[2:])

top_level = glob(os.path.expanduser('~/git/ksdesc/') + '*')

for putative_dir in top_level:
    if os.path.isdir(putative_dir):
        for putative_md in glob(putative_dir + '/*.md'):
            ident = os.path.split(putative_dir)[-1] + ':' + os.path.splitext(os.path.split(putative_md)[-1])[0]
            print(ident)
            with open(putative_md, 'rt') as f:
                def_ = f.read()

            if 'Definition' in def_:
                def_ = def_.split('Definition', 1)[-1].strip().strip('=').strip()

            g.add_node(ident, SKOS.definition, def_)

g.write()

