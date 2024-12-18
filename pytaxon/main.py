import argparse

from pytaxon import Pytaxon


def main(): 
    parser = argparse.ArgumentParser(description='Pytaxon arguments to use on terminal')
    parser.add_argument('-os', '--original_spreadsheet', type=str, help='Path of original spreadsheet')
    parser.add_argument('-ss', '--suggestion_spreadsheet', type=str, help='Path of suggestion spreadsheet')
    parser.add_argument('-r', '--columns', help="Input of column names: 'Kingdom, Phylum, Class, Order, Family, Genus, Species, ScientificName'")
    parser.add_argument('-si', '--source_id', type=int, help='Number of the source ID')
    parser.add_argument('-c', '--corrected', type=str, help='Name of corrected spreadsheet')
    args = parser.parse_args()

    if not args.columns and args.source_id:
        pt = Pytaxon()
        pt.update_original_spreadsheet(args.original_spreadsheet, args.suggestion_spreadsheet, args.corrected)
    else:
        pt = Pytaxon(args.source_id)
        pt.read_spreadshet(args.original_spreadsheet)
        pt.read_columns(args.columns)
        pt.check_species_and_lineage()
        pt.create_to_correct_spreadsheet(args.suggestion_spreadsheet)
        

if __name__ == '__main__':
    main()
