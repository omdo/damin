from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string('''
<AboutScreen>:
	BoxLayout:
		orientation: 'vertical'
		MDToolbar:
			title: 'About'
			elevation: 10
			right_action_items: [['arrow-left-circle', lambda x: root.manager.back()]]
		Widget:
''')

class AboutScreen(Screen):
	pass