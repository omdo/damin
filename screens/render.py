from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.properties import ObjectProperty, ListProperty
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window

Builder.load_string('''
<RenderScreen>
    name: 'render'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            id: tb
            title: 'RENDER'
        Widget:
''')

class RenderScreen(Screen):
    app = ObjectProperty()
    data = ListProperty()
    data_tables = ObjectProperty()
        
    def on_data(self, inst, values):
        column = []
        rows = []
        for value in values:
            row = []
            for k, v in value.items():
                col = (k, dp(30))
                if not col in column:
                    column.append(col)
                row.append(v)
            rows.append(tuple(row))

        self.data_tables = MDDataTable(
            auto_dismiss=False,
            background='',
            background_color=[0, 0, 0, 0],
            overlay_color=[0, 0, 0, 0],
            size_hint_y=(Window.height - self.ids.tb.height) / Window.height,
            pos_hint={'top': (Window.height - self.ids.tb.height) / Window.height},
            rows_num=len(rows),
            column_data=column,
            row_data=rows,
        )

    def on_enter(self):
        def pre_enter(i):
            self.data_tables = MDDataTable(
                rows_num=50,
                column_data=[
                    ("No.", dp(30)),
                    ("Column 1", dp(30)),
                    ("Column 2", dp(30)),
                    ("Column 3", dp(30)),
                    ("Column 4", dp(30)),
                    ("Column 5", dp(30)),
                ],
                row_data=[
                    (f"{i + 1}", "2.23", "3.65", "44.1", "0.45", "62.5")
                    for i in range(50)
                ]
            )
            self.data_tables.bind(on_dismiss=self.on_data_table_dismiss)
            self.data_tables.open()
        if not self.data_tables:
            Clock.schedule_once(pre_enter, 0)
        else:
            self.data_tables.open()