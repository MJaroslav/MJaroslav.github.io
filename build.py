#!/usr/bin/env python3
import argparse
import sys
import shutil
import os
from bs4 import BeautifulSoup as bs
import json
from datetime import date
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import http.server
import socketserver
import inline


def init():
    parser = argparse.ArgumentParser(
        add_help=True,
        description="Builder for MJaroslav.github.io site, but you can use it too. For dev, use -cds",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="PATH",
        default="_site",
        help='set build output directory. Default is "_site".',
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Clean output directory before build.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show more information about building.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Mark build as debug, its will disable visit counter and similar things.",
    )
    parser.add_argument(
        "-a",
        "--auto",
        action="store_true",
        help="Listen for any changes in source directory and rebuild project.",
    )
    parser.add_argument(
        "-s",
        "--server",
        action="store_true",
        help="Run local web server and listen for any changes in source directory and rebuild project.",
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    else:
        return parser.parse_args(sys.argv[1:])


class Builder(object):
    def __init__(self, buildDir, clean, verbose, debug, server):
        self.buildDir = buildDir
        self.clean = clean
        self.verbose = verbose
        self.debug = debug
        self.server = server

    def log(self, text):
        if self.verbose:
            print(text)

    def place_list(
        self,
        html_file,
        json_file,
        pre_msg,
        elem_msg,
        place_params,
        keys,
        place_type="div",
        strip=False,
        remove_ln=False,
    ):
        if pre_msg:
            self.log(pre_msg)
        with open(html_file, "r") as file:
            template = file.read()
            with open(json_file, "r") as file:
                data = json.load(file)
                data = inline.apply(data)
                for e in data:
                    formatted = template
                    for key in keys:
                        if type(key) == str:
                            formatted = formatted.replace(
                                f"@{key.upper()}@", e.get(key, "")
                            )
                        else:
                            formatted = formatted.replace(
                                key[0], e.get(key[1], key[2] if len(key) == 3 else "")
                            )
                    if strip:
                        formatted = formatted.strip()
                    if remove_ln:
                        formatted = formatted.replace("\n", "")
                    self.soup.find(place_type, **place_params).append(
                        bs(inline.compile(formatted), "html.parser")
                    )
                    if elem_msg:
                        if type(elem_msg) == str:
                            self.log(elem_msg)
                        else:
                            kwargs = {name: e.get(name, "") for name in elem_msg[1:]}
                            self.log(elem_msg[0].format(**kwargs))

    def build(self):
        inline.load_patterns(self.debug)
        config = json.load(open("./source/config.json", "r"))
        config = inline.apply(config)
        inline.inject_config(config)

        self.log(f"Build directory is {self.buildDir}")
        if self.clean:
            self.log("Clean build directory...")
            shutil.rmtree(f"{self.buildDir}", ignore_errors=True)

        self.log("Building...")

        for static in config["static"]:
            self.log(f"Copying static {static} data...")
            if os.path.isdir(f"./source/{static}"):
                shutil.copytree(
                    f"./source/{static}",
                    f"{self.buildDir}/{static}",
                    dirs_exist_ok=True,
                )
            else:
                shutil.copy(f"./source/{static}", f"{self.buildDir}/{static}")

        self.log(f"Opening {config['index']}...")
        self.soup = bs(inline.load(f"./source/{config['index']}"), "html.parser")

        self.log("Adding bio...")
        self.soup.find("div", id="bio").append(
            bs(inline.load("./source/data/about.html"), "html.parser")
        )

        self.log("Placing lists...")
        for list_data in config["place_list"]:
            self.place_list(*list_data.get("args", []), **list_data.get("kwargs", {}))

        self.log("Setting current year to the footer...")
        self.soup.find("p", id="year").string = str(date.today().year)

        self.log("Writting formatted pattern to index.html...")
        with open(f"{self.buildDir}/index.html", "w") as file:
            text = str(self.soup)
            # text = soup.prettify()
            self.log("Replacing elements...")
            for k, v in config["replace"].items():
                self.log(k + " to " + v)
                text = text.replace(k, v)
            file.write(text)

        self.log("Done!")

    def autobuild(self):
        change_handler = PatternMatchingEventHandler(["*"], None, False, True)

        def on_event(event):
            self.log("Detected changes! Rebuilding...")
            try:
                self.build()
            except Error as e:
                self.log(f"Error {e} when update")

        change_handler.on_created = on_event
        change_handler.on_moved = on_event
        change_handler.on_deleted = on_event
        change_handler.on_modified = on_event

        observer = Observer()
        observer.schedule(change_handler, "./source/", recursive=True)

        self.build()

        observer.start()
        httpd = None
        try:
            if self.server:
                bd = self.buildDir

                class Handler(http.server.SimpleHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, directory=bd, **kwargs)

                httpd = socketserver.TCPServer(("", 8000), Handler)
                self.log("Starting server on localhost:8000...")
                server = httpd
                httpd.serve_forever()
            else:
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            if httpd:
                self.log("Stopping the server...")
                httpd.server_close()


def main():
    args = init()
    if args.server:
        args.auto = True
    builder = Builder(args.output, args.clean, args.verbose, args.debug, args.server)
    if args.auto:
        builder.autobuild()
    else:
        builder.build()


if __name__ == "__main__":
    main()
