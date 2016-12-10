from .datatypes import PositionDataObject, FrameDataObject
from .utils import filesystem

from .image import Image

class Subtexture(object):
	__slots__ = ('_name', '_image', '_position')

	def __init__(self, name, image, position=None):
		super(Subtexture, self).__init__()
		self._name = name
		self._image = image
		self._position = position
		return

	@property
	def name(self):
		return self._name

	@property
	def image(self):
		return self._image

	@property
	def position(self):
		return self._position

	def place_image(self, position):
		self._position = PositionDataObject(*position)
		return

	@classmethod
	def load_image(sclass, name, home_path='.'):
		return sclass(name, Image.load_file(filesystem.name2path(name, home_path) + '.png'), None)

	def save_image(self, home_path='.'):
		self._image.save_file(filesystem.name2path(self._name, home_path) + '.png')
		return

	@classmethod
	def load_atlas(sclass, image, frame):
		return sclass(frame.name, image.crop_subtexture(frame.box), frame.position)

	def save_atlas(self, image):
		if self._position is None:
			raise RuntimeError('Subtexture could not be saved in atlas - position is not specified.')
		frame = FrameDataObject(self._name, self._position.x, self._position.y, self._image.width, self._image.height)
		image.paste_subtexture(self._image, frame.box)
		return frame

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return NotImplemented
		return self._name == other.name and self._image == other.image and self._position == other.position

	def __repr__(self):
		return '{}(name={!r}, image={!r}, position={!r})'.format(self.__class__.__name__, self._name, self._image, self._position)
