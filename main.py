# import convert360
# import cubemap_glue_floor
# import glue_images

import importlib
import argparse

def execute_module(module_name, module_args):
    module = importlib.import_module(module_name)
    module.execute_module(module_args)

def main():
    parser = argparse.ArgumentParser(description="Dynamic module execution")
    parser.add_argument("--module", help="Module to execute")
    args, extra_args = parser.parse_known_args()

    if args.module:
        execute_module(args.module, extra_args)
    else:
        print("Please specify --module")

if __name__ == '__main__':
    main()