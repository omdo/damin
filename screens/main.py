from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty
from mods.backdrop import MDBackdropFrontLayer
from kivy.uix.recycleview import RecycleView
from mods.list import CustomOneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.button import MDFlatButton

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

<DialogOption>:
	MDLabel:
		text: root._text
		theme_text_color: root.theme_text_color
		text_color: root.text_color
		pos_hint: {'center_x': .5, 'center_y': .5}
		halign: 'center'
		valign: 'middle'
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
					'callback': self.rw.front_callback,
					'divider': None,
					'bg_color': [1, 1, 1, 1]
				}
				for x in range(100)
			]

class DialogOption(OneLineIconListItem):
	divider = StringProperty('Full', allownone=True)
	theme_text_color = 'Custom'
	_text = StringProperty()

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
			print('FIX ME!! #REFRESH')
			return
		self.manager.switch_to(screen)

	def option_callback(self, btn, item):
		self.dialog.dismiss()
		if btn._text == 'Edit':
			print(item, 'Edited')
			print('FIX ME!!')
		elif btn._text == 'Remove':
			self.open_remove_dialog(item)

	def remove_callback(self, btn):
		if btn.text == 'OK':
			print(self.remove_dialog.item, 'deleted')
			print('FIX ME!!')
		self.remove_dialog.dismiss()
		self.dialog.open()

	def open_remove_dialog(self, item):
		if not hasattr(self, 'remove_dialog'):
			self.remove_dialog = MDDialog(
				auto_dismiss=False,
				text='This item will be deleted, continue?',
				buttons=[
					MDFlatButton(text='Cancel', on_release=self.remove_callback),
					MDFlatButton(text='OK', on_release=self.remove_callback, text_color=[1, 0, 0, 1])
				]
			)
		self.remove_dialog.item = item
		self.remove_dialog.open()

	def front_callback(self, item):
		if not hasattr(self, 'dialog'):
			self.dialog = MDDialog(
				auto_dismiss=False,
				type='simple',
				items=[
					DialogOption(_text='Edit', on_release=lambda x: self.option_callback(x, item)),
					DialogOption(_text='Remove', text_color=[1, 0, 0, 1], on_release=lambda x: self.option_callback(x, item)),
					DialogOption(_text='Cancel', divider=None, on_release=lambda x: self.option_callback(x, item)),
				]
			)
		self.dialog.open()