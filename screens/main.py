from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty
from mods.backdrop import MDBackdropFrontLayer
from kivy.uix.recycleview import RecycleView
from mods.list import CustomOneLineListItem, SelectableListItem
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
		MDBackdropBackLayer:
			BackLayer:
				id: back_layer
				rw: root
		MDBackdropFrontLayer:
			md_bg_color: .5, .5, .5, 1
			FrontLayer:
				id: front_layer
				rw: root

<FrontLayer>:
	viewclass: 'CustomOneLineListItem'
	RecycleBoxLayout:
		id: box
		padding: 10
		spacing: 8
		default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<BackLayer>:
	viewclass: 'SelectableListItem'
	RecycleBoxLayout:
		id: box
		padding: 10
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
			self.data = [
				{
					'text': f'List Item {x+1}',
					'num': x+1,
					'callback': self.rw.front_callback,
					'divider': None,
					'bg_color': [1, 1, 1, 1]
				}
				for x in range(100)
			]

	def remove_data(self, num):
		removed = None
		for data in self.data:
			if data['num'] == num:
				removed = data
				break

		if removed == None:
			return print(num, 'not found ?')

		self.data.remove(removed)
		self.data = sorted(self.data, key=lambda x: x['num'])

class BackLayer(RecycleView):
	rw = ObjectProperty()

	def on_rw(self, inst, value):
		if value:
			templates = ['Program', 'Tamu', 'Keuangan', 'Rapat', 'Kerja']
			self.data = [
				{
					'text': f'Buku {templates[i]}',
					'num': 1,
					'callback': self.rw.back_callback,
				}
				for i in range(len(templates))
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
			return print('FIX ME!! #REFRESH')
		self.manager.switch_to(screen)


	def remove_callback(self, btn, num):
		self.remove_dialog.dismiss()
		if btn.text == 'OK':
			self.ids.front_layer.remove_data(num)
			return
		self.dialog.open()

	def open_remove_dialog(self, num):
		if not hasattr(self, 'remove_dialog'):
			self.remove_dialog = MDDialog(
				auto_dismiss=False,
				text='This item will be deleted, continue?',
				buttons=[
					MDFlatButton(text='Cancel'),
					MDFlatButton(text='OK', text_color=[1, 0, 0, 1])
				]
			)
		for button in self.remove_dialog.buttons:
			if not hasattr(button, 'last_bound'):
				button.last_bound = None
			if button.last_bound != None:
				button.unbind_uid('on_release', button.last_bound)
			button.last_bound = button.fbind('on_release', lambda x: self.remove_callback(x, num))
		self.remove_dialog.open()

	def option_callback(self, btn, num):
		self.dialog.dismiss()
		if btn._text == 'Edit':
			print(btn, 'Edited')
			print('FIX ME!!')
		elif btn._text == 'Remove':
			self.open_remove_dialog(num)

	def front_callback(self, item):
		num = int(item.num)
		if not hasattr(self, 'dialog'):
			self.dialog = MDDialog(
				auto_dismiss=False,
				type='simple',
				items=[
					DialogOption(_text='Edit'),
					DialogOption(_text='Remove', text_color=[1, 0, 0, 1]),
					DialogOption(_text='Cancel', divider=None),
				]
			)
		for option in self.dialog.items:
			if not hasattr(option, 'last_bound'):
				option.last_bound = None
			if option.last_bound != None:
				option.unbind_uid('on_release', option.last_bound)
			option.last_bound = option.fbind('on_release', lambda x: self.option_callback(x, num))
		self.dialog.open()

	def back_callback(self, item):
		print(item.text, 'selected')