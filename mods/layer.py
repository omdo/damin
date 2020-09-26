from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from .list import CustomOneLineListItem, SelectableListItem

Builder.load_string('''
#:import ScrollEffect kivy.effects.scroll.ScrollEffect
<FrontLayer>:
	viewclass: 'CustomOneLineListItem'
	effect_cls: ScrollEffect
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
''')

class FrontLayer(RecycleView):
	rw = ObjectProperty()

	def on_rw(self, inst, value):
		def oo(i):
			self.data = self.rw.template_data
		self.data = []
		Clock.schedule_once(oo, .2)

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

		if self.rw.template_data != self.data:
			self.rw.template_data = self.data

class BackLayer(RecycleView):
	rw = ObjectProperty()

	def on_rw(self, inst, value):
		if value:
			templates = ['Program', 'Tamu', 'Keuangan', 'Rapat', 'Kerja']
			self.data = [
				{
					'text': f'Buku {templates[i]}',
					'template': templates[i],
					'num': i+1,
					'callback': self.rw.back_callback,
				}
				for i in range(len(templates))
			]

			data = self.data
			for i in range(len(data)):
				data[i]['template_data'] = [
					{
						'text': f"{data[i]['text']} Item {x}",
						'num': x+1,
						'callback': self.rw.front_callback,
					}
					for x in range(100)
				]

			self.data = data