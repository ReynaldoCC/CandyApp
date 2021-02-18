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
Comando para probar celery en la consola con el log level en debug
`celery -A locales_viv worker -B -l debug`
