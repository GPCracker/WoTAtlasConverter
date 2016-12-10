from .algorithms import UniversalSettings
from .utils import filesystem
from .atlas import Atlas

def _assemble(atlas_name, subtexture_names, subtexture_path='.', atlas_path='.', sort='default', algorithm='default', width=0, height=0):
	settings = UniversalSettings(algorithm, width=width, height=height)
	atlas = Atlas.load_subtextures(atlas_name, subtexture_names, subtexture_path, sort, algorithm, settings)
	atlas.save_file(atlas_path)
	return

def assemble(atlas_name, subtextures, subtexture_path='.', atlas_path='.', sort='default', algorithm='default', width=0, height=0):
	subtexture_names_iterator = filesystem.find_subtextures_iterator(subtextures, subtexture_path)
	return _assemble(atlas_name, subtexture_names_iterator, subtexture_path, atlas_path, sort, algorithm, width, height)

def disassemble(atlas_name, atlas_path='.', subtexture_path='.'):
	atlas = Atlas.load_file(atlas_name, atlas_path)
	atlas.save_subtextures(subtexture_path)
	return
