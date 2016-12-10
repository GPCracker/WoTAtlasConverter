import os
import sys
import glob

def norm_path(path):
	return os.path.normpath(path).replace(os.sep, '/') or '.'

def encode(ustr):
	return ustr.encode(sys.getfilesystemencoding())

def decode(fstr):
	return unicode(fstr, encoding=sys.getfilesystemencoding())

def name2path(name, home_path='.'):
	return norm_path(os.path.join(home_path, encode(name)))

def path2name(path, home_path='.'):
	return decode(norm_path(os.path.relpath(path, home_path)))

def create_dirs(dst_path):
	dst_dir = norm_path(os.path.dirname(dst_path))
	if not os.path.isdir(dst_dir):
		os.makedirs(dst_dir)
	return

def find_subtextures_iterator(wildcards=('.', ), home_path='.'):
	for wildcard in wildcards:
		for subtexture_path in glob.iglob(wildcard):
			if os.path.isfile(subtexture_path):
				if os.path.splitext(subtexture_path)[1] == '.png':
					yield path2name(os.path.join(os.path.splitext(subtexture_path)[0]), home_path)
			elif os.path.isdir(subtexture_path):
				for root, dirs, files in os.walk(subtexture_path):
					for file in files:
						if os.path.splitext(file)[1] == '.png':
							yield path2name(os.path.join(root, os.path.splitext(file)[0]), home_path)
	return
