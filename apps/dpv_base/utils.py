from django.conf import settings

from django import urls as dj_urls

from .models import ConfigMail

from main import urls

import os


def store_url_names():
    settings.BULK_URLS = []
    for url_base in urls.urlpatterns:
        if isinstance(url_base, dj_urls.URLResolver):
            for urlpattern in url_base.url_patterns:
                if isinstance(urlpattern, dj_urls.URLPattern) and urlpattern.name:
                    settings.BULK_URLS.append(urlpattern.name)
        elif isinstance(url_base, dj_urls.URLPattern):
            settings.BULK_URLS.append(url_base.name)


def get_settings_email_conf():
    conf = ConfigMail()
    conf.password = settings.EMAIL_HOST_PASSWORD or ''
    conf.usuario = settings.EMAIL_HOST_USER or ''
    conf.servidor = settings.EMAIL_HOST or ''
    conf.puerto = settings.EMAIL_PORT or ''
    conf.usa_tls = settings.EMAIL_USE_TLS or False
    conf.usa_ssl = settings.EMAIL_USE_SSL or False
    return conf


def get_db_email_conf():
    conf = ConfigMail.objects.all().first()
    return conf


def comapare_db_settings_conf(confdb, confset):
    if not confdb or not confset or confdb.puerto is None or confset.puerto is None:
        return False
    return confdb.usuario == confset.usuario and confdb.servidor == confset.servidor and \
        int(confdb.puerto) == int(confset.puerto) and confdb.password == confset.password and \
        confdb.use_tls == confset.usa_tls and confdb.use_ssl == confset.usa_ssl


def set_settings_email_conf(configuration):
    if not configuration:
        return
    if configuration.use_ssl and configuration.use_tls:
        configuration.use_ssl = False
        configuration.use_tls = False
    lines = []
    settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")

    settings_realitve_path = settings_module.split('.')
    settings_realitve_path = os.sep.join(settings_realitve_path)
    settings_realitve_path += ".py"
    try:
        settingdfile = open(os.path.join(settings.BASE_DIR, settings_realitve_path), "r", encoding="utf-8")
        lines = settingdfile.readlines()
        settingdfile.close()
    except:
        print("no se pudo abrir el archivo para leerlo")
    try:
        settingdfile = open(os.path.join(settings.BASE_DIR, settings_realitve_path), "w", encoding="utf-8")
    except:
        print("no se pudo escribir en el archivo")
    else:
        for line in lines:
            if 'EMAIL_HOST ' in line:
                new_line = 'EMAIL_HOST = "' + str(configuration.servidor) + '"\n'
                settingdfile.write(new_line)
            elif 'EMAIL_HOST_PASSWORD ' in line:
                new_line = 'EMAIL_HOST_PASSWORD = "' + str(configuration.password) + '"\n'
                settingdfile.write(new_line)
            elif 'EMAIL_HOST_USER ' in line:
                new_line = 'EMAIL_HOST_USER = "' + str(configuration.usuario) + '"\n'
                settingdfile.write(new_line)
            elif 'EMAIL_PORT ' in line:
                new_line = 'EMAIL_PORT = "' + str(configuration.puerto) + '"\n'
                settingdfile.write(new_line)
            elif 'EMAIL_USE_TLS ' in line:
                new_line = 'EMAIL_USE_TLS = ' + str(configuration.use_tls) + '\n'
                settingdfile.write(new_line)
            elif 'EMAIL_USE_SSL ' in line:
                new_line = 'EMAIL_USE_SSL = ' + str(configuration.use_ssl) + '\n'
                settingdfile.write(new_line)
            else:
                settingdfile.write(line)
        settingdfile.close()
    return True


def main_email_candy_conf(db_config=None):
    settings_conf = get_settings_email_conf()
    if not db_config:
        db_config = get_db_email_conf()
    same_config = comapare_db_settings_conf(db_config, settings_conf)
    if not same_config:
        set_ok = set_settings_email_conf(db_config)
        return set_ok
    return True
