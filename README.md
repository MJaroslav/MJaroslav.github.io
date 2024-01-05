# MJaroslav.github.io

Personal site with info and connections.

---

This site has custom builder and auto deploy on GitHub Pages by commits in master branch. You can use this repository as pattern for your own site.

## How to build site

### Requirements

- Python 3.10
    - Some python libraries in [requirements](requirements.txt) file.

### Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Site editing

All site sources contains in `source` directory.
Edit [pattern.html](source/pattern.html) with your information and configure some things in [config.json](source/config.json). For using your links and music then configure [music.json](source/data/music.json) and [profiles.json](source/data/profiles.json), music image root folder is [source/assets/media/music](source/assets/media/music).

Configuration values:

- `static`: add directories and files for copy to site.
- `index`: you can set your own pattern file name.
- `replace`: map with key-value replacements for pattern file.
    - Use `debug` and `!debug` for placing `true`/`false` value of `--debug` builder argument.

### Building

Just run build script:

```bash
python build.py
```

By default, site will build in `_site` directory.

You can run this command with `--help` parameter for show all command arguments.

### Runtime site editing

You can run local web server with file change listener in source folder:

```bash
python build.py --clean --server
```

### Deploy

Just push to `master` branch and [action](.github/workflows/build-and-deploy.yml) will build and deploy site from `_site` directory to `gh-pages` branch.

## Post Scriptum

Feel free to correct typos and errors in the text or code :)
