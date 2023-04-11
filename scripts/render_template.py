import argparse
import json
import os
from collections.abc import Iterable, Mapping
from typing import Union, Optional

import jinja2


DEFAULT_CONFIG_KEY = "default"
Config = Mapping[str, str]
MetaConfig = Mapping[str, Config]


def get_args():
    """
    :return: argument parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", help="The path to the work directory. "\
                                           "If provided, all other path arguments should be given relative to this.",
                        type=str, default=None)
    parser.add_argument("--tmpl-path", help="A path to the template file.",
                        type=str, default=None, required=True)
    parser.add_argument("--cnfg-path", help="A path to the config file. "
                                            "It should be a json format, with a dict of dicts. "
                                            "Each dict in the main level represents a different config. "
                                            "The structure can also be put in the 2nd place of a 2 item list, "
                                            "with the 1st item being the name of the selected config.",
                        type=str, default=None, required=True)
    parser.add_argument("--cnfg-key", help="The chosen config to be applied to the template from the config file.",
                        type=str, default=DEFAULT_CONFIG_KEY)

    parser.add_argument("--dest-path", help="A path to the output location of the file.",
                        type=str, default=None, required=True)

    return parser


def handle_args(args: Mapping[str,]) -> tuple[Mapping[str,], str]:
    """
    :param args: The raw arguments passed by the user.
    """
    if args.work_dir is not None:
        args.tmpl_path = os.path.join(args.work_dir, args.tmpl_path)
        args.cnfg_path = os.path.join(args.work_dir, args.cnfg_path)
        args.dest_path = os.path.join(args.work_dir, args.dest_path)
    config_name : str = args.cnfg_key
    return args, config_name


def handle_configs(args: Mapping[str,], 
                   user_configs: Union[MetaConfig, tuple[str, MetaConfig]], 
                   config_name: Optional[str] = None) -> Config:
    """
    :param args: Arguments passed tot he program.
    :param user_configs: A collection of configurations loaded from a config file.
    :param config_name: The config to be chosen from the config file.
    """
    if isinstance(user_configs, Mapping):
        user_configs: MetaConfig
    elif isinstance(user_configs, Iterable):
        # assert (len(user_configs) >= 2) and (len(user_configs) <= 3)
        assert len(user_configs) == 2
        config_name: str = config_name if config_name is not None else user_configs[0]
        user_configs: MetaConfig = user_configs[-1]
        return handle_configs(args, user_configs, config_name)
    else:
        raise TypeError("The config file does not match any of the expected formats.")
    config_name = config_name if config_name is not None else DEFAULT_CONFIG_KEY
    return user_configs[config_name]


def render_template(args=None):
    """
    Stitch a list of SEG-Y files into 1 long HDF5 file.
    """
    if args is None:
        args = get_args().parse_args()
    args, config_name = handle_args(args)

    tmplLoader = jinja2.FileSystemLoader(searchpath="./")
    tmplEnv = jinja2.Environment(loader=tmplLoader)

    tmpl = tmplEnv().get_template(args.tmpl_path)
    
    with open(args.cnfg_path, 'r') as file:
        user_configs = json.load(file)
        user_configs = handle_configs(args, user_configs, config_name)
    
    
    outp = tmpl.render(**user_configs)
    with open(args.dest_path, 'w') as file:
        file.writelines(outp)


if __name__ == "__main__":
  render_template()
