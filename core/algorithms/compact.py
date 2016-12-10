import copy
import operator
import collections

class CompactAlgorithmNode(object):
	__slots__ = ('x', 'y', 'width', 'height', 'is_used', 'node_down', 'node_right')

	def __init__(self, x=0, y=0, width=0, height=0, is_used=False, node_down=None, node_right=None):
		super(CompactAlgorithmNode, self).__init__()
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.is_used = is_used
		self.node_down = node_down
		self.node_right = node_right
		return

	def copy(self):
		'''
		Create a node copy.
		'''
		return copy.copy(self)

	def find(self, width, height):
		'''
		Find a node where required size could be allocated.
		'''
		if self.is_used:
			return self.node_right and self.node_right.find(width, height) or self.node_down and self.node_down.find(width, height)
		return self if self.width >= width and self.height >= height else None

	def split(self, width, height):
		'''
		Split a node into three parts to allocate required size.
		Leaves original node unchanged, but separate 2 free parts of it (after size allocation).
		'''
		assert self.width >= width and self.height >= height
		self.node_down = CompactAlgorithmNode(self.x, self.y + height, self.width, self.height - height)
		self.node_right = CompactAlgorithmNode(self.x + width, self.y, self.width - width, height)
		self.is_used = True
		return self

	def __repr__(self):
		return '{}(x={!r}, y={!r}, width={!r}, height={!r}, is_used={!r}, node_down={!r}, node_right={!r})'.format(
			self.__class__.__name__,
			self.x,
			self.y,
			self.width,
			self.height,
			self.is_used,
			self.node_down,
			self.node_right
		)

class CompactAlgorithmRoot(CompactAlgorithmNode):
	__slots__ = ()

	def acquire(self, width, height):
		'''
		Acquire free space in existing nodes, if possible.
		'''
		suitable_node = self.find(width, height)
		return suitable_node and suitable_node.split(width, height)

	def grow(self, width, height, ratio=0):
		'''
		Grow the canvas to the most appropriate direction.
		Direction is selected to add as less new space as possible.
		'''
		abs_ratio = lambda ratio: ratio if ratio >= 1.0 else 1.0 / ratio
		can_grow_down = width <= self.width
		can_grow_right = height <= self.height
		if can_grow_down:
			grow_down_width = self.width
			grow_down_height = self.height + height
			grow_down_area = grow_down_width * grow_down_height
			grow_down_ratio = operator.truediv(grow_down_width, grow_down_height)
			grow_down_rating = abs_ratio(grow_down_ratio / ratio) if ratio else grow_down_area
		if can_grow_right:
			grow_right_width = self.width + width
			grow_right_height = self.height
			grow_right_area = grow_right_width * grow_right_height
			grow_right_ratio = operator.truediv(grow_right_width, grow_right_height)
			grow_right_rating = abs_ratio(grow_right_ratio / ratio) if ratio else grow_right_area
		# Compare marks.
		if can_grow_right and (not can_grow_down or grow_right_rating <= grow_down_rating):
			return self.grow_right(width, height)
		return self.grow_down(width, height) if can_grow_down else None

	def grow_down(self, width, height):
		'''
		Grow the canvas down.
		Original node increases, separate previous space as right (as a copy), new as down.
		'''
		assert width <= self.width
		origin = self.copy()
		self.height += height
		self.node_down = CompactAlgorithmNode(origin.x, origin.y + origin.height, origin.width, height)
		self.node_right = origin
		self.is_used = True
		return self.node_down.split(width, height)

	def grow_right(self, width, height):
		'''
		Grow the canvas to the right.
		Original node increases, separate previous space as down (as a copy), new as right.
		'''
		assert height <= self.height
		origin = self.copy()
		self.width += width
		self.node_down = origin
		self.node_right = CompactAlgorithmNode(origin.x + origin.width, origin.y, width, origin.height)
		self.is_used = True
		return self.node_right.split(width, height)

class CompactAlgorithmSettings(collections.namedtuple('CompactAlgorithmSettings', ('width', 'height', 'ratio'))):
	__slots__ = ()

	def __new__(sclass, width=0, height=0, ratio=0.0):
		return super(CompactAlgorithmSettings, sclass).__new__(sclass, width, height, ratio)

	@property
	def area(self):
		return self.width * self.height

class CompactAlgorithmCanvas(object):
	__slots__ = ('_root', '_settings')

	_default_settings = CompactAlgorithmSettings(0, 0, 0.0)

	def __init__(self, settings=None):
		super(CompactAlgorithmCanvas, self).__init__()
		self._settings = settings if settings is not None else self._default_settings
		self._root = CompactAlgorithmRoot(width=self._settings.width, height=self._settings.height) if self._settings.area else None
		return

	@property
	def width(self):
		return self._root.width

	@property
	def height(self):
		return self._root.height

	def allocate(self, frame_width, frame_height):
		if not self._root:
			self._root = CompactAlgorithmRoot(width=frame_width, height=frame_height)
		allocated_node = self._root.acquire(frame_width, frame_height) or self._root.grow(frame_width, frame_height, self._settings.ratio)
		if not allocated_node:
			raise RuntimeError('Node for this frame could not be allocated.')
		return allocated_node.x, allocated_node.y

	def __repr__(self):
		return '{}(settings={!r})'.format(self.__class__.__name__, self._settings)
