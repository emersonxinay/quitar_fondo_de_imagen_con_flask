import threading
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from rembg import remove
import shutil
import time
from datetime import date

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


def calcular_proxima_navidad():
    # Cálculo de la próxima Navidad (25 de diciembre de este año)
    current_year = date.today().year
    next_christmas = date(current_year, 12, 25)
    return next_christmas


def actualizar_proxima_navidad():
    while True:
        next_christmas = calcular_proxima_navidad()
        app.config['next_christmas'] = next_christmas
        # Espera 24 horas (86400 segundos) antes de volver a calcular
        time.sleep(86400)


# Inicializar la fecha de la próxima Navidad en un hilo separado
thread = threading.Thread(target=actualizar_proxima_navidad)
thread.start()


# Ruta principal para cargar una imagen


@app.route('/', methods=['GET', 'POST'])
def index():
    title = "Quitando fondo de Imagenes"

    # Variable para almacenar la imagen procesada
    processed_image = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        image = request.files['image']
        if image.filename == '':
            return redirect(request.url)
        if image:
            filename = os.path.join(
                app.config['UPLOAD_FOLDER'], image.filename)
            image.save(filename)
            processed_filename = process_image(filename)
            if processed_filename:
                processed_image = os.path.basename(processed_filename)
            else:
                return "Error al procesar la imagen."
    return render_template('index.html', title=title, processed_image=processed_image, next_christmas=app.config['next_christmas'])

# Ruta para servir archivos desde la carpeta 'uploads'


@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta para mostrar todas las imágenes procesadas


@app.route('/processed_images')
def processed_images():

    title = "imagenes procesadas"
    processed_images = os.listdir(app.config['UPLOAD_FOLDER'])
    processed_images = [
        image for image in processed_images if image.startswith('processed_')]
    return render_template('processed_images.html', title=title, processed_images=processed_images,  next_christmas=app.config['next_christmas'])

# Función para procesar la imagen y eliminar el fondo


def process_image(filename):
    try:
        # Crear una copia del archivo original con el prefijo "original_"
        original_filename = os.path.join(
            app.config['UPLOAD_FOLDER'], 'original_' + os.path.basename(filename))
        shutil.copy(filename, original_filename)

        # Elimina el fondo de la imagen utilizando rembg
        with open(filename, "rb") as input_file:
            output = remove(input_file.read())

        # Guarda la imagen procesada
        processed_filename = os.path.join(
            app.config['UPLOAD_FOLDER'], 'processed_' + os.path.basename(filename))
        with open(processed_filename, "wb") as output_file:
            output_file.write(output)

        return processed_filename
    except Exception as e:
        print(f"Error al procesar la imagen: {str(e)}")
        return None


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
