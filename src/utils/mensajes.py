from tkinter import messagebox


NO_SELECCIONADO = "No ha seleccionado ningun directorio"
VACIO = "El directorio se encuentra vacio"



def show_error(mensaje):
    messagebox.showerror("Error", mensaje)

def show_info(title,mensaje):
    messagebox.showinfo(title,mensaje) 

def question(titulo,pregunta):
    return messagebox.askquestion(title=titulo, message=pregunta)

