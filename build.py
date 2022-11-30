#!/usr/bin/env python3
import argparse
import sys
import shutil
from bs4 import BeautifulSoup as bs
import json
from datetime import date


def init():
    parser = argparse.ArgumentParser(add_help=True,
                                     description="Builder for MJaroslav.github.io site, but you can use it too.")
    parser.add_argument("-o", "--output", metavar="PATH",
                        default="_site", help='set build output directory. Default is "_site".')
    parser.add_argument("-c", "--clean", action="store_true",
                        help="Clean output directory before build.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show more information about building.")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Mark build as debug, its will disable visit counter and similar things.")
    return parser.parse_args(sys.argv[1:])


def build(buildDir, clean, verbose, debug):
    def log(text):
        if (verbose):
            print(text)
    log(f"Build directory is {buildDir}")
    if clean:
        log("Clean build directory...")
        shutil.rmtree(f"./{buildDir}", ignore_errors=True)
    log("Building...")

    for static in ["media", "fonts", "scripts", "styles"]:
        log(f"Copying static {static} data...")
        shutil.copytree(f"./source/{static}",
                        f"./{buildDir}/{static}", dirs_exist_ok=True)

    log("Opening pattern.html...")
    html = open("./source/pattern.html")
    soup = bs(html, 'html.parser')

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
                "title": tooltip
            }
            link = soup.new_tag("a", **attrs)
            soup.find("div", class_="profiles").append(link)
            log(f"Created profile entry {e['name']}")

    log("Adding music...")
    with open("./source/data/music.json", "r") as file:
        music = json.load(file)
        for e in music:
            attrs = {
                "class": "music-entry p-3",
                "href": e["url"]
            }
            link = soup.new_tag("a", **attrs)
            tooltip = e["name"]
            if "tooltip" in e:
                tooltip += f"<br><br>{e['tooltip']}"
            attrs = {
                "data-html": "true",
                "data-toggle": "tooltip",
                "title": tooltip,
                "alr": e["name"],
                "src": f"media/music/{e['image']}",
                "class": "col music-entry-image p-0 rounded-circle border"
            }
            img = soup.new_tag("img", **attrs)
            link.append(img)
            soup.find("div", class_="music").append(link)
            log(f"Created music entry {e['name']}")

    log("Setting current year...")
    soup.find("p", id="year").string = str(date.today().year)

    log("Writting formatted pattern to index.html...")
    with open(f"./{buildDir}/index.html", "w") as file:
        text = str(soup)
        log("Toggle visit counter...")
        text = text.replace("@COUNTER@", str(not bool(debug)))
        file.write(text)

    log("Done!")


def main():
    args = init()
    build(args.output, args.clean, args.verbose, args.debug)


if __name__ == "__main__":
    main()
