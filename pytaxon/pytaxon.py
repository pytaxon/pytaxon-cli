#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pytaxon import Pytaxon_GBIF

def main():
    if len(sys.argv) == 1:
        if not pt.connect_to_api:
            print('Could not connect to GBIF API')
            exit()

        pt = Pytaxon_GBIF()
        print(pt.logo)
        pt.read_spreadshet(sys.argv[1])
        pt.read_columns()
        pt.check_species_and_lineage()
    else:
        print('Please pass the path to the spreadsheet')

if __name__ == '__main__':
    main()
