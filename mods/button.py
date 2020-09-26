from kivymd.uix.button import MDFloatingActionButton
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.animation import Animation

Builder.load_string('''
<CustomFAB>
	icon: 'arrow-up'
	elevation: 10
	elevation_normal: 10
''')

class CustomFAB(MDFloatingActionButton):
	is_showing = BooleanProperty()

	def on_is_showing(self, inst, value):
		if not hasattr(self, 'orig_y'):
			self.orig_y = self.y
		y = self.orig_y if value else 0 - self.height
		Animation(y=y, d=.2, t='out_cubic').start(self)