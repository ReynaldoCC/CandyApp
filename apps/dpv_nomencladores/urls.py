from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='nomenclador_index'),

    path('provincia/', index_provincia, name='nomenclador_provincia'),
    path('nueva_provincia/', add_provincia, name='provincia_new'),
    path('editar_provincia/<int:id_provincia>', update_provincia, name='provincia_edit'),
    path('eliminar_provincia/<int:id_provincia>', delete_provincia, name='provincia_delete'),

    path('municipio/', index_municipio, name='nomenclador_municipio'),
    path('nuevo_municipio/', add_municipio, name='municipio_new'),
    path('editar_municipio/<int:id_municipio>', update_municipio, name='municipio_edit'),
    path('eliminar_municipio/<int:id_municipio>', delete_municipio, name='municipio_delete'),

    path('consejopopular/', index_consejopopular, name='nomenclador_consejopopular'),
    path('nuevo_consejopopular/', add_consejopopular, name='consejopopular_new'),
    path('editar_consejopopular/<int:id_consejopopular>', update_consejopopular, name='consejopopular_edit'),
    path('eliminar_consejopopular/<int:id_consejopopular>', delete_consejopopular, name='consejopopular_delete'),

    path('calle/', index_calle, name='nomenclador_calle'),
    path('nueva_calle/', add_calle, name='calle_new'),
    path('new_calle/', add_calle_on_user, name='calle_new_async'),
    path('agree_calle/', agree_calle, name='agree_calle'),
    path('editar_calle/<int:id_calle>', update_calle, name='calle_edit'),
    path('eliminar_calle/<int:id_calle>', delete_calle, name='calle_delete'),

    path('piso/', index_piso, name='nomenclador_piso'),
    path('nuevo_piso/', add_piso, name='piso_new'),
    path('editar_piso/<int:id_piso>', update_piso, name='piso_edit'),
    path('eliminar_piso/<int:id_piso>', delete_piso, name='piso_delete'),

    path('organismo/', index_organismo, name='nomenclador_organismo'),
    path('nuevo_organismo/', add_organismo, name='organismo_new'),
    path('organismo/autofill', autofill_organismo, name='organismo_autofill'),
    path('organismo/found', found_organismo_by_name, name='organismo_found'),
    path('editar_organismo/<int:id_organismo>', update_organismo, name='organismo_edit'),
    path('eliminar_organismo/<int:id_organismo>', delete_organismo, name='organismo_delete'),

    path('destino/', index_destino, name='nomenclador_destino'),
    path('nuevo_destino/', add_destino, name='destino_new'),
    path('editar_destino/<int:id_destino>', update_destino, name='destino_edit'),
    path('eliminar_destino/<int:id_destino>', delete_destino, name='destino_delete'),

    path('concepto/', index_concepto, name='nomenclador_concepto'),
    path('nuevo_concepto/', add_concepto, name='concepto_new'),
    path('editar_concepto/<int:id_concepto>', update_concepto, name='concepto_edit'),
    path('eliminar_concepto/<int:id_concepto>', delete_concepto, name='concepto_delete'),

    path('genero/', index_genero, name='nomenclador_genero'),
    path('nuevo_genero/', add_genero, name='genero_new'),
    path('editar_genero/<int:id_genero>/', update_genero, name='genero_edit'),
    path('eliminar_genero/<int:id_genero>', delete_genero, name='genero_delete'),

    path('departamento/', index_areatrabajo, name='nomenclador_areatrab'),
    path('nuevo_departamento/', add_areatrabajo, name='areatrabajo_new'),
    path('editar_departamento/<int:id_areatrabajo>', update_areatrabajo, name='areatrabajo_edit'),
    path('eliminar_departamento/<int:id_areatrabajo>', delete_areatrabajo, name='areatrabajo_delete'),

    path('unidad/', index_centrotrabajo, name='nomenclador_centrab'),
    path('nuevo_centrotrabajo/', add_centrotrabajo, name='centrotrabajo_new'),
    path('editar_unidad/<int:id_centrotrabajo>', update_centrotrabajo, name='centrotrabajo_edit'),
    path('eliminar_unidad/<int:id_centrotrabajo>', delete_centrotrabajo, name='centrotrabajo_delete'),

    path('codificadorasunto/', index_codificadorasunto, name='nomenclador_codificadorasunto'),
    path('nuevo_codificadorasunto/', add_codificadorasunto, name='codificadorasunto_new'),
    path('editar_codificadorasunto/<int:id_codificadorasunto>', update_codificadorasunto, name='codificadorasunto_edit'),
    path('eliminar_codificadorasunto/<int:id_codificadorasunto>', delete_codificadorasunto, name='codificadorasunto_delete'),

    path('tipoqueja/', index_tipoqueja, name='nomenclador_tipoqueja'),
    path('nuevo_tipoqueja/', add_tipoqueja, name='tipoqueja_new'),
    path('editar_tipoqueja/<int:id_tipoqueja>', update_tipoqueja, name='tipoqueja_edit'),
    path('eliminar_tipoqueja/<int:id_tipoqueja>', delete_tipoqueja, name='tipoqueja_delete'),

    path('procedencia/', index_procedencia, name='nomenclador_procedencia'),
    path('nuevo_procedencia/', add_procedencia, name='procedencia_new'),
    path('editar_procedencia/<int:id_procedencia>', update_procedencia, name='procedencia_edit'),
    path('eliminar_procedencia/<int:id_procedencia>', delete_procedencia, name='procedencia_delete'),

    path('tipoprocedencia/', index_tipoprocedencia, name='nomenclador_tipoprocedencia'),
    path('nuevo_tipoprocedencia/', add_tipoprocedencia, name='tipoprocedencia_new'),
    path('editar_tipoprocedencia/<int:id_tipoprocedencia>', update_tipoprocedencia, name='tipoprocedencia_edit'),
    path('eliminar_tipoprocedencia/<int:id_tipoprocedencia>', delete_tipoprocedencia, name='tipoprocedencia_delete'),

    path('estado/', index_estado, name='nomenclador_estado'),
    path('nuevo_estado/', add_estado, name='estado_new'),
    path('editar_estado/<int:id_estado>', update_estado, name='estado_edit'),
    path('eliminar_estado/<int:id_estado>', delete_estado, name='estado_delete'),

    path('clasificacionrespuesta/', index_clasificacionrespuesta, name='nomenclador_clasificacionrespuesta'),
    path('nuevo_clasificacionrespuesta/', add_clasificacionrespuesta, name='clasificacionrespuesta_new'),
    path('editar_clasificacionrespuesta/<int:id_clasificacionrespuesta>', update_clasificacionrespuesta, name='clasificacionrespuesta_edit'),
    path('eliminar_clasificacionrespuesta/<int:id_clasificacionrespuesta>', delete_clasificacionrespuesta, name='clasificacionrespuesta_delete'),

    path('prensaescrita/', index_prensaescrita, name='nomenclador_prensaescrita'),
    path('nuevo_prensaescrita/', add_prensaescrita, name='prensaescrita_new'),
    path('editar_prensaescrita/<int:id_prensaescrita>', update_prensaescrita, name='prensaescrita_edit'),
    path('eliminar_prensaescrita/<int:id_prensaescrita>', delete_prensaescrita, name='prensaescrita_delete'),
    path('prensaescrita/autofill', autofill_prensaescrita, name='prensaescrita_autofill'),
    path('prensaescrita/found', found_prensaescrita_by_name, name='prensaescrita_found'),

    path('telefono/', index_telefono, name='nomenclador_telefono'),
    path('nuevo_telefono/', add_telefono, name='telefono_new'),
    path('editar_telefono/<int:id_telefono>', update_telefono, name='telefono_edit'),
    path('eliminar_telefono/<int:id_telefono>', delete_telefono, name='telefono_delete'),
    path('telefono/autofill', autofill_telefono, name='telefono_autofill'),
    path('telefono/found', found_telefono_by_number, name='telefono_found'),

    path('email/', index_email, name='nomenclador_email'),
    path('nuevo_email/', add_email, name='email_new'),
    path('editar_email/<int:id_email>', update_email, name='email_edit'),
    path('eliminar_email/<int:id_email>', delete_email, name='email_delete'),
    path('email/autofill', autofill_email, name='email_autofill'),
    path('email/found', found_email_by_address, name='email_found'),

    path('gobierno/', index_gobierno, name='nomenclador_gobierno'),
    path('nuevo_gobierno/', add_gobierno, name='gobierno_new'),
    path('editar_gobierno/<int:id_gobierno>', update_gobierno, name='gobierno_edit'),
    path('eliminar_gobierno/<int:id_gobierno>', delete_gobierno, name='gobierno_delete'),
    path('gobierno/autofill', autofill_gobierno, name='gobierno_autofill'),
    path('gobierno/found', found_gobierno_by_name, name='gobierno_found'),

    path('organizacion/', index_organizacion, name='nomenclador_organizacion'),
    path('nuevo_organizacion/', add_organizacion, name='organizacion_new'),
    path('editar_organizacion/<int:id_organizacion>', update_organizacion, name='organizacion_edit'),
    path('eliminar_organizacion/<int:id_organizacion>', delete_organizacion, name='organizacion_delete'),
    path('organizacion/autofill', autofill_organizacion, name='organizacion_autofill'),
    path('organizacion/found', found_organizacion_by_name, name='organizacion_found'),

    path('responder/add/json', create_reponder_a_json, name="resp_new_json"),

]
