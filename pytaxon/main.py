#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

from pytaxon import Pytaxon, Pytaxon_GBIF, Pytaxon_OTT


def main(): 
    parser = argparse.ArgumentParser(description='Pytaxon baby')
    parser.add_argument('-i', '--input', help='Input of original spreadsheet')
    parser.add_argument('-r', '--columns', help="Input of column names: ['Species', 'Family', 'Order', 'Class', 'Phylum', 'Kingdom']")
    parser.add_argument('-c', '--to_check', type=str, help='Name of spreadsheet to check')
    parser.add_argument('-gbif', action='store_true', help='Use the GBIF service API')
    parser.add_argument('-ott', action='store_true', help='Use the Open Tree of Life service API')

    parser.add_argument('-os', '--original_spreadsheet', help='Use the Open Tree of Life service API')
    parser.add_argument('-cs', '--checked_spreadsheet', help='Use the Open Tree of Life service API')
    parser.add_argument('-o', '--output', help='Name of checked spreadsheet')
    args = parser.parse_args()

    if args.gbif:
        pt = Pytaxon_GBIF()
        pt.read_spreadshet(args.input)
        pt.read_columns(args.columns)
        pt.check_species_and_lineage()
        pt.create_to_correct_spreadsheet(args.to_check)

    elif args.ott:
        pt = Pytaxon_OTT()
        pt.read_spreadshet(args.input)
        pt.read_columns(args.columns)
        pt.check_species_and_lineage()
        pt.create_to_correct_spreadsheet(args.to_check)

    elif args.original_spreadsheet and args.corrected_spreadsheet:
        pt = Pytaxon()
        pt.update_original_spreadsheet(args.original_spreadsheet, args.corrected_spreadsheet, args.output)
    else:
        print('Error')


if __name__ == '__main__':
    main()
