# WoT Atlas Converter

WoT Atlas Converter is a python script that could be used to assemble or disassemble WoT png texture atlases.

*Important: Pillow need to be installed on your system, otherwise exception will be raised. XML is processed by standard ElementTree.*

## Installation

Script does not requires any "installation" and could just be downloaded and run.
However, it will raise an import exception unless [Pillow is installed](https://pillow.readthedocs.io/en/3.4.x/installation.html).

To run bash script directly (if you are a Linux user) set executable permission first:

	$ chmod u+x atlscnv

Bash script just run a python one. It is only a shortcut for `python atlscnv.py`, last could be used both Windows and Linux.

## Usage

**To disassemble an atlas run**

	$ atlscnv disassemble --atlas-path <atlas-path> --subtexture-path <subtexture-path> <atlas-name>

Where `<atlas-name>` is a name of atlas, `<atlas-path>` is a path where atlas is located.
Atlas consists of 2 files, `*.png` and `*.xml`, so these 2 parts are required, however `<atlas-path>` and `<subtexture-path>` defaults are a current directory.
Atlas will be read from files `<atlas-path>/<atlas-name>.png` and `<atlas-path>/<atlas-name>.xml`.

This atlas implementation support slashes in subtexture names, and they are described as folders.
So item with name `<folder>/<name>` will be saved as `<subtexture-path>/<folder>/<name>.png`.

**Atlases also could be assembled by command**

	$ atlscnv assemble --subtexture-path <subtexture-path> --atlas-path <atlas-path> <atlas-name> <subtextures>

Where `<subtextures>` is a sequence of subtextures paths, wildcards is also supported.
To calculate proper subtexture names `<subtexture-path>` is used.
Image named `<subtexture-path>/<folder>/<name>.png` will be saved in atlas as `<folder>/<name>`.
Atlas itself - as `<atlas-path>/<atlas-name>.png`.

*There are a few more parameters described in help.*
