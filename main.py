import flet as ft
import getpass
import os
from pages import *
from settings import *
from utils import *
from flet import MainAxisAlignment, CrossAxisAlignment
cl = ColorSetting()
ws = WindowSetting()
sg = SteamGuard()

class PanelPage:
    def main(self, page):
        icon_path = os.path.abspath('D:/SteamManager/assets/icons/icon.ico')
        page.window.icon = icon_path
        page.title = 'Steam Helper'
        page.bgcolor = cl.defBgColor
        page.window.width = ws.defaultWidth
        page.window.height = ws.defaultHeight
        page.window.resizable = False
        page.window.full_screen = False
        page.window.center()
        page.padding = 0
        page.window.frameless = True

        self.generator = GeneratorView(page)
        self.sda = SdaView(page)
        self.bottom_bar = BottomAppBar(
            page,
            on_go_sda=lambda e: self.show_sda(),
            on_go_generator=lambda e: self.show_generator()
        )
        self.top_bar = TopAppBar(
            page,
            close_app = lambda e: close_app(e)
        )

        page.bottom_appbar = self.bottom_bar.bottom_appbar

        """MAIN CONTAINER"""
        self.main_container = ft.Column(expand=True,
                                        alignment=MainAxisAlignment.CENTER,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        controls=[
            ft.Column(controls=[self.top_bar.top_appbar]),
            ft.Column(expand=3,
                      alignment=MainAxisAlignment.CENTER,
                      horizontal_alignment=CrossAxisAlignment.CENTER,
                      controls=[self.sda.sda_page]),

        ])

        page.add(self.main_container)

        def close_app(e):
            page.window.close()

    def show_generator(self):
        """SHOW PAGE GENERATOR"""
        self.main_container.controls[1].controls = [self.generator.generator_page]

        self.main_container.update()

    def show_sda(self):
        """SHOW PAGE SDA"""
        self.main_container.controls[1].controls = [self.sda.sda_page]
        self.main_container.update()

panel_page_instance = PanelPage()
load_cfg()
settings_load()
sg.load_secret_keys()
ft.app(panel_page_instance.main)