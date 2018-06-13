#!/usr/bin/env python3

import argparse
import pathlib
import sys

import settings
from apii.api_interface import APIInterface
from authorizer.authorizer import Authorizer
from database.db import Database
from database.interpreter import Interpreter
from nicparser.parser import Parser

cmds = argparse.ArgumentParser(
    description="Compile network information files into Cypherpath SDIs." + \
                "\nCurrently only supports pcap formatted files.")
cmds.add_argument("-a", "--all",
                  help="display all available information while compiling",
                  action="store_true")
cmds.add_argument("-f", "--files", nargs="+",
                  help="path to one or more pcap files or a directory of pcap files to compile")
cmds.add_argument("-v", "--version",
                  help="print the version number",
                  action="store_true")

# Force argparse to print help when no args are specified
# Could override argparse error if further control is required
if len(sys.argv) == 1:
    cmds.print_help(sys.stderr)
    sys.exit()

args = cmds.parse_args()

# Process the arguments
if args.version:
    print("Version:", settings.VERSION)
    sys.exit()


# Initialize all the nic1 subsystems to process the files
# If anything fails, exit
if args.files:
    try:
        DB = Database()
        parse = Parser(DB)
        authorizer = Authorizer()
    except ValueError as err:
        print(err.args)
        exit(1) #abnormal exit

    print("Compiling...")
    # Loop through the specified files
    for f in args.files:
        f_path = pathlib.Path(f)
        if f_path.is_dir():
            for f_path in f_path.iterdir():
                if f_path.is_file():
                    parse.parse_file(f_path.as_posix())
        else:
            if f_path.is_file():
                parse.parse_file(f_path.as_posix())

    interpreter = Interpreter(DB)
    interpreter.interpret()
    if args.all:
        DB.print_all_tables()

    # Create the SDI
    apii = APIInterface(authorizer, DB)

    apii.start(authorizer.get_username(), ", ".join(args.files))
    apii.add_networks()
    apii.add_machines()
    apii.connect()
    apii.specify_machines()
    apii.print_success()
