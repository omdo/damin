from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, ILeftBodyTouch
from kivymd.uix.behaviors import RectangularElevationBehavior, TouchBehavior
from kivymd.theming import ThemableBehavior
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.core.window import Window

Builder.load_string('''
<CustomOneLineListItem>:
	elevation: 5
	Lefty:
		size_hint: 1, 1
		MDFlatButton
			_no_ripple_effect: True
			size_hint: 1, 1
			text: str(root.num)
			font_size: '19sp'
			opacity: 1 if root.with_icon else 0
		MDSeparator:
			orientation: 'vertical'
			color: .7, .7, .7, .1
			width: dp(4)
			opacity: 1 if root.with_icon else 0

<SelectableListItem>
    size_hint_y: None
    height: self.minimum_height
    spacing: "10dp"

    canvas:
        Color:
            rgba:
                root.theme_cls.primary_dark if root.selected_item \
                else root.theme_cls.primary_color
        RoundedRectangle:
            pos: self.pos
            size: self.size

    MDIconButton:
        icon: root.icon
        theme_text_color: "Custom"
        text_color: (0, 0, 0, .5) if not root.selected_item else (0, 0, 0, 1)

    MDLabel:
        text: root.text
        color: (0, 0, 0, .5) if not root.selected_item else (0, 0, 0, 1)
''')

class Lefty(MDBoxLayout, ILeftBodyTouch):
	pass

class CustomOneLineListItem(OneLineIconListItem, RectangularElevationBehavior, TouchBehavior):
	callback = ObjectProperty()
	num = NumericProperty()
	with_icon = BooleanProperty(True)

	def on_release(self):
		self.callback(self)

class SelectableListItem(ThemableBehavior, BoxLayout):
    icon = StringProperty("android")
    text = StringProperty()
    selected_item = BooleanProperty(False)
    callback = ObjectProperty(None, allownone=True)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            for item in self.parent.children:
                if item.selected_item:
                    item.selected_item = False
            self.selected_item = True
        return super().on_touch_down(touch)

    def on_selected_item(self, instance, value):
    	if self.callback:
    		if value:
    			self.callback(self)