import argparse
import json

import jinja2


def get_args():
    """
    :return: argument parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", help="",
                        type=str, default=None)
    parser.add_argument("--tmpl-name", help="",
                        type=str, default=None)
    parser.add_argument("--cnfg-name", help="",
                        type=str, default=None)
    parser.add_argument("--cnfg-key", help="",
                        type=str, default=None)

    parser.add_argument("--dst-name", help="",
                        type=str, default=None)

    return parser


def render_template(args=None):
    """
    Stitch a list of SEG-Y files into 1 long HDF5 file.
    """
    if args is None:
        args = get_args().parse_args()
    tmplLoader = jinja2.FileSystemLoader(searchpath="./")
    tmplEnv = jinja2.Environment(loader=tmplLoader)

    tmpl = tmplEnv().get_template("README.md.tpl")  # TODO: replace magic word with args
    user_args = dict()  # TODO: load user args using args
    outp = tmpl.render(**user_args)

    # TODO: save outp as a file


if __name__ == "__main__":
  render_template()
