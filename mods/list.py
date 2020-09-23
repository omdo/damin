from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, ILeftBodyTouch
from kivymd.uix.behaviors import RectangularElevationBehavior, TouchBehavior
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.core.window import Window

Builder.load_string('''
<CustomOneLineListItem>:
	elevation: 5
	Lefty:
		size_hint: 1, 1
		MDFlatButton
			_no_ripple_effect: True
			size_hint: 1, 1
			text: str(root.index)
			font_size: '19sp'
		MDSeparator:
			orientation: 'vertical'
			color: .7, .7, .7, .1
			width: dp(4)
''')

class Lefty(MDBoxLayout, ILeftBodyTouch):
	pass

class CustomOneLineListItem(OneLineIconListItem, RectangularElevationBehavior, TouchBehavior):
	callback = ObjectProperty()
	index = NumericProperty()

	def on_release(self):
		self.callback(self)