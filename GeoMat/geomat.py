import csv
import os
import pickle

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatIconButton, MDRectangleFlatButton, MDFlatButton, MDRaisedButton, \
    MDIconButton
from kivy.uix.scrollview import ScrollView
from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDList, OneLineRightIconListItem, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.effects.scroll import ScrollEffect
from kivy.metrics import dp
from kivy.utils import platform
from datetime import datetime


class MenuScreen(Screen):
    name = 'menu'

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=[10, 10, 10, 0], spacing=30)
        ab_button = MDRectangleFlatIconButton(text='DODAJ ODWIERT', pos_hint={'center_x': 0.5, 'center_y': 0.75},
                                              size_hint=(.8, 1), line_width=2, font_size='24sp',
                                              on_press=ab_change_screen)
        ed_button = MDRectangleFlatIconButton(text='EXPORTUJ DANE', pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                              size_hint=(.8, 1), line_width=2, font_size='24sp',
                                              on_press=ed_change_screen)
        ds_button = MDRectangleFlatIconButton(text='LISTA OTWORÓW', pos_hint={'center_x': 0.5, 'center_y': 0.25},
                                              size_hint=(.8, 1), line_width=2, font_size='24sp',
                                              on_press=ds_change_screen)
        home_label = MDLabel(text='MENU GŁÓWNE', halign='center', center_x=0.5, padding=2, size_hint=(1, .7),
                             theme_text_color='Custom', text_color='#2196f3', font_style='H4')

        version_label = MDLabel(text=f'Version: {version}', halign='center', theme_text_color='Hint',
                                center_x=0.5, padding=2, size_hint=(1, .3))

        layout.add_widget(home_label)
        layout.add_widget(ds_button)
        layout.add_widget(ab_button)
        layout.add_widget(ed_button)
        layout.add_widget(version_label)
        self.add_widget(layout)
        return


class AddBoreholeScreen(Screen):
    name = 'add_borehole'
    names_list = ['nazwa otworu', 'głębokość', 'początek wiercenia', 'koniec wiercenia', 'rzędna', 'kilometraż',
                  'wsp x (lat)', 'wsp y (lon)', 'układ współrzędnych', 'obiekt', 'miejscowość', 'system wiercenia',
                  'wiertnica', 'cel wiercenia', 'dozorca', 'nadzorca', 'wykonawca wiercenia']
    csv_names_list = ['nazwa', 'glebokosc', 'data_pocz', 'data_konc', 'z', 'kilometraz',
                      'x', 'y', 'cs', 'obiekt', 'miejsce', 'system_wiercenia', 'wiertnica',
                      'cel_wiercenia', 'dozorca', 'nadzorca', 'wykonawca_w']
    user_input_list = []
    used_layers = []
    borehole_to_edit = None
    as_edit = False
    btn_to_remove = None

    def __init__(self, **kwargs):
        super(AddBoreholeScreen, self).__init__(**kwargs)
        self.data_dict = None
        self.menu_field = None
        self.edit_layer_button = None
        self.scroll = ScrollView()
        self.scroll.effect_cls = ScrollEffect
        layout = MDGridLayout(cols=1, adaptive_height=True, spacing=10, padding=(10, 10, 10, 10),
                              row_default_height=dp(90))
        self.fields_layout = MDGridLayout(cols=1, adaptive_height=True, spacing=10, row_default_height=dp(50))

        add_layer_button = MDRectangleFlatButton(text='DODAJ WARSTWĘ', size_hint=(1, 1), line_width=1.2,
                                                 font_size='20sp')
        submit_button = MDRectangleFlatButton(text='ZAPISZ', size_hint=(1, 1), line_width=1.2,
                                              font_size='20sp')
        back_to_menu_button = MDRectangleFlatButton(text='WRÓĆ DO MENU', size_hint=(1, 1), line_width=1.2,
                                                    font_size='20sp')

        def all_fields_builder():
            self.field1 = self.text_field_builder(self.names_list[0])
            self.field2 = self.text_field_builder(self.names_list[1])
            self.field3 = self.text_field_builder(self.names_list[2])
            self.field4 = self.text_field_builder(self.names_list[3])
            self.field5 = self.text_field_builder(self.names_list[4])
            self.field6 = self.text_field_builder(self.names_list[5])
            self.field7 = self.text_field_builder(self.names_list[6])
            self.field8 = self.text_field_builder(self.names_list[7])
            self.field9 = self.text_field_builder(self.names_list[8])
            self.field10 = self.text_field_builder(self.names_list[9])
            self.field11 = self.text_field_builder(self.names_list[10])
            self.field12 = self.text_field_builder(self.names_list[11])
            self.field13 = self.text_field_builder(self.names_list[12])
            self.field14 = self.text_field_builder(self.names_list[13])
            self.field15 = self.text_field_builder(self.names_list[14])
            self.field16 = self.text_field_builder(self.names_list[15])
            self.field17 = self.text_field_builder(self.names_list[16])

            # add all fields to layout
            for i in range(len(self.names_list)):
                i += 1
                name = f"self.field{i}"
                self.fields_layout.add_widget(eval(name))

        all_fields_builder()

        add_layer_button.bind(on_press=al_change_screen)
        submit_button.bind(on_press=self.save_data)
        back_to_menu_button.bind(on_press=return_to_menu)

        layout.add_widget(self.fields_layout)
        layout.add_widget(add_layer_button)
        layout.add_widget(submit_button)
        layout.add_widget(back_to_menu_button)
        self.scroll.add_widget(layout)
        self.add_widget(self.scroll)

        Window.softinput_mode = 'below_target'
        return

    def on_pre_enter(self, *args):
        """loads borehole data"""
        if self.as_edit:
            self.remove_buttons()
            AddBoreholeScreen.as_edit = False
            children_list = list(self.fields_layout.children)
            children_list.reverse()
            i = 0
            for textfield_child in children_list:
                borehole_data = main_data_dict[self.borehole_to_edit]
                borehole_data = list(borehole_data.values())
                textfield_child.text = borehole_data[i]
                i += 1

            # loads buttons
            for layer in main_layer_data_dict:
                ldict = main_layer_data_dict[layer]
                borehole_tag = ldict.get('nazwa otworu')
                if borehole_tag == self.borehole_to_edit:
                    self.edit_layer_button = MDRectangleFlatButton(text=f'{layer}', size_hint=(1, 1),
                                                                   on_press=self.enter_layer_edit)
                    self.fields_layout.add_widget(self.edit_layer_button)
                    self.used_layers.append(layer)

        # prepopulates date fields
        frmt_current_date = datetime.now().strftime("%y-%m-%d")
        if self.field3.text == '':
            self.field3.text = frmt_current_date
        if self.field4.text == '':
            self.field4.text = frmt_current_date

    def on_enter(self, *args):
        """ removes or adds layers buttons """
        if self.btn_to_remove:
            self.remove_one_button(btn_to_remove=self.btn_to_remove)
            AddBoreholeScreen.btn_to_remove = None
        try:
            for l_name in AddLayerScreen.layers_names:
                if l_name not in self.used_layers:
                    self.edit_layer_button = MDRectangleFlatButton(text=f'{l_name}', size_hint=(1, 1),
                                                                   on_press=self.enter_layer_edit)
                    self.fields_layout.add_widget(self.edit_layer_button)
                    self.used_layers.append(l_name)
        except Exception as e:
            print(e)
        self.scroll.scroll_to(self.field1)

    def enter_layer_edit(self, instance):
        """ enter selected edit layer view """
        layer_to_edit = instance.text
        AddLayerScreen.layer_to_edit = layer_to_edit
        AddLayerScreen.as_edit = True
        al_change_screen()

    def text_field_builder(self, field_name):
        """ initializes text input widget """
        frmt_current_date = datetime.now().strftime("%y-%m-%d")
        if field_name == self.names_list[8]:
            self.text_field = MDTextField(hint_text=f'{field_name.upper()}',
                                          mode='rectangle',
                                          size_hint=(1, None),
                                          )
            menu_list = ['geograficzny', 'lokalny', 'PUWG 2000', 'PUWG 1992', 'PUWG 1980']
            menu_items = [
                {
                    "viewclass": "OneLineListItem",
                    "height": dp(45),
                    "text": f"{i}",
                    "on_release": lambda x=f"{i}": self.set_item(x),
                }
                for i in menu_list
            ]
            self.menu_field = MDDropdownMenu(
                caller=self.text_field,
                items=menu_items,
                position='auto',
                elevation=0,
                radius=[16, 16, 16, 16],
                background_color='#ade2e6',
                ver_growth="down",
                hor_growth="left",
                width_mult=2.2,
            )
            self.text_field.bind(focus=self.menu_open)

        elif field_name == self.names_list[2]:
            self.text_field = MDTextField(hint_text=f'{field_name.upper()}',
                                          text=frmt_current_date,
                                          mode='rectangle',
                                          size_hint=(1, None),
                                          )

        elif field_name == self.names_list[3]:
            self.text_field = MDTextField(hint_text=f'{field_name.upper()}',
                                          text=frmt_current_date,
                                          mode='rectangle',
                                          size_hint=(1, None),
                                          )
        else:
            self.text_field = MDTextField(hint_text=f'{field_name.upper()}',
                                          mode='rectangle',
                                          size_hint=(1, None),
                                          id=f'{field_name}'
                                          )

        self.text_field.bind(focus=self.on_focus)
        return self.text_field

    def set_item(self, text__item):
        self.field9.text = text__item
        self.menu_field.dismiss()

    def menu_open(self, *args):
        if self.field9.focus:
            self.menu_field.open()

    def on_focus(self, instance, value):
        if value:
            self.scroll.scroll_to(instance)
            if instance.text == 'NAZWA NIE MOŻE BYĆ PUSTA':
                instance.text = ''

    def save_inputs(self):
        """ generates list of user answers for each field """
        for i in range(len(self.names_list)):
            i += 1
            name = f"self.field{i}"
            answer = eval(name)
            self.user_input_list.append(answer.text)
        return self.user_input_list

    def save_data(self, *args):
        """ validates if borehole data can be saved then saves data """
        if self.field1.text != '':
            self.save_inputs()

            self.data_dict = dict(zip(self.csv_names_list, self.user_input_list))

            borehole_name = self.user_input_list[0]

            self.add_tag_to_layer(borehole_name)
            self.upd_names_list(borehole_name)

            main_data_dict.update({f'{borehole_name}': self.data_dict})

            self.clear_text_fields()

            self.remove_buttons()

            self.used_layers = []
            AddLayerScreen.layers_names = []
            self.user_input_list = []
            return_to_menu()

        else:
            self.scroll.scroll_to(self.field1)
            self.field1.text = 'NAZWA NIE MOŻE BYĆ PUSTA'

        return

    def remove_buttons(self):
        """ removes all buttons """
        id_list = []

        # counts how many layer buttons were added
        for children in self.fields_layout.children:
            if isinstance(children, MDRectangleFlatButton):
                id_list.append(id(children))

        if id_list:
            iterations = self.calculate_iterations(len(id_list))
            # removes buttons
            for i in range(iterations):
                for children in self.fields_layout.children:
                    if id(children) in id_list:
                        self.fields_layout.remove_widget(children)
                        id_list.remove(id(children))

    def remove_one_button(self, btn_to_remove):
        """ removes go to layer button """
        for children in self.fields_layout.children:
            if isinstance(children, MDRectangleFlatButton) and children.text == btn_to_remove:
                self.fields_layout.remove_widget(children)

    def add_tag_to_layer(self, borehole_name):
        """ adds borehole tag (name) to layer for further identification """
        for lr in AddLayerScreen.layers_names:
            layer = main_layer_data_dict[lr]
            layer.update({'nazwa otworu': f'{borehole_name}'})

    def calculate_iterations(self, z):
        """ calculates how many times it is needed to remove all buttons """
        i = 1
        if z == 1:
            pass
        else:
            while True:
                z = z // 2
                if z != 1:
                    i += 1
                    continue
                else:
                    i += 1
                    break
        return i

    def upd_names_list(self, borehole_name):
        if borehole_name not in list_of_boreholes:
            list_of_boreholes.append(borehole_name)

    def clear_text_fields(self):
        for i in range(len(self.names_list)):
            i += 1
            name = f"self.field{i}"
            field = eval(name)
            field.text = ''


class AddLayerScreen(Screen):
    name = 'add_layer'
    layer_names_list = ['nazwa warstwy', 'strop', 'symbol gruntu głównego', 'opis litologiczny', 'stratygrafia',
                        'geneza', 'wałeczkowanie', 'stan gruntu', 'wilgotność', 'zawartość CaCO3']
    user_inputs = []
    layers_names = []
    layer_to_edit = None
    as_edit = False

    def __init__(self, **kwargs):
        super(AddLayerScreen, self).__init__(**kwargs)
        self.menu_field = None
        self.delete_button = None
        self.scroll = ScrollView(always_overscroll=False)
        self.scroll.effect_cls = ScrollEffect
        self.layout = MDGridLayout(cols=1, adaptive_height=True, spacing=10, padding=(10, 10, 10, 10),
                                   rows_minimum={10: dp(100), 11: dp(100)})
        self.box_layout = MDBoxLayout(orientation='horizontal')

        back_to_borehole_button = MDRectangleFlatButton(text='WRÓĆ', size_hint=(1, 1), line_width=1.2,
                                                        font_size='20sp')
        submit_button = MDRectangleFlatButton(text='ZAPISZ', size_hint=(1, 1), line_width=1.2, font_size='20sp')

        def all_fields_builder():
            self.field1 = self.field_builder(self.layer_names_list[0])
            self.field2 = self.field_builder(self.layer_names_list[1])
            self.field3 = self.field_builder(self.layer_names_list[2])
            self.field4 = self.field_builder(self.layer_names_list[3])
            self.field5 = self.field_builder(self.layer_names_list[4])
            self.field6 = self.field_builder(self.layer_names_list[5])
            self.field7 = self.field_builder(self.layer_names_list[6])
            self.field8 = self.field_builder(self.layer_names_list[7])
            self.field9 = self.field_builder(self.layer_names_list[8])
            self.field10 = self.field_builder(self.layer_names_list[9])

        all_fields_builder()

        for i in range(len(self.layer_names_list)):
            i += 1
            name = f"self.field{i}"
            self.layout.add_widget(eval(name))

        back_to_borehole_button.bind(on_press=ab_change_screen)

        submit_button.bind(on_press=self.save_data)

        self.box_layout.add_widget(back_to_borehole_button)

        self.layout.add_widget(self.box_layout)
        self.layout.add_widget(submit_button)
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)

        Window.softinput_mode = 'below_target'

    def on_pre_enter(self, *args):
        """loads layer data"""
        if self.as_edit:
            AddLayerScreen.as_edit = False
            children_list = list(self.layout.children)
            children_list.reverse()
            del children_list[-2:]
            i = 0
            for textfield_child in children_list:
                layer_data = main_layer_data_dict[self.layer_to_edit]
                layer_data = list(layer_data.values())
                textfield_child.text = layer_data[i]
                i += 1

            self.delete_button = MDIconButton(icon='delete-forever', size_hint=(0.3, 1), icon_size='50sp',
                                              theme_icon_color='Custom', icon_color='#2196f3', )
            self.delete_button.bind(on_press=self.open_confirm_delete_dialog)
            self.box_layout.add_widget(self.delete_button)
        else:
            self.clear_text_fields()

    def on_enter(self, *args):
        self.scroll.scroll_to(self.field1)

    def field_builder(self, field_name):
        """ initializes text input widget """
        if field_name == self.layer_names_list[3]:
            self.field = MDTextField(hint_text=f'{field_name.upper()}',
                                     mode='rectangle',
                                     size_hint=(1, None),
                                     multiline=True)
        elif field_name == self.layer_names_list[9]:
            self.field = MDTextField(hint_text=f'ZAWARTOŚĆ CaCO3',
                                     mode='rectangle',
                                     size_hint=(1, None),
                                     )

            menu_list = ['<1', 1, 2, 3, 4, 5]
            menu_items = [
                {
                    "viewclass": "OneLineListItem",
                    "height": dp(45),
                    "text": f"{i}",
                    "on_release": lambda x=f"{i}": self.set_item(x),
                }
                for i in menu_list
            ]
            self.menu_field = MDDropdownMenu(
                caller=self.field,
                items=menu_items,
                position='auto',
                elevation=0,
                radius=[16, 16, 16, 16],
                background_color='#ade2e6',
                ver_growth="down",
                hor_growth="left",
                width_mult=2,
            )
            self.field.bind(focus=self.menu_open)
        else:
            self.field = MDTextField(hint_text=f'{field_name.upper()}',
                                     mode='rectangle',
                                     size_hint=(1, None))
        self.field.bind(focus=self.on_focus)
        return self.field

    def set_item(self, text__item):
        self.field10.text = text__item
        self.menu_field.dismiss()

    def menu_open(self, *args):
        if self.field.focus:
            self.menu_field.open()

    def on_focus(self, instance, value):
        if value:
            self.scroll.scroll_to(instance)
            if instance.text == 'NAZWA NIE MOŻE BYĆ PUSTA':
                instance.text = ''

    def save_inputs(self):
        for i in range(len(self.layer_names_list)):
            i += 1
            name = f"self.field{i}"
            answer = eval(name)
            self.user_inputs.append(answer.text)
        return self.user_inputs

    def clear_text_fields(self):
        for i in range(len(self.layer_names_list)):
            i += 1
            name = f"self.field{i}"
            field = eval(name)
            field.text = ''

    def save_data(self, *args):
        """ saves user input data """
        if self.field1.text != '':
            print('nie pusta')
            self.save_inputs()
            self.clear_text_fields()

            layer_name = self.user_inputs[0]

            self.layers_names.append(layer_name)

            layer_data_dict = dict(zip(self.layer_names_list, self.user_inputs))
            main_layer_data_dict.update({f'{layer_name}': layer_data_dict})

            print(main_layer_data_dict)
            self.user_inputs = []
            ab_change_screen()
        else:
            self.field1.text = 'NAZWA NIE MOŻE BYĆ PUSTA'
            self.scroll.scroll_to(self.field1)

    def delete_layer(self, *args):
        """ deletes layer """
        AddBoreholeScreen.btn_to_remove = self.layer_to_edit
        print(self.layer_to_edit)
        del main_layer_data_dict[self.layer_to_edit]
        if self.layer_to_edit in self.layers_names:
            self.layers_names.remove(self.layer_to_edit)
        self.clear_text_fields()
        ab_change_screen()

    def open_confirm_delete_dialog(self, *args):
        confirm_delete_dialog = MDDialog(title=f'Czy na pewno usunąć warstwę?',
                                         elevation=0,
                                         buttons=[
                                             MDFlatButton(text='ANULUJ'),
                                             MDRaisedButton(text='USUŃ', elevation=0)
                                         ])
        btn1 = confirm_delete_dialog.buttons[0]
        btn2 = confirm_delete_dialog.buttons[1]
        btn1.bind(on_press=confirm_delete_dialog.dismiss)
        btn2.bind(on_press=self.delete_layer)
        btn2.bind(on_press=confirm_delete_dialog.dismiss)
        confirm_delete_dialog.open()

    def on_leave(self, *args):
        try:
            self.box_layout.remove_widget(self.delete_button)
        except AttributeError as ae:
            pass


class ExportDataScreen(Screen):
    name = 'export_data'
    list_of_added_boreholes = []
    selected_boreholes_keys = []

    def __init__(self, **kwargs):
        frmt_current_date = datetime.now().strftime("%y%m%d")
        super(ExportDataScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=[10, 0, 10, 10], spacing=10)
        back_to_menu_button = MDRectangleFlatButton(text='Wroć do menu',
                                                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                                    size_hint=(1, 0.1),
                                                    line_width=1.2,
                                                    font_size='20sp'
                                                    )
        export_data_button = MDRectangleFlatButton(text='Exportuj dane do pliku.csv',
                                                   pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                                   size_hint=(1, 0.1),
                                                   line_width=1.2,
                                                   font_size='20sp'
                                                   )
        self.name_file_input = MDTextField(hint_text='Nazwa pliku', text=f'otwory_geomat_{frmt_current_date}',
                                           mode='rectangle')

        self.boreholes_table = MDDataTable(pos_hint={'center_x': 0.5, 'center_y': 1},
                                           size_hint=(1, 0.4),
                                           check=True,
                                           elevation=0,
                                           column_data=[
                                               ("Nazwa otworu", dp(80)),
                                               ("", dp(0))
                                           ],
                                           row_data=[]
                                           )

        export_data_button.bind(on_press=self.export_data)
        back_to_menu_button.bind(on_press=return_to_menu)
        layout.add_widget(self.boreholes_table)
        layout.add_widget(self.name_file_input)
        layout.add_widget(back_to_menu_button)
        layout.add_widget(export_data_button)
        self.add_widget(layout)
        Window.softinput_mode = 'below_target'
        return

    def on_pre_enter(self, *args):
        for borehole_name in list_of_boreholes:
            if borehole_name not in self.list_of_added_boreholes:
                self.boreholes_table.add_row((borehole_name, ''))
                self.list_of_added_boreholes.append(borehole_name)

    def get_row_checks(self):
        checked_rows = self.boreholes_table.get_row_checks()
        for row in checked_rows:
            self.selected_boreholes_keys.append(row[0])

    def export_data_to_csv(self):
        """ saves selected data to csv file """
        try:
            if not self.selected_boreholes_keys:
                raise Exception

            csv_file_name = f'{self.name_file_input.text}.csv'
            if platform == "android":
                file_path = f'/storage/emulated/0/Documents/{csv_file_name}'
            else:
                file_path = f'{os.getcwd()}/{csv_file_name}'

            csv_layer_names_list = AddLayerScreen.layer_names_list.copy()
            csv_layer_names_list.append('nazwa otworu')

            with open(file_path, 'w', newline='', encoding='utf8') as file_open:
                b_writer = csv.DictWriter(file_open, delimiter='|', fieldnames=AddBoreholeScreen.csv_names_list)
                l_writer = csv.DictWriter(file_open, delimiter='|', fieldnames=csv_layer_names_list)
                # write boreholes header and all data
                b_writer.writeheader()
                for b_key in self.selected_boreholes_keys:
                    if b_key in main_data_dict:
                        b_writer.writerow(main_data_dict[b_key])

                # write layers header and all data
                if main_layer_data_dict != {}:
                    l_writer.writeheader()
                    for l_key in main_layer_data_dict:
                        for b_key in self.selected_boreholes_keys:
                            if b_key in main_layer_data_dict[l_key].values():
                                l_writer.writerow(main_layer_data_dict[l_key])

            self.name_file_input.text = ''
            self.show_success_dialog(file_path)

        except Exception:
            self.show_fail_dialog()

    def show_fail_dialog(self, *args):
        fail_dialog = MDDialog(title=f'Nie udało się zapisać pliku',
                               md_bg_color='#ff3333', elevation=0)
        fail_dialog.open()

    def show_success_dialog(self, file_path, *args):
        success_dialog = MDDialog(title=f'Pomyślnie zapisano plik w {file_path}',
                                  md_bg_color='#66fa66', elevation=0)
        success_dialog.open()

    def export_data(self, *args):
        """ integrates export data tasks """
        self.get_row_checks()
        self.export_data_to_csv()


    def on_leave(self, *args):
        self.selected_boreholes_keys = []


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    """Custom right container."""


class DraftSavesScreen(Screen):
    name = 'draft_saves'
    list_of_added_boreholes = []
    list_of_added_drafts = []
    checks = []

    def __init__(self, **kwargs):
        super(DraftSavesScreen, self).__init__(**kwargs)

        self.field = None
        screen = Screen()

        self.scroll = ScrollView()

        self.boreholes_register = MDList()

        self.content = MDGridLayout(cols=1, adaptive_height=True)

        self.scroll.add_widget(self.content)

        self.return_to_menu_button = MDRectangleFlatButton(text='WRÓĆ DO MENU',
                                                           pos_hint={'center_x': 0.4, 'center_y': 0.05},
                                                           size_hint=(0.8, 0.1),
                                                           padding=['0dp', '8dp'],
                                                           line_width=0.1,
                                                           font_size='24sp',
                                                           md_bg_color='#2196f3',
                                                           text_color='#ffffff',
                                                           line_color='#2196f3'
                                                           )

        self.delete_button = MDIconButton(icon='delete-forever',
                                          icon_size='50sp',
                                          pos_hint={'center_x': 0.9, 'center_y': 0.05},
                                          size_hint=(0.2, 0.1),
                                          )

        self.return_to_menu_button.bind(on_press=return_to_menu)
        self.delete_button.bind(on_press=self.open_confirm_delete_dialog)

        self.content.add_widget(self.boreholes_register)

        screen.add_widget(self.scroll)
        screen.add_widget(self.delete_button)
        screen.add_widget(self.return_to_menu_button)

        self.add_widget(screen)

    def on_pre_enter(self, *args):
        """if any - loads boreholes as list items"""
        for b_name in list_of_boreholes:
            if b_name not in self.list_of_added_boreholes:
                bfield = self.field_builder(b_name)
                self.boreholes_register.add_widget(bfield)
                self.list_of_added_boreholes.append(b_name)

    def field_builder(self, name):
        self.field = OneLineRightIconListItem(text=f'{name}', id=f'field-{name}', on_press=self.enter_edit)
        checkbox = RightCheckbox(on_press=self.on_checkbox_active, id=f'{name}')
        self.field.add_widget(checkbox)
        return self.field

    def on_checkbox_active(self, checkbox):
        if checkbox in self.checks:
            self.checks.remove(checkbox)
        else:
            self.checks.append(checkbox)

    def delete_checked_boreholes(self, *args):
        """deletes items from list view"""
        if self.checks:
            for obj in self.checks:
                md_list = obj.parent.parent.parent
                md_list_item = obj.parent.parent
                md_list.remove_widget(md_list_item)
            self.delete_from_database()
            self.checks = []

    def delete_from_database(self):
        """ deletes selected boreholes with corresponding layers """
        layers_to_del = []
        for obj in self.checks:
            check_id = obj.id
            if check_id in main_data_dict:
                del main_data_dict[check_id]
                list_of_boreholes.remove(check_id)

            for layer_key in main_layer_data_dict:
                layer_dict = main_layer_data_dict[layer_key]
                layer_data = layer_dict.values()
                if check_id in layer_data:
                    layers_to_del.append(layer_key)
        for x in layers_to_del:
            del main_layer_data_dict[x]

    def open_confirm_delete_dialog(self, *args):
        confirm_delete_dialog = MDDialog(title=f'Czy na pewno usunąć {len(self.checks)} otworów?',
                                         elevation=0,
                                         buttons=[
                                             MDFlatButton(text='ANULUJ'),
                                             MDRaisedButton(text='USUŃ', elevation=0)
                                         ])
        btn1 = confirm_delete_dialog.buttons[0]
        btn2 = confirm_delete_dialog.buttons[1]
        btn1.bind(on_press=confirm_delete_dialog.dismiss)
        btn2.bind(on_press=self.delete_checked_boreholes)
        btn2.bind(on_press=confirm_delete_dialog.dismiss)
        confirm_delete_dialog.open()

    def enter_edit(self, instance):
        borehole_to_edit = instance.text
        AddBoreholeScreen.borehole_to_edit = borehole_to_edit
        AddBoreholeScreen.as_edit = True
        ab_change_screen()


class GeoMatApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mldd_path = None
        self.mdd_path = None
        self.lob_path = None

    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(MenuScreen(name='menu'))
        screen_manager.add_widget(AddBoreholeScreen(name='add_borehole'))
        screen_manager.add_widget(AddLayerScreen(name='add_layer'))
        screen_manager.add_widget(ExportDataScreen(name='export_data'))
        screen_manager.add_widget(DraftSavesScreen(name='draft_saves'))

        return screen_manager

    def on_start(self):
        try:
            self.lob_path = f'{self.user_data_dir}/user_local_data-list_of_boreholes.pickle'
            self.mdd_path = f'{self.user_data_dir}/user_local_data-main_data_dict.pickle'
            self.mldd_path = f'{self.user_data_dir}/user_local_data-main_layer_data_dict.pickle'
            self.load_data()
        except FileNotFoundError as errno2:
            print(errno2)

    def on_pause(self):
        self.save_data()
        return True

    def on_stop(self):
        if platform == 'win':
            self.save_data()

    def save_data(self):
        """Saves the data to a pickle file for reuse later."""
        with open(self.lob_path, 'wb') as lob_file:
            pickle.dump(list_of_boreholes, lob_file)

        with open(self.mdd_path, 'wb') as mdd_file:
            pickle.dump(main_data_dict, mdd_file)

        with open(self.mldd_path, 'wb') as mldd_file:
            pickle.dump(main_layer_data_dict, mldd_file)

    def load_data(self):
        """Loads data from a pickle file"""
        try:
            with open(self.lob_path, 'rb') as file:
                boreholes = pickle.load(file)
                for bh in boreholes:
                    list_of_boreholes.append(bh)
        except EOFError as error:
            print(error)

        try:
            with open(self.mdd_path, 'rb') as file:
                data_dict = pickle.load(file)
                main_data_dict.update(data_dict)
        except EOFError as error:
            print(error)

        try:
            with open(self.mldd_path, 'rb') as file:
                layer_data_dict = pickle.load(file)
                main_layer_data_dict.update(layer_data_dict)
        except EOFError as error:
            print(error)


def ab_change_screen(*args):
    app = MDApp.get_running_app()
    app.root.current = 'add_borehole'


def ed_change_screen(*args):
    app = MDApp.get_running_app()
    app.root.current = 'export_data'


def ds_change_screen(*args):
    app = MDApp.get_running_app()
    app.root.current = 'draft_saves'


def al_change_screen(*args):
    app = MDApp.get_running_app()
    app.root.current = 'add_layer'


def return_to_menu(*args):
    app = MDApp.get_running_app()
    app.root.current = 'menu'


################################################################################
list_of_boreholes = []

main_data_dict = {}

main_layer_data_dict = {}

version = '1.1'

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

GeoMatApp().run()
