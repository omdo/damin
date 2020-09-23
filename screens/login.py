from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty

Builder.load_string('''
<LoginScreen>:
	app: app
	BoxLayout:
		orientation: 'vertical'
		MDToolbar:
			title: 'Login'
		FloatLayout:
			MDRaisedButton:
				pos_hint: {'center_x': .5, 'center_y': .5}
				text: 'Login'
				on_release: root.login()
''')

class LoginScreen(Screen):
	app = ObjectProperty()

	def login(self):
		self.manager.switch_to(self.app.screens.main)