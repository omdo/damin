from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string('''
<AccountScreen>:
	BoxLayout:
		orientation: 'vertical'
		MDToolbar:
			title: 'Account'
			elevation: 10
			right_action_items: [['arrow-left-circle', lambda x: root.manager.back()]]
		Widget:
''')

class AccountScreen(Screen):
	pass