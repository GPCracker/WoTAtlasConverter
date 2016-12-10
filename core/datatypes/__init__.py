import collections

class PositionDataObject(collections.namedtuple('PositionDataObject', ('x', 'y'))):
	__slots__ = ()

	def __new__(sclass, x=0, y=0):
		return super(PositionDataObject, sclass).__new__(sclass, x, y)

class SizeDataObject(collections.namedtuple('SizeDataObject', ('width', 'height'))):
	__slots__ = ()

	def __new__(sclass, width=0, height=0):
		return super(SizeDataObject, sclass).__new__(sclass, width, height)

class BoxDataObject(collections.namedtuple('PositionDataObject', ('left', 'top', 'right', 'bottom'))):
	__slots__ = ()

	def __new__(sclass, left=0, top=0, right=0, bottom=0):
		return super(BoxDataObject, sclass).__new__(sclass, left, top, right, bottom)

class FrameDataObject(collections.namedtuple('FrameDataObject', ('name', 'x', 'y', 'width', 'height'))):
	__slots__ = ()

	def __new__(sclass, name, x=0, y=0, width=0, height=0):
		return super(FrameDataObject, sclass).__new__(sclass, name, x, y, width, height)

	@property
	def position(self):
		return PositionDataObject(self.x, self.y)

	@property
	def size(self):
		return SizeDataObject(self.width, self.height)

	@property
	def box(self):
		return BoxDataObject(self.x, self.y, self.x + self.width, self.y + self.height)
