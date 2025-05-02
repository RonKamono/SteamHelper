import flet as ft
from pages import *
from settings import *

cl = ColorSetting()
ws = WindowSetting()


class PanelPage:
    async def main(self, page: ft.Page):
        from utils.config_utils import load_cfg
        load_cfg()
        icon_path = r'C:\Users\Ron\PycharmProjects\SteamManager\assets\icons\icon.ico'
        page.window.icon = icon_path
        page.title = "SteamManager"
        page.bgcolor = cl.defBgColor
        page.window.width = ws.defaultWidth
        page.window.height = ws.defaultHeight
        page.window.resizable = False
        page.window.full_screen = False
        page.window.maximizable = False
        # page.window.center()

        generator = GeneratorView(page)
        abar = ButtomAppBar(page)

        # VIEW APPBAR
        page.bottom_appbar = abar.appbar

        # VIEW GENERATOR
        page.add(
            ft.Column(expand=True,
                      controls=[
                          ft.Column(expand=1),
                          ft.Column(
                              expand=3,
                              controls=[
                                  generator.generator_page
                              ]),
                      ])
        )

panel_page_instance = PanelPage()
ft.app(panel_page_instance.main)
