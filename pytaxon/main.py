#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

from pytaxon import Pytaxon, Pytaxon_COL, Pytaxon_NCBI, Pytaxon_INAT, Pytaxon_GBIF


def main(): 
    parser = argparse.ArgumentParser(description='Pytaxon baby')
    parser.add_argument('-i', '--input', help='Input of original spreadsheet')
    parser.add_argument('-r', '--columns', help="Input of column names: 'ScientificName, Species, Genus, Family, Order, Class, Phylum, Kingdom'")
    parser.add_argument('-c', '--to_check', type=str, help='Name of spreadsheet to check')
    parser.add_argument('-si', '--source_id', type=int, help='Number of the source ID')

    parser.add_argument('-os', '--original_spreadsheet', help='Use the Open Tree of Life service API')
    parser.add_argument('-cs', '--checked_spreadsheet', help='Use the Open Tree of Life service API')
    parser.add_argument('-o', '--output', help='Name of checked spreadsheet')
    args = parser.parse_args()

    match args.source_id:
        case 1:
            pt = Pytaxon_COL()
            pt.read_spreadshet(args.input)
            pt.read_columns(args.columns)
            pt.check_species_and_lineage(1)
            pt.create_to_correct_spreadsheet(args.to_check)

        case 4:
            pt = Pytaxon_NCBI()
            pt.read_spreadshet(args.input)
            pt.read_columns(args.columns)
            pt.check_species_and_lineage(4)
            pt.create_to_correct_spreadsheet(args.to_check)

        case 11:
            pt = Pytaxon_GBIF()
            pt.read_spreadshet(args.input)
            pt.read_columns(args.columns)
            pt.check_species_and_lineage(11)
            pt.create_to_correct_spreadsheet(args.to_check)

        case 180:
            pt = Pytaxon_INAT()
            pt.read_spreadshet(args.input)
            pt.read_columns(args.columns)
            pt.check_species_and_lineage(180)
            pt.create_to_correct_spreadsheet(args.to_check)

        case _:
            if args.original_spreadsheet and args.checked_spreadsheet:
                pt = Pytaxon()
                pt.update_original_spreadsheet(args.original_spreadsheet, args.checked_spreadsheet, args.output)
            else:
                print('Error')


if __name__ == '__main__':
    main()
