import flet as ft

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Hola "
        self.build()

    def build(self):
        self.page.add(
            ft.TextField(
                label = "Nombre",
                hint_text = "Ingresa tu Nombre"
            )
        )
        self.page.add(
            ft.Button(
                text="Saludar"
            )
        )


if __name__ == "__main__":
    ft.app(target=App)