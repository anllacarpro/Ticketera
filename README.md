# Ticketera

Ticketera es una aplicación de escritorio para la gestión de tickets, desarrollada con Python y Tkinter.

## Características

- Gestión de tickets: Permite a los usuarios introducir un código de ticket y seleccionar un tipo de ticket de una lista desplegable.
- Validación de entradas: Verifica que el código del ticket y el tipo no estén vacíos y que el código del ticket no exista ya en la lista de tickets.
- Gestión de tipos de tickets: Los tipos de tickets se pueden añadir o eliminar a través de una ventana de configuración.
- Conteo de tickets: Cuenta el número total de tickets creados en el día actual.
- Persistencia de datos: Los tickets y los tipos de tickets se almacenan en archivos y se cargan al iniciar la aplicación.

## Instalación

Para instalar y ejecutar esta aplicación, sigue estos pasos:

1. Clona este repositorio.
2. Navega a la carpeta del repositorio en tu terminal.
3. Instala las dependencias con pip: `pip install -r requirements.txt`
4. Ejecuta el script principal: `python ticketera.py`

## Uso

Para usar la aplicación, introduce un código de ticket y selecciona un tipo de ticket, luego haz clic en "Enviar". Para añadir o eliminar tipos de tickets, haz clic en "Configuración".

## Contribuir

Las contribuciones son bienvenidas. Para contribuir, por favor abre un issue o realiza un pull request.

## Licencia

Ticketera está licenciada bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.