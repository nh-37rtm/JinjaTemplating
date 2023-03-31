#! /usr/bin/python3

import argparse
import os

import Modules.EntryPoint as EntryPoint

# =============================================
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='customize a jinja template file')

    parser.add_argument('-c', '--config-file', required=False,
        default= None)

    parser.add_argument('-dr', '--dry-run', default = False, required=False, action='store_true' )
    
    parser.add_argument('-i', '--input', required=False)
    parser.add_argument('-f', '--format', required=False)
    parser.add_argument('-o', '--output', required=False)
    parser.add_argument('-t', '--template', required=False)
    parser.add_argument('-r', '--reference-path',
        default=os.getcwd(), required=False)
    parser.add_argument('-v', '--output-validator', 
        action='append', required=False)

    args=parser.parse_args()
    EntryPoint.validateArgsAndRun(args)
