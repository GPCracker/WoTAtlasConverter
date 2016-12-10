import PIL.Image

from .utils import filesystem

class Image(object):
	__slots__ = ('_data', )

	def __init__(self, data):
		super(Image, self).__init__()
		self._data = data
		return

	@property
	def data(self):
		return self._data

	@property
	def width(self):
		return self._data.size[0]

	@property
	def height(self):
		return self._data.size[1]

	@property
	def side(self):
		return max(self._data.size)

	@property
	def area(self):
		return self._data.size[0] * self._data.size[1]

	@classmethod
	def create_new(sclass, width, height):
		return sclass(PIL.Image.new('RGBA', (width, height)))

	@classmethod
	def load_file(sclass, image_path):
		with open(image_path, 'rb') as data_io:
			data = PIL.Image.open(data_io).convert('RGBA')
		return sclass(data)

	def save_file(self, image_path):
		filesystem.create_dirs(image_path)
		with open(image_path, 'wb') as data_io:
			self._data.save(data_io, format='PNG')
		return

	def crop_subtexture(self, box=None):
		return self.__class__(self._data.crop(box).copy())

	def paste_subtexture(self, image, box=None):
		self._data.paste(image.data, box)
		return

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return NotImplemented
		return self._data == other.data

	def __repr__(self):
		return '{}(data={!r})'.format(self.__class__.__name__, self._data)
