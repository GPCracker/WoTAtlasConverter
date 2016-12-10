#!/usr/bin/env python

import sys
import argparse

from core import converter

ustr = lambda name: unicode(name, encoding=sys.getfilesystemencoding())

parser = argparse.ArgumentParser(
	description='Atlas converter is a tool for assemble or disassemble WoT png texture atlases.'
)
subparsers = parser.add_subparsers(
	metavar='action',
	dest='action',
	help='conversion type'
)
parser_assemble = subparsers.add_parser(
	'assemble',
	help='assemble atlas from subtextures',
	description='Assembler for WoT atlases.'
)
parser_assemble.add_argument(
	'--subtexture-path',
	action='store',
	metavar='path',
	dest='subtexture_path',
	type=str,
	default='.',
	help='subtextures base path (calculate subtexture name relative to)'
)
parser_assemble.add_argument(
	'--atlas-path',
	action='store',
	metavar='path',
	dest='atlas_path',
	type=str,
	default='.',
	help='atlas base path (store atlas using its name relative to)'
)
parser_assemble.add_argument(
	'--sort',
	action='store',
	metavar='method',
	dest='sort',
	type=str,
	choices=['width', 'height', 'side', 'area', 'default'],
	default='default',
	help='subtexture sorting method'
)
parser_assemble.add_argument(
	'--algorithm',
	action='store',
	metavar='packer',
	dest='algorithm',
	type=str,
	choices=['compact', 'default'],
	default='default',
	help='subtexture placement algorithm'
)
parser_assemble.add_argument(
	'--width',
	action='store',
	metavar='width',
	dest='width',
	type=int,
	default=0,
	help='atlas width (if not overflowed)'
)
parser_assemble.add_argument(
	'--height',
	action='store',
	metavar='height',
	dest='height',
	type=int,
	default=0,
	help='atlas height (if not overflowed)'
)
parser_assemble.add_argument(
	'atlas_name',
	action='store',
	metavar='atlas',
	type=ustr,
	help='atlas name'
)
parser_assemble.add_argument(
	'subtextures',
	action='store',
	metavar='subtexture',
	nargs='+',
	default='.',
	help='subtexture(s) to save in atlas'
)
parser_disassemble = subparsers.add_parser(
	'disassemble',
	help='disassemble atlas to subtextures',
	description='Disassembler for WoT atlases.',
)
parser_disassemble.add_argument(
	'atlas_name',
	action='store',
	metavar='atlas_name',
	type=ustr,
	help='atlas name'
)
parser_disassemble.add_argument(
	'--atlas-path',
	action='store',
	metavar='path',
	dest='atlas_path',
	type=str,
	default='.',
	help='atlas base path (calculate atlas path using its name relative to)'
)
parser_disassemble.add_argument(
	'--subtexture-path',
	action='store',
	metavar='path',
	dest='subtexture_path',
	type=str,
	default='.',
	help='subtextures base path (store subtexture using its name relative to)'
)

args = parser.parse_args()
print args

if args.action == 'assemble':
	converter.assemble(
		args.atlas_name,
		args.subtextures,
		args.subtexture_path,
		args.atlas_path,
		args.sort,
		args.algorithm,
		args.width,
		args.height
	)
elif args.action == 'disassemble':
	converter.disassemble(
		args.atlas_name,
		args.atlas_path,
		args.subtexture_path
	)
