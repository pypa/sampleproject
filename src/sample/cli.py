import argparse


def greet(argv=None):
    parser = argparse.ArgumentParser(prog="sample-greet")
    parser.add_argument("--name", default="World")
    args = parser.parse_args(argv)

    print(f"Hello, {args.name}")
