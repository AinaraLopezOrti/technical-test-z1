# technical test z1

A continuación, se detallan los pasos necesarios para poner en marcha el proyecto Django en un entorno virtual, además de cómo instalar las herramientas necesarias en diferentes sistemas operativos: Windows, Ubuntu y macOS.

## Resumen del Proyecto - API GraphQL con Django y PostgreSQL

El objetivo de este proyecto es desarrollar un API GraphQL utilizando Django y PostgreSQL para brindar servicios a una aplicación móvil. El API se centrará en resolver diversas historias de usuario que abarcan diferentes funcionalidades de la aplicación. A continuación, se presenta un resumen de las principales características y funcionalidades del proyecto:

### 1. Registro y Autenticación de Usuarios

Los usuarios podrán registrarse proporcionando su dirección de correo electrónico, un nombre de usuario y una contraseña.
Los usuarios podrán iniciar sesión utilizando su dirección de correo electrónico y contraseña.

### 2. Cambio y Restauración de Contraseña

Los usuarios podrán cambiar su contraseña después del inicio de sesión.
Los usuarios podrán restaurar su contraseña mediante el envío de un enlace mágico por correo electrónico.

### 3. Publicación de Ideas

Los usuarios podrán publicar ideas como texto corto en cualquier momento.
Las ideas tendrán opciones de visibilidad: pública (visible para todos), protegida (solo visible para seguidores) y privada (solo visible para el creador).

### 4. Gestión de Ideas

Los usuarios podrán editar la visibilidad de sus ideas después de la publicación.
Los usuarios podrán eliminar sus ideas publicadas.

### 5. Seguimiento de Usuarios

Los usuarios podrán solicitar seguir a otros usuarios.
Los usuarios recibirán solicitudes de seguimiento y podrán aprobar o denegarlas.
Los usuarios podrán ver la lista de personas que siguen y que les siguen.

### 6. Búsqueda de Usuarios

Los usuarios podrán buscar otros usuarios ingresando un nombre de usuario o parte de él.

### 7. Visualización de Ideas

Los usuarios podrán ver la lista de ideas de cualquier otro usuario, teniendo en cuenta su visibilidad.
Los usuarios tendrán un timeline que muestra sus propias ideas y las de los usuarios que siguen, respetando la visibilidad de cada idea.

### 8. Notificaciones

Los usuarios recibirán notificaciones cada vez que un usuario al que siguen publique una nueva idea a la que tengan acceso.

## Requisitos previos

Asegúrate de tener instalado Python 3.9 en tu sistema antes de comenzar. Puedes descargarlo desde el sitio web oficial de Python (https://www.python.org/downloads/) y seguir las instrucciones de instalación específicas para tu sistema operativo.

## Pasos para poner en marcha el proyecto Django

### 1. Crear un entorno virtual

Un entorno virtual te permitirá aislar las dependencias de tu proyecto y evitar conflictos con otras aplicaciones. Sigue estos pasos para crear y activar un entorno virtual:

#### Windows:

```
bash
pip install virtualenv
virtualenv venv
venv\Scripts\activate
```

#### Ubuntu / macOS:

```
pip install virtualenv
virtualenv -p python3.9 venv
source venv/bin/activate
```

### 2. Instalar las dependencias
Dentro del entorno virtual, instala las dependencias necesarias para el proyecto usando pipenv:

```
pip install pipenv
pipenv install
```

### 3. Configuración PostgreSQL

Es necesario crear un archivo llamado localConfig.py en la ruta config/settings/ donde se añadirán los datos de la base de datos PostgreSQL que se va a utilizar. A continuación, se muestra un ejemplo de cómo debe ser el contenido de este archivo:

1. Primero, crea el archivo localConfig.py en la ruta config/settings/.

2. A continuación, agrega el siguiente contenido al archivo localConfig.py:
```
# config/settings/localConfig.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_de_la_base_de_datos',
        'USER': 'nombre_de_usuario',
        'PASSWORD': 'contraseña_del_usuario',
        'HOST': 'localhost',  # Cambia esto si la base de datos está en otro host
        'PORT': '',          # Puedes especificar un puerto si es necesario
    }
}
```

Reemplaza 'nombre_de_la_base_de_datos', 'nombre_de_usuario' y 'contraseña_del_usuario' con los datos reales de tu base de datos PostgreSQL.

Si la base de datos PostgreSQL se encuentra en un host diferente a localhost, modifica la variable 'HOST' con la dirección IP o el nombre del host correspondiente.

Si la base de datos utiliza un puerto diferente al predeterminado, puedes especificarlo en la variable 'PORT'.

Una vez que hayas creado y configurado el archivo localConfig.py, estará listo para realizar las migraciones y configurar la base de datos de PostgreSQL para tu proyecto Django. Esto permitirá que Django utilice la configuración específica de tu base de datos al realizar las operaciones de migración y administrar los modelos de tu aplicación.

### 4. Realizar las migraciones

El siguiente paso es aplicar las migraciones al modelo de base de datos:
```
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear un superusuario (opcional)

Si deseas acceder al panel de administrador de Django, puedes crear un superusuario con el siguiente comando:

```
python manage.py createsuperuser
```
Sigue las instrucciones que aparecerán en la terminal para configurar el nombre de usuario, dirección de correo electrónico y contraseña del superusuario.

### 6.  Ejecutar el proyecto

Finalmente, para poner en marcha el proyecto, ejecuta el siguiente comando:
```
python manage.py runserver
```

El servidor de desarrollo se ejecutará por defecto en http://127.0.0.1:8000/. Si deseas utilizar otro puerto, puedes especificarlo agregando el número de puerto después del comando runserver, por ejemplo:

```
python manage.py runserver 8080
```

Si no deseas que el servidor se recargue automáticamente cada vez que se realicen cambios en el código, puedes agregar la opción --noreload:

```
python manage.py runserver --noreload
```

¡El proyecto Django debería estar ahora en funcionamiento!

## Ejecución de pruebas

Se ha creado un test para cada historia de usuario del proyecto. Para ejecutar todas las pruebas, utiliza el siguiente comando:

```
python manage.py test
```

## Ejecución de Pruebas con GraphQL y Autenticación JWT

A continuación, se explica cómo realizar pruebas utilizando GraphQL y la autenticación JWT para el API desarrollado en Django. Antes de comenzar, asegúrate de haber seguido los pasos anteriores para poner en marcha el proyecto y haber creado un usuario registrado mediante la mutación que se muestra a continuación:

### Registro de un Usuario

Para registrar un usuario, puedes utilizar la siguiente mutación en la herramienta de pruebas de GraphQL o mediante alguna herramienta de cliente HTTP (por ejemplo, Postman):

```
mutation {
    registerUser(email: "test@example.com", username: "testuser", password: "testpassword") {
        user {
            id
            email
            username
        }
    }
}
```

Este código enviará una petición de mutación para registrar un usuario con la dirección de correo electrónico "test@example.com", el nombre de usuario "testuser" y la contraseña "testpassword". Si el registro es exitoso, recibirás los detalles del usuario registrado como respuesta, incluido su ID, dirección de correo electrónico y nombre de usuario.


### Autenticación JWT
Una vez que tengas un usuario registrado, podrás utilizar la autenticación JWT para realizar otras pruebas que requieran acceso a rutas protegidas. Para obtener un token JWT válido, sigue los siguientes pasos:

1. Realiza una petición de mutación de inicio de sesión con las credenciales del usuario registrado. La mutación de inicio de sesión debería ser similar a esta:

```
mutation {
    tokenAuth(username: "testuser", password: "testpassword") {
        token
    }
}
```

2. Si las credenciales son correctas, recibirás un token JWT como respuesta. Este token deberá ser incluido en los encabezados de las siguientes solicitudes para acceder a rutas protegidas.

Para incluir el token JWT en las solicitudes, agrega un encabezado "Authorization" con el valor "JWT {token}" en cada petición. Por ejemplo:

```
"Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

Menos para el registro de usuarios y el reseteo de la contraseña es necesario estar autenticado para hacer las pruebas.