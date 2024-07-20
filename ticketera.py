import json
import os
import configparser
from tkinter import *
from tkinter import filedialog, messagebox
from datetime import datetime

# Lista para almacenar los tickets
tickets = []
# Conjunto para almacenar los códigos de tickets
ticket_codes = set()
# Ruta del archivo JSON
json_file_path = ''
# Ruta del archivo de configuración
config_file_path = 'config.txt'
# Crea una instancia de ConfigParser
config = configparser.ConfigParser()

# Verifica si el archivo de configuración existe
if os.path.exists(config_file_path):
    # Carga la configuración existente
    config.read(config_file_path)

# Verifica si la sección 'TIPOS' existe, si no, la crea
if not config.has_section('TIPOS'):
    config.add_section('TIPOS')
    
# Verifica si la sección 'DEFAULT' y la opción 'json_file_path' existen
if config.has_section('DEFAULT') and config.has_option('DEFAULT', 'json_file_path'):
    # Carga la ruta del archivo JSON desde el archivo de configuración
    json_file_path = config.get('DEFAULT', 'json_file_path')
else:
    # Si no existe, puedes establecer una ruta predeterminada o lanzar un error
    json_file_path = 'C:/Users/alarc/Documents/GitHub/Ticketera/test.json'  # Asegúrate de reemplazar esto con una ruta válida
    # O podrías lanzar un error o advertencia si prefieres manejarlo de esa manera
    # raise FileNotFoundError("La ruta del archivo JSON no está especificada en el archivo de configuración.")


# Obtiene los tipos de tickets desde el archivo de configuración
ticket_types = [config.get('TIPOS', option) for option in config.options('TIPOS')]

# Verifica si ticket_types está vacío y, en caso afirmativo, proporciona un valor predeterminado
if not ticket_types:
    ticket_types = ["No hay tipos disponibles"]


def load_tickets():
    global tickets, ticket_codes, json_file_path, config

    # Verificar si el archivo de configuración existe
    if os.path.exists(config_file_path):
        # Cargar la configuración existente
        config.read(config_file_path)
    else:
        # Mostrar el diálogo de guardar archivo
        json_file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("Archivo JSON", "*.json")])
        # Guardar la ruta del archivo JSON en el archivo de configuración
        with open(config_file_path, 'w') as file:
            file.write(json_file_path)

    try:
        # Cargar los tickets desde el archivo JSON
        with open(json_file_path, 'r') as file:
            tickets = json.load(file)
            # Actualizar el conjunto de códigos de tickets
            ticket_codes = {ticket['ticket'] for ticket in tickets}
    except FileNotFoundError:
        # Si el archivo no existe, iniciar con listas vacías
        tickets = []
        ticket_codes = set()

def update_ticket_types():
    global ticket_types, type_option, type_var
    # Obtiene los tipos de tickets desde el archivo de configuración
    ticket_types = [config.get('TIPOS', option)
                    for option in config.options('TIPOS')]
    # Actualiza type_option para mostrar los nuevos tipos
    type_option['menu'].delete(0, 'end')
    for ticket_type in ticket_types:
        type_option['menu'].add_command(
            label=ticket_type, command=lambda value=ticket_type: type_var.set(value))


# Función para guardar el nuevo tipo de ticket
def save_new_type(new_type_var, config_window):
    new_type = new_type_var.get()
    if new_type:
        # Verifica si el tipo ya existe
        for option in config.options('TIPOS'):
            if config.get('TIPOS', option) == new_type:
                messagebox.showerror("Error", "El tipo de ticket ya existe.")
                return
        # Añade el nuevo tipo a la sección 'TIPOS'
        config.set(
            'TIPOS', f'tipo{len(config.options("TIPOS")) + 1}', new_type)
        # Escribe los cambios en el archivo de configuración
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        # Actualiza la lista de tipos
        update_ticket_types()
        # Cierra la ventana de configuración para volver al inicio
        config_window.destroy()
        messagebox.showinfo(
            "Información", "Tipo de ticket guardado con éxito.")

# Función para eliminar un tipo de ticket existente


def delete_existing_type(existing_type_var, config_window):
    existing_type = existing_type_var.get()
    if existing_type:
        # Encuentra y elimina el tipo existente
        for option in config.options('TIPOS'):
            if config.get('TIPOS', option) == existing_type:
                config.remove_option('TIPOS', option)
                break
        # Escribe los cambios en el archivo de configuración
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        # Actualiza la lista de tipos
        update_ticket_types()
        # Cierra la ventana de configuración para volver al inicio
        config_window.destroy()
        messagebox.showinfo(
            "Información", "Tipo de ticket eliminado con éxito.")

# Función para enviar un ticket
def submit_ticket():
    # Obtener los valores de los campos de entrada
    ticket = ticket_entry.get()
    type = type_var.get()
    pending = pending_response_var.get()
    support = support_var.get()
    # Verificar si el código del ticket ya existe
    if not ticket or not type:
        error_label.config(
            text='Error: El ticket y el tipo no pueden estar vacíos.')
        return
    if ticket in ticket_codes:
        error_label.config(text='Error: El código del ticket ya existe.')
        return

    # Crear un nuevo ticket
    new_ticket = {
        'ticket': ticket,
        'type': type,
        'support' : support,
        'pending': pending,
        # get current date in YYYY-MM-DD format
        'date': datetime.now().strftime('%Y-%m-%d')
    }

    # Agregar el nuevo ticket a la lista de tickets y el código del ticket al conjunto de códigos
    tickets.append(new_ticket)
    ticket_codes.add(ticket)

    # Contar el total de tickets para el día actual
    total_tickets = len(
        [t for t in tickets if t['date'] == new_ticket['date']])

    # Mostrar el total de tickets
    total_label.config(text='Total de tickets hoy: ' + str(total_tickets))

    # Limpiar el mensaje de error
    error_label.config(text='')

    # Convertir la lista de tickets a JSON y guardarla en un archivo
    with open(json_file_path, 'w') as file:
        json.dump(tickets, file)
        
def export_tickets():
    # Mostrar el diálogo de guardar archivo
    
    # Mostrar un mensaje de éxito
    messagebox.showinfo("Información", "Tickets exportados con éxito.")


# Crear la interfaz de usuario
root = Tk(
    className=' Ticketera',
    baseName=' Ticketera',
    useTk=1,
)
# Hacer que type_var y type_option sean variables globales
global type_var, type_option,support_var, pending_response_var
type_var = StringVar(root)
type_option = OptionMenu(root, type_var, *ticket_types)

root.geometry('400x550')
root.configure(bg='white')  # Set the background color to white

# Use a simple and legible font
font = ('Helvetica', 12)

load_tickets()

Label(root, text='Ticket:', bg='white', font=font).pack(pady=10)
ticket_entry = Entry(root, font=font)
ticket_entry.pack(pady=10)

Label(root, text='Tipo:', bg='white', font=font).pack(pady=10)
type_var = StringVar(root)
type_option = OptionMenu(root, type_var, *ticket_types)
type_option.config(bg='white', font=font)
type_option.pack(pady=10)

Button(root, text='Submit', command=submit_ticket,
       bg='white', font=font).pack(pady=10)

# Definir la variable de control para el Checkbutton
pending_response_var = IntVar(root)

# Crear el Checkbutton para marcar el ticket como pendiente de respuesta
pending_response_checkbutton = Checkbutton(root, text='Pendiente de respuesta', variable=pending_response_var, onvalue=1, offvalue=0, bg='white', font=font)
pending_response_checkbutton.pack(pady=10)

# Definir la variable de control para otro Checkbutton (si aplica)
support_var = IntVar(root)

# Crear otro Checkbutton para indicar "dónde se apoyó"
support_checkbutton = Checkbutton(root, text='Donde se apoyó', variable=support_var, onvalue=1, offvalue=0, bg='white', font=font)
support_checkbutton.pack(pady=10)

Button(root, text='Export', command=export_tickets,
       bg='white', font=font).pack(pady=10)

total_label = Label(root, text='', bg='white', font=font)
total_label.pack(pady=10)

error_label = Label(root, text='', fg='red', bg='white', font=font)
error_label.pack(pady=10)

# Función para abrir la ventana de configuración


def open_config_window():
    config_window = Toplevel(root)
    config_window.title("Configuración")
    config_window.geometry('200x200')
    new_type_var = StringVar()
    existing_type_var = StringVar()

    Label(config_window, text="Nuevo tipo de ticket:").pack(pady=10)
    Entry(config_window, textvariable=new_type_var).pack()
    Button(config_window, text="Guardar",
           command=lambda: save_new_type(new_type_var, config_window)).pack()

    Label(config_window, text="Eliminar tipo existente:").pack(pady=10)
    existing_type_option = OptionMenu(
        config_window, existing_type_var, *ticket_types)
    existing_type_option.pack()
    Button(config_window, text="Eliminar",
           command=lambda: delete_existing_type(existing_type_var, config_window)).pack()


# Crea el botón de configuración
config_button = Button(root, text="Configuración",
                       command=open_config_window, bg='white', font=font)

config_button.pack()
root.mainloop()
