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
    return parser.parse_args(sys.argv[1:])


def build(buildDir, clean, verbose, debug):
    def log(text):
        if verbose:
            print(text)

    def format_config(value):
        if value == "!debug":
            return str(not bool(debug))
        elif value == "debug":
            return str(bool(debug))
        else:
            return value

    config = json.load(open("source/config.json", "r"))
    config["replace"] = {k: format_config(v) for k, v in config["replace"].items()}

    log(f"Build directory is {buildDir}")
    if clean:
        log("Clean build directory...")
        shutil.rmtree(f"{buildDir}", ignore_errors=True)

    log("Building...")

    for static in config["static"]:
        log(f"Copying static {static} data...")
        if os.path.isdir(f"./source/{static}"):
            shutil.copytree(
                f"./source/{static}", f"{buildDir}/{static}", dirs_exist_ok=True
            )
        else:
            shutil.copy(f"./source/{static}", f"{buildDir}/{static}")

    log(f"Opening {config['index']}...")
    html = open(f"./source/{config['index']}")
    soup = bs(html, "html.parser")

    log("Adding bio...")
    with open("./source/data/about.html", "r") as file:
        soup.find("div", id="bio").append(bs(file.read(), "html.parser"))

    log("Adding profiles...")
    with open("./source/data/profiles.json", "r") as file:
        profiles = json.load(file)
        for e in profiles:
            tooltip = e["name"]
            if "tooltip" in e:
                tooltip += f"<br><br>{e['tooltip']}"
            attrs = {
                "class": f"profile-entry display-4 {e['icon']} mr-2",
                "href": e["url"],
                "data-html": "true",
                "data-toggle": "tooltip",
                "title": tooltip,
            }
            link = soup.new_tag("a", **attrs)
            soup.find("div", class_="profiles").append(link)
            log(f"Created profile entry {e['name']}")

    log("Adding projects...")
    with open("./source/data/project.html", "r") as file:
        template = file.read()
        with open("./source/data/projects.json", "r") as file:
            projects = json.load(file)
            for e in projects:
                soup.find("div", class_="projects").append(
                    bs(
                        template.replace("@NAME@", e["name"])
                        .replace("@DESC@", e["desc"])
                        .replace("@URL@", e["url"])
                        .replace("@SRC@", e["src"]),
                        "html.parser",
                    )
                )
                log(f"Created project entry {e['name']}")

    log("Adding music...")
    with open("./source/data/music.html", "r") as file:
        template = file.read()
        with open("./source/data/music.json", "r") as file:
            music = json.load(file)
            for e in music:
                tooltip = e["name"]
                if "tooltip" in e:
                    tooltip += f"<br><br>{e['tooltip']}"
                soup.find("div", class_="music").append(
                    bs(
                        template.replace("@URL@", e["url"])
                        .replace("@NAME@", e["name"])
                        .replace("@TOOLTIP@", tooltip)
                        .replace("@IMG@", e["image"]),
                        "html.parser",
                    )
                )
                log(f"Created music entry {e['name']}")

    log("Setting current year to the footer...")
    soup.find("p", id="year").string = str(date.today().year)

    log("Writting formatted pattern to index.html...")
    with open(f"{buildDir}/index.html", "w") as file:
        text = str(soup)
        # text = soup.prettify()
        log("Replacing elements...")
        for k, v in config["replace"].items():
            log(k + " to " + v)
            text = text.replace(k, v)
        file.write(text)

    log("Done!")


def autobuild(buildDir, clean, verbose, debug, server):
    change_handler = PatternMatchingEventHandler(["*"], None, False, True)

    def on_event(event):
        if verbose:
            print("Detected changes! Rebuilding...")
        build(buildDir, clean, verbose, debug)

    change_handler.on_created = on_event
    change_handler.on_moved = on_event
    change_handler.on_deleted = on_event
    change_handler.on_modified = on_event

    observer = Observer()
    observer.schedule(change_handler, "./source/", recursive=True)

    build(buildDir, clean, verbose, debug)

    observer.start()
    httpd = None
    try:
        if server:

            class Handler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=buildDir, **kwargs)

            httpd = socketserver.TCPServer(("", 8000), Handler)
            print("Starting server on localhost:8000...")
            server = httpd
            httpd.serve_forever()
        else:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        if httpd:
            print("Stopping the server...")
            httpd.server_close()


def main():
    args = init()
    if args.server:
        args.auto = True
    if args.auto:
        autobuild(args.output, args.clean, args.verbose, args.debug, args.server)
    else:
        build(args.output, args.clean, args.verbose, args.debug)


if __name__ == "__main__":
    main()
