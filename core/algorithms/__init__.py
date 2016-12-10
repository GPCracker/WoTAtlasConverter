from .compact import CompactAlgorithmCanvas, CompactAlgorithmSettings

_processors = {
	'compact': CompactAlgorithmCanvas,
	'default': CompactAlgorithmCanvas
}

_settings = {
	'compact': CompactAlgorithmSettings,
	'default': CompactAlgorithmSettings
}

class UniversalCanvas(object):
	__slots__ = ('_canvas', )

	def __init__(self, algorithm='default', settings=None):
		self._canvas = _processors[algorithm](settings)
		return

	@property
	def width(self):
		return self._canvas.width

	@property
	def height(self):
		return self._canvas.height

	def allocate(self, frame_width, frame_height):
		return self._canvas.allocate(frame_width, frame_height)

def UniversalSettings(algorithm='default', **kwargs):
	return _settings[algorithm](**kwargs)
