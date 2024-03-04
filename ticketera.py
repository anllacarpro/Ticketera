import json
import os
from tkinter import *
from tkinter import filedialog
from datetime import datetime

# Lista para almacenar los tickets
tickets = []
# Conjunto para almacenar los códigos de tickets
ticket_codes = set()
# Ruta del archivo JSON
json_file_path = ''
# Ruta del archivo de configuración
config_file_path = 'config.txt'


def load_tickets():
    global tickets, ticket_codes, json_file_path

    # Verificar si el archivo de configuración existe
    if os.path.exists(config_file_path):
        # Cargar la ruta del archivo JSON desde el archivo de configuración
        with open(config_file_path, 'r') as file:
            json_file_path = file.read().strip()
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


def submit_ticket():
    # Obtener los valores de los campos de entrada
    ticket = ticket_entry.get()
    type = type_var.get()

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


# Crear la interfaz de usuario
root = Tk(
    className=' Ticketera',
    baseName=' Ticketera',
    useTk=1,
)
root.geometry('400x350')
root.configure(bg='white')  # Set the background color to white

# Use a simple and legible font
font = ('Helvetica', 12)

load_tickets()

Label(root, text='Ticket:', bg='white', font=font).pack(pady=10)
ticket_entry = Entry(root, font=font)
ticket_entry.pack(pady=10)

Label(root, text='Tipo:', bg='white', font=font).pack(pady=10)
type_var = StringVar(root)
type_var.set('Tipo 1')  # valor por defecto
type_option = OptionMenu(
    root, type_var, 'Incidencia Custom Care', 'Incidencia Comercial TLK', 'Tipo 3')
type_option.config(bg='white', font=font)
type_option.pack(pady=10)

Button(root, text='Submit', command=submit_ticket,
       bg='white', font=font).pack(pady=10)

total_label = Label(root, text='', bg='white', font=font)
total_label.pack(pady=10)

error_label = Label(root, text='', fg='red', bg='white', font=font)
error_label.pack(pady=10)

root.mainloop()
