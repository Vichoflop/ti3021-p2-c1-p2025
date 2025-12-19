import flet as ft

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Hola Mundo"
        self.build()

    def build(self):
        self.page.add(
            ft.Text("Hola Mundo")
        )

def main(page: ft.Page):
    App(page)

if __name__ == "__main__":
    ft.app(target=main)
