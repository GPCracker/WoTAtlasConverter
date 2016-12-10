from .algorithms import UniversalCanvas
from .utils import filesystem

from .subtexture import Subtexture
from .layout import LayoutTree
from .image import Image

class Atlas(object):
	__slots__ = ('_name', '_image', '_frames')

	def __init__(self, name, image, frames):
		super(Atlas, self).__init__()
		self._name = name
		self._image = image
		self._frames = frames
		return

	@property
	def name(self):
		return self._name

	@property
	def image(self):
		return self._image

	@property
	def frames(self):
		return self._frames

	@classmethod
	def load_file(sclass, name, home_path='.'):
		image = Image.load_file(filesystem.name2path(name, home_path) + '.png')
		frames = LayoutTree.load_file(filesystem.name2path(name, home_path) + '.xml').get_frames()
		return sclass(name, image, frames)

	def save_file(self, home_path='.'):
		self._image.save_file(filesystem.name2path(self._name, home_path) + '.png')
		LayoutTree.from_frames(self._frames).save_file(filesystem.name2path(self._name, home_path) + '.xml')
		return

	@classmethod
	def load_subtextures(sclass, atlas_name, subtexture_names, home_path='.', sort='default', algorithm='default', settings=None):
		subtextures = [Subtexture.load_image(image_name, home_path) for image_name in subtexture_names]
		if not subtextures:
			raise RuntimeError('Subtexture list should not be empty.')
		sortkey = {
			'width': lambda subtexture: subtexture.image.width,
			'height': lambda subtexture: subtexture.image.height,
			'side': lambda subtexture: subtexture.image.side,
			'area': lambda subtexture: subtexture.image.area,
			'default': lambda subtexture: subtexture.image.side,
		}[sort]
		subtextures.sort(key=sortkey, reverse=True)
		canvas = UniversalCanvas(algorithm, settings)
		for subtexture in subtextures:
			subtexture.place_image(canvas.allocate(subtexture.image.width, subtexture.image.height))
		image = Image.create_new(canvas.width, canvas.height)
		frames = [subtexture.save_atlas(image) for subtexture in subtextures]
		return sclass(atlas_name, image, frames)

	def save_subtextures(self, home_path='.'):
		for frame in self._frames:
			Subtexture.load_atlas(self._image, frame).save_image(home_path)
		return

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return NotImplemented
		return self._name == other.name and self._image == other.image and self._frames == other.frames

	def __repr__(self):
		return '{}(name={!r}, image={!r}, frames={!r})'.format(self.__class__.__name__, self._name, self._image, self._frames)
