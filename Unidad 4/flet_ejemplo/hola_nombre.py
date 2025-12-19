import flet as ft

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Hola "

        self.input_nombre = ft.TextField(
            label = "Nombre",
            hint_Text= "Ingresa tu Nombre"
        )
        self.button_saludar = ft.Button(
            Text="Saludar"
        )
        self.Text_saludar = ft.Text(
            value = ""
        )

        self.build()

    def build(self):
        self.page.add(
            self.input_nombre,
            self.button_saludar,
            self.Text_saludar
        )
        
    def on_saludar(self):
        nombre = (self.input_nombre.value or "").strip()
        if not nombre:
            self.Text_saludar.value = "Ingresa tu Nombre"
        else:
            self.Text_saludar.value = f"Hola {nombre}"
            self.page.update()
        

if __name__ == "__main__":
    ft.app(target=App)