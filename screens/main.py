from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty
from mods.backdrop import MDBackdropFrontLayer
from kivy.uix.recycleview import RecycleView
from mods.list import CustomOneLineListItem

Builder.load_string('''
#:import CustomBackdrop mods.backdrop.CustomBackdrop
<MainScreen>:
	CustomBackdrop:
		id: backdrop
		right_action_items: root.right_menu
		header_text: root.current_template
		MDBackdropFrontLayer:
			md_bg_color: .5, .5, .5, 1
			FrontLayer:
				rw: root

<FrontLayer>:
	viewclass: 'CustomOneLineListItem'
	RecycleBoxLayout:
		padding: 10
		spacing: 8
		default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')

class FrontLayer(RecycleView):
	rw = ObjectProperty()
	
	def on_rw(self, inst, value):
		if value:
			print(value)
			self.data = [
				{
					'text': f'List Item {x+1}',
					'index': x+1,
					'callback': self.btn_callback,
					'divider': None,
					'bg_color': [1, 1, 1, 1]
				}
				for x in range(100)
			]

	def btn_callback(self, btn):
		print(btn.text)

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

	def front_callback(self, btn):
		print(btn)