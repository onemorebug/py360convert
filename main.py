import cut_equi_top
import convert360
import cubemap_trim_floor
import cubemap_glue_floor
import glue_images

import importlib
import argparse

def execute_module(module_name):
    module = importlib.import_module(module_name)
    module.execute_module()

def main():
    parser = argparse.ArgumentParser(description="Dynamic module execution")
    parser.add_argument("--module", help="Module to execute")
    args = parser.parse_args()

    if args.module:
        execute_module(args.module)
    else:
        print("Please specify --module")

if __name__ == '__main__':
    main()