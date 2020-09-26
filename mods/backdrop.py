from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivymd.theming import ThemableBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDToolbar

Builder.load_string(
    """
<CustomBackdrop>
    header_size: header_button.height
    canvas:
        Color:
            rgba:
                root.theme_cls.primary_color if not root.background_color \
                else root.background_color
        Rectangle:
            pos: self.pos
            size: self.size

    MDBackdropToolbar:
        id: toolbar
        title: root.title
        elevation: 0
        md_bg_color:
            root.theme_cls.primary_color if not root.background_color \
            else root.background_color
        left_action_items: root.left_action_items
        right_action_items: root.right_action_items
        pos_hint: {'top': 1}

    _BackLayer:
        id: back_layer
        y: -toolbar.height
        padding: dp(20), 0, dp(20), toolbar.height + dp(10)

    _FrontLayer:
        id: _front_layer
        md_bg_color: 0, 0, 0, 0
        orientation: "vertical"
        size_hint_y: None
        height: root.height - toolbar.height
        padding: root.padding

        canvas:
            Color:
                rgba: root.theme_cls.bg_normal
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius:
                    [
                    (root.radius, root.radius),
                    (0, 0),
                    (0, 0),
                    (0, 0)
                    ]

        OneLineListItem:
            id: header_button
            # text: root.header_text
            # divider: 'Inset'
            _no_ripple_effect: True
            on_press: root.open()
            MDLabel:
                text: root.header_text
                # theme_text_color: 'Custom'
                # text_color: app.theme_cls.primary_dark
                halign: 'left'
                valign: 'middle'
                pos_hint: {'center_y': .5}
                x: root.radius

        BoxLayout:
            id: front_layer
            padding: 0, "1dp", 0, 0
"""
)


class CustomBackdrop(ThemableBehavior, FloatLayout):
    padding = ListProperty([0, 0, 0, 0])
    left_action_items = ListProperty()
    right_action_items = ListProperty()
    title = StringProperty()
    background_color = ListProperty()
    radius = NumericProperty(25)
    header = BooleanProperty(True)
    header_text = StringProperty("Header")
    close_icon = StringProperty("close")
    _open_icon = ""
    _front_layer_open = BooleanProperty(False)
    _header_text = 'Template Items:'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_open")
        self.register_event_type("on_close")
        Clock.schedule_once(
            lambda x: self.on_left_action_items(self, self.left_action_items)
        )

    def on__front_layer_open(self, inst, value):
        if not hasattr(self.ids.toolbar, 'softy'):
            self.ids.toolbar.softy = self.ids.toolbar._soft_shadow_a
        if not hasattr(self.ids.toolbar, 'hardy'):
            self.ids.toolbar.hardy = self.ids.toolbar._hard_shadow_a
        soft = self.ids.toolbar.softy if value else 0
        hard = self.ids.toolbar.hardy if value else 0
        # Animation(_soft_shadow_a=soft, _hard_shadow_a=hard, d=.5, t='out_quad').start(self.ids.toolbar)

    def on_open(self):
        """When the front layer drops."""

    def on_close(self):
        """When the front layer rises."""

    def on_left_action_items(self, instance, value):
        if value:
            self.left_action_items = [value[0]]
        else:
            self.left_action_items = [["menu", lambda x: self.open()]]
        self._open_icon = self.left_action_items[0][0]

    def on_header(self, instance, value):
        if not value:
            self.ids._front_layer.remove_widget(self.ids.header_button)

    def open(self, open_up_to=0):
        """
        Opens the front layer.

        :open_up_to:
            the height to which the front screen will be lowered;
            if equal to zero - falls to the bottom of the screen;
        """

        self.animtion_icon_menu()
        if self._front_layer_open:
            self.close()
            return
        if open_up_to:
            y = open_up_to
        else:
            y = dp(100) - self.height
        Animation(y=y, d=0.2, t="out_quad").start(self.ids._front_layer)
        self._front_layer_open = True
        self.dispatch("on_open")

    def close(self):
        """Opens the front layer."""

        Animation(y=0, d=0.2, t="out_quad").start(self.ids._front_layer)
        self._front_layer_open = False
        self.dispatch("on_close")

    def animtion_icon_menu(self):
        icon_menu = self.ids.toolbar.ids.left_actions.children[0]
        anim = Animation(opacity=0, d=0.2, t="out_quad")
        anim.bind(on_complete=self.animtion_icon_close)
        anim.start(icon_menu)

    def animtion_icon_close(self, instance_animation, instance_icon_menu):
        instance_icon_menu.icon = (
            self.close_icon
            if instance_icon_menu.icon == self._open_icon
            else self._open_icon
        )
        Animation(opacity=1, d=0.2).start(instance_icon_menu)

    def add_widget(self, widget, index=0, canvas=None):
        if widget.__class__ in (MDBackdropToolbar, _BackLayer, _FrontLayer):
            return super().add_widget(widget)
        else:
            if widget.__class__ is MDBackdropBackLayer:
                self.ids.back_layer.add_widget(widget)
            elif widget.__class__ is MDBackdropFrontLayer:
                self.ids.front_layer.add_widget(widget)


class MDBackdropToolbar(MDToolbar):
    pass


class MDBackdropFrontLayer(BoxLayout):
    pass


class MDBackdropBackLayer(BoxLayout):
    pass


class _BackLayer(BoxLayout):
    pass


class _FrontLayer(MDCard):
    pass