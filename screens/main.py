from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

Builder.load_string('''
#:import CustomBackdrop mods.backdrop.CustomBackdrop
<MainScreen>:
	CustomBackdrop:
		id: backdrop
		right_action_items: root.right_menu
		header_text: root.current_template


''')
class MainScreen(Screen):
	right_menu = ListProperty()
	current_template = StringProperty('None')

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.right_menu = [
			['refresh-circle', lambda x: self.menu_callback(x)],
			['account-circle', lambda x: self.menu_callback(x)],
			['alert-circle', lambda x: self.menu_callback(x)]
		]

	def menu_callback(self, btn):
		if btn.icon == self.right_menu[1][0]:
			screen = self.manager.app.screens.account
		elif btn.icon == self.right_menu[2][0]:
			screen = self.manager.app.screens.about
		else:
			print(btn.icon)
			return
		self.manager.switch_to(screen)