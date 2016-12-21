import io
import codecs

from xml.etree.ElementTree import XML, XMLParser, Element, ElementTree, TreeBuilder

from .datatypes import FrameDataObject
from .utils import filesystem

class LayoutElement(Element):
	__slots__ = ()

	@classmethod
	def create_new(sclass, tag, text=None, tail=None, parent=None, *args, **kwargs):
		element = sclass(tag, *args, **kwargs)
		if text is not None:
			element.text = text
		if tail is not None:
			element.tail = tail
		if parent is not None:
			parent.append(element)
		return element

	def prettify(self, level=0):
		indent = u'\n' + level * u'\t'
		if len(self):
			if not self.text or not self.text.strip():
				self.text = indent + u'\t'
			if not self.tail or not self.tail.strip():
				self.tail = indent
			for element in self:
				element.prettify(level + 1)
			if not element.tail or not element.tail.strip():
				element.tail = indent
		elif not self.tail or not self.tail.strip():
			self.tail = indent
		return

class LayoutTree(ElementTree):
	__slots__ = ()

	_element = LayoutElement

	def __init__(self, *args, **kwargs):
		super(LayoutTree, self).__init__(*args, **kwargs)
		return

	def prettify(self):
		self.getroot().prettify()
		return

	def tostring(self):
		with io.BytesIO() as content_io:
			self.write(content_io, encoding='utf-8')
			content = unicode(content_io.getvalue(), encoding='utf-8')
		return content

	@classmethod
	def load_file(sclass, layout_path):
		with codecs.open(layout_path, 'r', 'utf-8-sig') as layout:
			root = XML(layout.read().encode('utf-8'), XMLParser(target=TreeBuilder(sclass._element)))
		root.prettify()
		return sclass(root)

	def save_file(self, layout_path):
		filesystem.create_dirs(layout_path)
		with codecs.open(layout_path, 'w', 'utf-8-sig') as layout:
			layout.write(self.tostring())
		return

	@classmethod
	def from_frames(sclass, frames):
		root = sclass._element.create_new('root')
		for frame in frames:
			subtexture = sclass._element.create_new(u'SubTexture', parent=root)
			sclass._element.create_new(u'name', parent=subtexture, text=unicode(frame.name))
			sclass._element.create_new(u'x', parent=subtexture, text=unicode(frame.x))
			sclass._element.create_new(u'y', parent=subtexture, text=unicode(frame.y))
			sclass._element.create_new(u'width', parent=subtexture, text=unicode(frame.width))
			sclass._element.create_new(u'height', parent=subtexture, text=unicode(frame.height))
		root.prettify()
		return sclass(root)

	def get_frames(self):
		return [FrameDataObject(
			name=unicode(subtexture.find(u'name').text.strip()),
			x=int(subtexture.find(u'x').text.strip()),
			y=int(subtexture.find(u'y').text.strip()),
			width=int(subtexture.find(u'width').text.strip()),
			height=int(subtexture.find(u'height').text.strip())
		) for subtexture in self.iterfind(u'SubTexture')]
