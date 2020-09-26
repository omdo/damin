from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty, BooleanProperty
from mods.dialog import CustomDialog, DialogOption
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
from kivy.animation import Animation

Builder.load_string('''
#:import CustomBackdrop mods.backdrop.CustomBackdrop
#:import CustomFAB mods.button.CustomFAB
#:import FrontLayer mods.layer.FrontLayer
#:import BackLayer mods.layer.BackLayer
<MainScreen>:
	CustomBackdrop:
		id: backdrop
		right_action_items: root.right_menu
		header_text: 'Buku ' + root.current_template.template + ':' if root.current_template else 'Select Template'
		on_open:
			self.header_text = ''
			root.on_front_open(True)
		on_close:
			self.header_text = 'Buku ' + root.current_template.template + ':' if root.current_template else 'No template selected, pick one.'
			root.on_front_open(False)
		MDBackdropBackLayer:
			BackLayer:
				id: back_layer
				rw: root
		MDBackdropFrontLayer:
			md_bg_color: .5, .5, .5, 1
			FrontLayer:
				id: front_layer
	CustomFAB:
		id: fab
		md_bg_color: app.theme_cls.primary_color
		pos: root.width - self.width - dp(25), dp(25)
		on_release: root.fab_callback(self)
''')
class MainScreen(Screen):
	right_menu = ListProperty()
	current_template = ObjectProperty()
	backdrop_elevation = NumericProperty(0)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.right_menu = [
			['account-circle', lambda x: self.menu_callback(x)],
			['alert-circle', lambda x: self.menu_callback(x)]
		]
		self.ids.front_layer.bind(scroll_y=self.on_front_scroll)

	def on_current_template(self, inst, value):
		if value:
			if 'refresh-circle' in [x[0] for x in self.right_menu]:
				return
			btn = ['refresh-circle', lambda x: self.menu_callback(x)]
			self.right_menu.insert(0, btn)
		else:
			if 'refresh-circle' in [x[0] for x in self.right_menu]:
				for menu in self.right_menu:
					if menu[0] == 'refresh-circle':
						self.right_menu.remove(menu)

	def on_front_open(self, value):
		opacity = 0 if value else 1
		Animation(opacity=opacity, d=.2, t='out_cubic').start(self.ids.fab)

	def on_front_scroll(self, inst, value):
		if value < .98:
			if self.ids.fab.is_showing:
				return
			self.ids.fab.is_showing = True
		else:
			if not self.ids.fab.is_showing:
				return
			self.ids.fab.is_showing = False

	def fab_callback(self, fab):
		Animation(scroll_y=1, d=.5, t='out_cubic').start(self.ids.front_layer)

	def menu_callback(self, btn):
		if btn.icon == 'account-circle':
			screen = self.manager.app.screens.account
		elif btn.icon == 'alert-circle':
			screen = self.manager.app.screens.about
		else:
			render_screen = self.manager.app.screens.render
			render_screen.data = [
				{
					'No': x,
					'Nama': 'Fajar',
					'Nama2': 'Jiwandono',
					'Alamat': 'Mawar1',
					'Pekerjaan': 'santuy'
				}
				for x in range(1, 21)
			]
			return self.manager.switch_to(render_screen)
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
				radius=[20, 20, 20, 20],
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
			self.dialog = CustomDialog(
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
		def after_open(i):
			self.current_template = item
			self.ids.front_layer.rw = item
		self.ids.backdrop.open()
		Clock.schedule_once(after_open, .1)

	def on_pre_enter(self):
		self.ids.fab.is_showing = False

	def on_enter(self):
		def enter(i):
			if self.ids.backdrop._front_layer_open:
				self.ids.backdrop.open()
				return
			if not self.current_template:
				self.ids.backdrop.open()
		Clock.schedule_once(enter, .2)