# -*- coding: utf-8 -*-

import argparse


def is_verbose():
    """Returns whether verbose output should be used or not."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="display verbose output",
                        action="store_true")
    options = parser.parse_args()
    return options.verbose
