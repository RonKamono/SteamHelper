import flet as ft

class BtnStyle:
    def __init__(self):

        self.ButtonStyle(
            color={
                ft.ControlState.HOVERED: ft.Colors.WHITE,
                ft.ControlState.FOCUSED: ft.Colors.BLUE,
                ft.ControlState.DEFAULT: ft.Colors.BLACK,
            }
        )