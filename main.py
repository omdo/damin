from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.clock import Clock
from screens import Screens
from functools import partial
from kivy.utils import platform

if platform == 'android':
	from jnius import autoclass, cast
	from android.runnable import run_on_ui_thread
	Toast = autoclass('android.widget.Toast')
	activity = autoclass('org.kivy.android.PythonActivity').mActivity
	AndroidString = autoclass('java.lang.String')

KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
<CustomScreenManager>

CustomScreenManager:
	app: app
	transition: FadeTransition(duration=.2, clearcolor=app.theme_cls.primary_dark)
	Screen:
		name: 'Dummy'
'''

class CustomScreenManager(ScreenManager):
	last = None
	app = ObjectProperty()

	def switch_to(self, screen, **kwargs):
		self.last = self.current_screen
		super().switch_to(screen, **kwargs)
		if self.current_screen == self.app.screens.main:
			self.last = None

	def back(self):
		if self.last:
			if self.current_screen == self.app.screens.render:
				self.current_screen.data_tables.dismiss()	
			self.switch_to(self.last)
			return True
		else:
			return self.app.trigger_exit()

class DaminApp(MDApp):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.root = Builder.load_string(KV)
		self.screens = Screens()
		self.is_exit = False
		Window.bind(on_keyboard=self.on_back_button)

	def on_back_button(self, window, key, *args):
		if key == 27:
			return self.root.back()

	def trigger_exit(self):
		if self.root.current_screen.ids.backdrop._front_layer_open:
			self.root.current_screen.ids.backdrop.open()
			return True
		if self.is_exit:
			return False
		self.is_exit = True
		Clock.schedule_once(lambda delta: setattr(self, 'is_exit', False), 1.5)
		self.toast('Press again to exit')
		return True

	def toast(self, message):
		if platform == 'android':
			@run_on_ui_thread
			def _toast(message):
				Toast.makeText(
					activity,
					cast('java.lang.CharSequence', AndroidString(message)),
					Toast.LENGTH_SHORT
				).show()
			return _toast(message)

		else:
			print(message)

	def build(self):
		self.theme_cls.primary_palette = 'Teal'
		return self.root

	def on_start(self):
		def login(i):
			self.root.switch_to(self.screens.login)
		Clock.schedule_once(login, .2)

if __name__ == '__main__':
	DaminApp().run()