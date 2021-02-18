# <center><img src="./static/dpv_base/images/logo.svg" width="90"> </center>
# <center>CandyApp</center>

Aplicación de la DPV la Habana para informatización de las distintas áreas de gestión.


## Índice


## Instalación

#### Instalación de requerimientos del sistema

* ###### En Ubuntu

```bash
$ sudo apt install build-essential python3 python3-dev python3-pip python3-wheel python3-setuptools python3-virtualenv python3-virtualenvwrapper libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info git
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


Comando para probar celery en la consola con el log level en debug
`celery -A locales_viv worker -B -l debug`
