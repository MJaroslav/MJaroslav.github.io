#!/usr/bin/env python3
import argparse
import sys
import shutil


def init():
    parser = argparse.ArgumentParser(
        description="Builder for MJaroslav.github.io site, but you can use it too.")
    parser.add_argument("-o", "--output", metavar="PATH",
                        default="_site", help='set build output directory. Default is "_site".')
    return parser.parse_args(sys.argv[1:])


def build(buildDir):
    # For actions test
    shutil.rmtree(f"./{buildDir}", ignore_errors=True)
    shutil.copytree("./source/", f"./{buildDir}")


def main():
    args = init()
    build(args.output)


if __name__ == "__main__":
    main()
