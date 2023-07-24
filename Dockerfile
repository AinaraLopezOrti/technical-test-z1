# Usa la imagen base de Python
FROM python:3.9

# Variables de entorno para evitar la generación de archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo en /app
WORKDIR /testz1

# Instala pipenv
RUN pip install pipenv

# Copia los archivos de dependencias
COPY Pipfile Pipfile.lock /testz1//

# Instala las dependencias usando pipenv
RUN pipenv install --system

# Copia el resto de los archivos del proyecto al contenedor
COPY . /testz1/

# Expone el puerto 8000 para que pueda ser accedido desde fuera del contenedor
EXPOSE 8000

# Comando para ejecutar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

