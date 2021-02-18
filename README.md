# <center><img src="./static/dpv_base/images/logo.svg" width="90"> </center>
# <center>CandyApp</center>

Aplicación de la DPV la Habana para informatización de las distintas áreas de gestión.


## Índice


## Instalación

#### Instalación de requerimientos del sistema

* ###### En Ubuntu

```bash
$ sudo apt install build-essential python3 python3-dev python3-pip python3-wheel python3-setuptools python3-virtualenv python3-virtualenvwrapper libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info git redis 
```

* ###### En Windows
Instalar Python3 [Python3 64bit](https://www.python.org/ftp/python/3.8.7/python-3.8.7-amd64.exe) o [Python3 32bit](https://www.python.org/ftp/python/3.8.7/python-3.8.7.exe)
según la arquitectura del sistema, y configure la ruta a [python dentro de la variable PATH](https://datatofish.com/add-python-to-windows-path/)


#### Crear y activar el virtualenv
```bash
$ virtualenv expemxenv -p python3
$ source expemxenv/bin/activate
```

#### Instalación de los requerimientos con PiP
```bash
$ pip3 install -r <path/to/project/folder>/requeriments.txt
```

#### Configurar todos los datos mediante variables de entorno

Ver en el archivo 'envs/local/example_env' ahi se exponen las distintas variable que puede necesitar el sistema para funcionar, la idea es crear un archivo de entorno con los valores para las variables necesarias, una alertnativa puede ser copiar el archivo antes mensionado y a partir de el crear un archivo con las configuracion

* ###### En Ubuntu

```bash
$ sudo /<path>/<to>/<proyect>/envs/local/example_env /etc/environment.d/candy_app.conf
```

* ###### En windows

configurar manualmemte las varibles de entorno como se explica [aquí](https://answers.microsoft.com/es-es/windows/forum/windows_10-other_settings/windows-10-variables-de-entorno-windows-10-version/703ea5fa-1db4-46da-8ff7-6261140bf58b)

#### Ejecutar la aplicacición 

* ###### En el servidor de desarrollo de Django
Los pasos para ejecutar la aplicación con el servidor de desarrollo de django serian los siguientes:
    
1. Activar el entorno virtual

    ```bash
    $ source /<path>/<to>/<environment>/bin/acttivate
    ```

2. cambiar al directorio del proyecto

    ```bash
    $ cd /<path>/<to>/<proyect>/
    ```

3. Ejecutar las migraciones

    ```bash
    $ python3 manage.py migrate
    ```

4. Crear el usuario administrador

    ```bash
    $ python3 manage.py createsuperuser
    ```

5. Ejecutar el servidor de desarrollo de django

    ```bash
    $ python3 manage.py runserver 0.0.0.0:8000
    ```

6. Abrir una nueva terminal y ejecutar celery para las tareas asincronas y periodicas. El nivel de la bitácora de celery se pone a 'debug' pero puede cambiarse segun se desee.

    ```bash
    $ celery -A locales_viv worker -B -l debug
    ```



* ###### En Apache

Los pasos para la ejecución de la aplicación en Apache2 serían los siguientes:

1. Instalar Apache, el modulo wsgi de apache y supervisor para que ejecute celery en background

    ```bash
   $ sudo apt install apache2 libapache2-mod-wsgi-py3 supervisor
    ```

2. Probar que el sistema funciona para ello podemos serguir los pasos [explicados aquí](#en-el-servidor-de-desarrollo-de-django).
3. configurar apache para levantar candy como aplicación por defecto.

    ```bash
   $ sudo cp /<path>/<to>/<proyect>/apache_example.conf /etc/apache2/conf-available/candyapp.conf
   $ sudo vi /etc/apache2/conf-available/candyapp.conf
    ```
4. Editamos el contenido con los valores que vamos a utilizar digase servername, serveradmin, documentroot y las rutas al proyecto y al entorno virtual. Yo uso *vi* por preferencia puede usar cualquier otro editor como por ejemplo *nano*. Una vez editado el archivo con la configuración válida activamos el sitio de candy app y desactivamos el default de apache

    ```bash
    $ sudo a2dissite 000-default.conf
    $ sudo a2ensite candyapp.conf
    ```

