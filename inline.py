#!/usr/bin/env python3
import re
import urllib.parse
import json
import sys
import inspect

INLINE_PATTERN = r"```((.|\n)*?)```"
SHIELDS_BADGE = "https://img.shields.io/badge"
SHIELDS_CURSE = "https://img.shields.io/curseforge"
SHIELDS_STARS = "https://img.shields.io/github/stars"
JITPACK = "https://jitpack.io"
CURSE_MOD = "https://www.curseforge.com/minecraft/mc-mods"
GITHUB = "https://github.com"
PATTERNS = {}


def get(name: str):
    return PATTERNS[name]


def conf(name: str):
    result = PATTERNS["config"]
    for el in name.split("."):
        result = result[el]
    return result


def is_debug():
    return PATTERNS["debug"]

def join(sep: str, *args: str) -> str:
    return sep.join(args)


def tooltip(text: str) -> str:
    return f'data-html="true" data-toggle="tooltip" title="{text}"'


def gh(url: str) -> str:
    return f'<a class="text-secondary" href="{GITHUB}/{url}">{url}</a>'


def notnone(target, html: str) -> str:
    return html.replace("@IT@", target if type(target) is str else str(target)) if target else ""


def orelse(target, html: str, else_html: str) -> str:
    return html.replace("@IT@", target if type(target) is str else str(target)) if target else else_html


def jitpack(owner: str, project: str) -> str:
    return f'<a href="{JITPACK}/#{owner}/{project}"><img alt="Version from JitPack" src="{JITPACK}/v/{owner}/{project}.svg"></a>'


def curse_dl(project_id: str) -> str:
    return f'<img alt="Downloads from CurseForge" src="{SHIELDS_CURSE}/dt/{project_id}?logo=curseforge&label=Downloads&color=orange">'


def curse(slug: str, project_id: str) -> str:
    return f'<a {tooltip(f"Click for see files on CurseForge")} href="{CURSE_MOD}/{slug}/files"><img alt="Version from CurseForge" src="{SHIELDS_CURSE}/v/{project_id}?logo=curseforge&label=CurseForge&color=orange"></a>'


def stars(owner: str, project: str) -> str:
    return f'<a {tooltip(f"Click for open GitHub stargazers")} href="{GITHUB}/{owner}/{project}/stargazers"><img alt="GitHub stargs" src="{SHIELDS_STARS}/{owner}/{project}"></a>'


def thing(
    name: str, color: str, logo_color: str = None, logo: str = None, desc: str = None
) -> str:
    encoded = __encode_badge_param__(name)
    if not logo and name == encoded:
        logo = name
    desc = f"-{__encode_badge_param__(desc)}" if desc else ""
    logo = f"?logo={logo.lower()}" if logo else ""
    logo_color = f"&logoColor={logo_color}" if logo_color and logo else ""
    return f'<img alt="{name}" src="{SHIELDS_BADGE}/{encoded}{desc}-{color}{logo}{logo_color}">'


def __encode_badge_param__(param) -> str:
    if type(param) is not str:
        str(param)
    return urllib.parse.quote_plus(
        param.replace("-", "--").replace("_", "__").replace(" ", "_")
    )


def __get_allowed_funcs__():
    self = sys.modules[__name__]
    funcs = filter(
        lambda e: not e[0].startswith("_"), inspect.getmembers(self, inspect.isfunction)
    )
    result = {}
    for func in funcs:
        result[func[0]] = func[1]
    del result["compile"]
    del result["load"]
    del result["load_patterns"]
    del result["inject_config"]
    return result


def compile(raw_text: str) -> str:
    return re.compile(INLINE_PATTERN).sub(
        lambda code: str(eval(code.group(1), {}, __get_allowed_funcs__())), raw_text
    )


def apply(element):
    if type(element) is list:
        return [apply(e) for e in element]
    elif type(element) is dict:
        return {k: apply(v) for k, v in element.items()}
    elif type(element) is str:
        return compile(element)
    else:
        return element


def load(path) -> str:
    with open(path, "r") as file:
        return compile(file.read())


def load_patterns(debug: bool):
    global PATTERNS
    with open("./source/inline.json", "r") as file:
        PATTERNS = json.load(file)
    PATTERNS["debug"] = debug


def inject_config(config: dir):
    global PATTERNS
    PATTERNS["config"] = config
