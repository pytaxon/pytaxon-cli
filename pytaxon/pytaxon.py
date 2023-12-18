#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

from pytaxon import Pytaxon_GBIF, Pytaxon_OTT


def main():  # sourcery skip: extract-method
    parser = argparse.ArgumentParser(description='Pytaxon baby')
    parser.add_argument('--gbif', help='Use the GBIF service API')
    parser.add_argument('--ott', help='Use the Open Tree of Life service API')
    parser.add_argument('--od', '--originalData', help='Use the Open Tree of Life service API')
    parser.add_argument('--cd', '--correctedData', help='Use the Open Tree of Life service API')
    args = parser.parse_args()

    if args.gbif:
        pt = Pytaxon_GBIF()
        pt.read_spreadshet(args.gbif)
        pt.read_columns()
        pt.check_species_and_lineage()

    elif args.ott:
        pt = Pytaxon_OTT()
        print(pt.logo)
        if not pt.connect_to_api:
            print('Could not connect to OpenTree API')
            exit()

        pt.read_spreadshet(args.ott)
        pt.read_taxon_columns()
        pt.connect_to_api_taxony()
        pt.data_incorrect_taxons()
        pt.create_taxonomies_pivot_spreadsheet()

    elif args.od and args.cd:
        pt = Pytaxon_GBIF()
        pt.update_original_spreadsheet(args.od, args.cd)
    else:
        print('Error')


if __name__ == '__main__':
    main()
