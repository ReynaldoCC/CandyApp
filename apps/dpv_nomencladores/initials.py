from django.db.models import Q
from .models import *


def create_initial():
    if not Provincia.objects.all().exists():
        Provincia.objects.bulk_create([
            Provincia(numero=1, nombre='Pinar del Rio'),
            Provincia(numero=2, nombre='Artemisa'),
            Provincia(numero=3, nombre='La Habana'),
            Provincia(numero=4, nombre='Mayabeque'),
            Provincia(numero=5, nombre='Matanzas'),
            Provincia(numero=6, nombre='Villa Clara'),
            Provincia(numero=7, nombre='Santi Spiritus'),
            Provincia(numero=8, nombre='Ciego de Avila'),
            Provincia(numero=9, nombre='Camagüey'),
            Provincia(numero=10, nombre='Las Tunas'),
            Provincia(numero=11, nombre='Holguin'),
            Provincia(numero=12, nombre='Gramma'),
            Provincia(numero=13, nombre='Santiago de Cuba'),
            Provincia(numero=14, nombre='Güatánamo'),
            Provincia(numero=15, nombre='Isla de la Juventud'),
        ])

    if not Municipio.objects.all().exists():
        provincia = Provincia.objects.get(nombre='La Habana')
        Municipio.objects.bulk_create([
            Municipio(numero=1, nombre='Playa', provincia=provincia),
            Municipio(numero=2, nombre='Plaza de la Revolución', provincia=provincia),
            Municipio(numero=3, nombre='Habana Vieja', provincia=provincia),
            Municipio(numero=4, nombre='Centro Habana', provincia=provincia),
            Municipio(numero=4, nombre='Cerro', provincia=provincia),
            Municipio(numero=5, nombre='Boyeros', provincia=provincia),
            Municipio(numero=6, nombre='Cotorro', provincia=provincia),
            Municipio(numero=7, nombre='La Lisa', provincia=provincia),
            Municipio(numero=8, nombre='Arroyo Naranjo', provincia=provincia),
            Municipio(numero=9, nombre='Habana del Este', provincia=provincia),
            Municipio(numero=10, nombre='10 de Octubre', provincia=provincia),
            Municipio(numero=11, nombre='San Miguel del Padrón', provincia=provincia),
            Municipio(numero=12, nombre='Marianao', provincia=provincia),
            Municipio(numero=13, nombre='Regla', provincia=provincia),
            Municipio(numero=14, nombre='Güanabacoa', provincia=provincia),
        ])
    else:
        pass

    if not ConsejoPopular.objects.all().exists():
        mun_playa = Municipio.objects.get(nombre='Playa')
        mun_plaza = Municipio.objects.get(nombre='Plaza de la Revolución')
        mun_cerro = Municipio.objects.get(nombre='Cerro')
        mun_ch = Municipio.objects.get(nombre='Centro Habana')

        ConsejoPopular.objects.bulk_create([
            ConsejoPopular(numero=1, nombre='Canal', municipio=mun_cerro),
            ConsejoPopular(numero=2, nombre='Palatino', municipio=mun_cerro),
            ConsejoPopular(numero=3, nombre='Los Sitios', municipio=mun_ch),
            ConsejoPopular(numero=4, nombre='San Leopoldo', municipio=mun_ch),
            ConsejoPopular(numero=5, nombre='Pueblo Nuevo', municipio=mun_ch),
            ConsejoPopular(numero=6, nombre='La Victoria', municipio=mun_ch),
            ConsejoPopular(numero=7, nombre='Colon', municipio=mun_ch),
            ConsejoPopular(numero=8, nombre='El Fanguito', municipio=mun_plaza),
            ConsejoPopular(numero=9, nombre='Vedado', municipio=mun_plaza),
            ConsejoPopular(numero=10, nombre='Nuevo Vedado', municipio=mun_plaza),
            ConsejoPopular(numero=11, nombre='Miramar', municipio=mun_playa),
            ConsejoPopular(numero=12, nombre='Buena Vista', municipio=mun_playa),
            ConsejoPopular(numero=13, nombre='Flores', municipio=mun_playa),
            ConsejoPopular(numero=14, nombre='Cubanacan', municipio=mun_playa),
        ])
    else:
        pass

    if not Concepto.objects.all().exists():
        Concepto.objects.bulk_create([
            Concepto(nombre='Propiedad'),
            Concepto(nombre='Usufructo Gratuito'),
            Concepto(nombre='Usufructo Arrendatario'),
        ])
    else:
        pass

    if not Calle.objects.all().exists():
        Calle.objects.bulk_create([
            Calle(nombre='2'),
            Calle(nombre='4'),
            Calle(nombre='6'),
            Calle(nombre='8'),
            Calle(nombre='10'),
            Calle(nombre='12'),
            Calle(nombre='14'),
            Calle(nombre='16'),
            Calle(nombre='18'),
            Calle(nombre='20'),
            Calle(nombre='22'),
            Calle(nombre='24'),
            Calle(nombre='26'),
            Calle(nombre='28'),
            Calle(nombre='30'),
            Calle(nombre='1ra'),
            Calle(nombre='3ra'),
            Calle(nombre='5ta'),
            Calle(nombre='7ma'),
            Calle(nombre='9na'),
            Calle(nombre='11'),
            Calle(nombre='13'),
            Calle(nombre='15'),
            Calle(nombre='17'),
            Calle(nombre='19'),
            Calle(nombre='21'),
            Calle(nombre='23'),
            Calle(nombre='25'),
            Calle(nombre='27'),
            Calle(nombre='29'),
            Calle(nombre='Paseo del Prado'),
            Calle(nombre='Ave. de los Precidentes'),
            Calle(nombre='Malecón'),
            Calle(nombre='Infanta'),
            Calle(nombre='Zanja'),
            Calle(nombre='Clavel'),
            Calle(nombre='Primelles'),
            Calle(nombre='Santa Catalina'),
            Calle(nombre='Palatino'),
            Calle(nombre='Via Blanca'),
            Calle(nombre='Calzada del Cerro'),
            Calle(nombre='Calzada de 10 de Octubre'),
            Calle(nombre='Coco'),
            Calle(nombre='A'),
            Calle(nombre='B'),
            Calle(nombre='C'),
            Calle(nombre='D'),
            Calle(nombre='E'),
            Calle(nombre='F'),
            Calle(nombre='G'),
            Calle(nombre='H'),
            Calle(nombre='I'),
            Calle(nombre='J'),
            Calle(nombre='K'),
            Calle(nombre='L'),
            Calle(nombre='M'),
            Calle(nombre='N'),
            Calle(nombre='O'),
            Calle(nombre='P'),
            Calle(nombre='Dominguez'),
            Calle(nombre='Montoro'),
            Calle(nombre='Desagüe'),
            Calle(nombre='Estrella'),
            Calle(nombre='Maloja'),
            Calle(nombre='Oquendo'),
            Calle(nombre='Marques Gonzalez'),
            Calle(nombre='San Rafael'),
            Calle(nombre='San Miguel'),
            Calle(nombre='San Martin'),
            Calle(nombre='San José'),
            Calle(nombre='San Lázaro'),
            Calle(nombre='Cuba'),
            Calle(nombre='Aguiar'),
            Calle(nombre='Orrelly'),
            Calle(nombre='Habana'),
            Calle(nombre='Obispo'),
            Calle(nombre='Carcel'),
            Calle(nombre='Obrapía'),
            Calle(nombre='Lamparilla'),
            Calle(nombre='Amargura'),
            Calle(nombre='Soledad'),
            Calle(nombre='Sol'),
            Calle(nombre='Chacón'),
            Calle(nombre='Cuarteles'),
            Calle(nombre='Industría'),
            Calle(nombre='Colon'),
            Calle(nombre='Consulado'),
            Calle(nombre='Genios'),
            Calle(nombre='Crespo'),
            Calle(nombre='Amistad'),
            Calle(nombre='Aguila'),
            Calle(nombre='Neptuno'),
            Calle(nombre='Carlos III'),
            Calle(nombre='Hospital'),
            Calle(nombre='Compostela'),
            Calle(nombre='Empedrado'),
            Calle(nombre='San Ignacio'),
            Calle(nombre='Ayestaran'),
            Calle(nombre='Tulipan'),
            Calle(nombre='Muralla'),
            Calle(nombre='Belen'),
            Calle(nombre='Cienfuegos'),
            Calle(nombre='Monte'),
            Calle(nombre='Belascoain'),
            Calle(nombre='Ave. Boyeros'),
        ])
    else:
        pass

    if not Piso.objects.all().exists():
        Piso.objects.bulk_create([
            Piso(nombre='Zotano'),
            Piso(nombre='Planta Baja'),
            Piso(nombre='1er Piso'),
            Piso(nombre='2do Piso'),
            Piso(nombre='3er Piso'),
            Piso(nombre='4to Piso'),
            Piso(nombre='5to Piso'),
            Piso(nombre='6to Piso'),
            Piso(nombre='7mo Piso'),
            Piso(nombre='8vo Piso'),
            Piso(nombre='Azotea'),
        ])
    else:
        pass

    if not CentroTrabajo.objects.all().exists():
        mun_playa = Municipio.objects.get(nombre='Playa')
        mun_plaza = Municipio.objects.get(nombre='Plaza de la Revolución')
        mun_cerro = Municipio.objects.get(nombre='Cerro')
        mun_ch = Municipio.objects.get(nombre='Centro Habana')
        CentroTrabajo.objects.bulk_create([
            CentroTrabajo(nombre='Dirección Provincialde Vivienda La Habana', siglas='DPVHAB',
                          numero=16, oc=True, municipio=mun_plaza),
            CentroTrabajo(nombre='Dirección Municipal de Vivienda Plaza de la Revolución', siglas='DMVPLZ',
                          numero=1, oc=False, municipio=mun_plaza),
            CentroTrabajo(nombre='Dirección Municipal de Vivienda Playa', siglas='DMVPLY',
                          numero=2, oc=False, municipio=mun_playa),
            CentroTrabajo(nombre='Dirección Municipal de Vivienda Cerro', siglas='DMVCER',
                          numero=3, oc=False, municipio=mun_cerro),
            CentroTrabajo(nombre='Dirección Municipal de Vivienda Centro Habana', siglas='DMVCHA',
                          numero=4, oc=False, municipio=mun_ch),
        ])
    else:
        pass

    if not AreaTrabajo.objects.all().exists():
        AreaTrabajo.objects.bulk_create([
            AreaTrabajo(nombre='Dirección Geneneral', numero=1),
            AreaTrabajo(nombre='Subdirección de Informática', numero=2),
            AreaTrabajo(nombre='Depto. de Informática', numero=3),
            AreaTrabajo(nombre='Subdirección de Economía', numero=4),
            AreaTrabajo(nombre='Depto. de Economía', numero=5),
            AreaTrabajo(nombre='Depto. de Recursos Humanos', numero=6),
            AreaTrabajo(nombre='Depto. de Atención a la Población', numero=7),
            AreaTrabajo(nombre='Depto. de Subcidios', numero=8),
        ])
    else:
        pass

    if not Organizacion.objects.all().exists():
        Organizacion.objects.bulk_create([
            Organizacion(nombre='Unión de Jovenes de Cuba (UJC)'),
            Organizacion(nombre='Partido Comunista de Cuba (PCC)'),
            Organizacion(nombre='Organización de Pioneros Jose Martí (OPJM)'),
            Organizacion(nombre='Federación de Estudiantes Universitarios (FEU)'),
            Organizacion(nombre='Federación de Estudiantes de la Enseñanza Media (FEEM)'),
            Organizacion(nombre='Central de Trabajadores de Cuba (CTC)'),
            Organizacion(nombre='Comité de Defensa de la Revolución (CDR)'),
            Organizacion(nombre='Federación de Mujeres de Cuba (FMC)'),
        ])
    else:
        pass

    if not Genero.objects.all().exists():
        Genero.objects.bulk_create([
            Genero(nombre='Femenino', sigla='F'),
            Genero(nombre='Masculino', sigla='M'),
            Genero(nombre='Otro', sigla='O'),
        ])
    else:
        pass

    if not CodificadorAsunto.objects.all().exists():
        CodificadorAsunto.objects.bulk_create([
            CodificadorAsunto(nombre='inmuebles (Casas, Departamentos, Ciudadelas, etc..)', numero=101),
            CodificadorAsunto(nombre='Ampliaciones', numero=102),
            CodificadorAsunto(nombre='Permuta entre particulares', numero=103),
            CodificadorAsunto(nombre='Permuta entre particulares y el estado', numero=104),
            CodificadorAsunto(nombre='Albergues', numero=105),
            CodificadorAsunto(nombre='Inversión y rehabilitación de vivienda', numero=106),
            CodificadorAsunto(nombre='Materiales de construcción (Comissiones de dsitribución centros expendedores, etc...)', numero=107),
            CodificadorAsunto(nombre='Reparaciones y construcciones (Núcleo Familiar)', numero=108),
            CodificadorAsunto(nombre='Reparaciones y contrucciones colectivas (edificios multifamiliares, ciudadelas, etc...)', numero=109),
            CodificadorAsunto(nombre='Créditos', numero=110),
            CodificadorAsunto(nombre='Incorporación a microbrigadas bajo costo propio o esfuerzo propio', numero=111),
        ])
    else:
        pass

    if not TipoQueja.objects.all().exists():
        TipoQueja.objects.bulk_create([
            TipoQueja(nombre='Denuncia', numero=1),
            TipoQueja(nombre='Consulta', numero=2),
            TipoQueja(nombre='Queja', numero=3),
        ])
    else:
        pass

    if not TipoProcedencia.objects.all().exists():
        TipoProcedencia.objects.bulk_create([
            TipoProcedencia(id=1, nombre='Anónimo', cant_dias=30, enviar=True),
            TipoProcedencia(id=2, nombre='Prensa Escrita', cant_dias=30, enviar=True),
            TipoProcedencia(id=3, nombre='Personal', cant_dias=30, enviar=True),
            TipoProcedencia(id=4, nombre='Teléfono', cant_dias=30, enviar=False),
            TipoProcedencia(id=5, nombre='Correo', cant_dias=30, enviar=True),
            TipoProcedencia(id=6, nombre='Empresa', cant_dias=30, enviar=True),
            TipoProcedencia(id=7, nombre='Gobierno', cant_dias=30, enviar=True),
            TipoProcedencia(id=8, nombre='Organización', cant_dias=30, enviar=True),
        ])
    else:
        pass

    if not Estado.objects.all().exists():
        Estado.objects.bulk_create([
            Estado(id=1, nombre='Radicada'),
            Estado(id=2, nombre='Asignada'),
            Estado(id=3, nombre='En proceso'),
            Estado(id=4, nombre='Pendiente de Aprobación Jefe'),
            Estado(id=5, nombre='Pendiente de Aprobación Dir.'),
            Estado(id=6, nombre='Pendiente de Notificación'),
            Estado(id=7, nombre='Concluida'),
            Estado(id=8, nombre='Trasladada'),
            Estado(id=9, nombre='Rechazada'),
            Estado(id=10, nombre='Respuesta Rechazada'),
            Estado(id=11, nombre='Sin Estado'),
        ])
    else:
        pass

    if not Procedencia.objects.all().exists():
        Procedencia.objects.bulk_create([
            # Procedencia(nombre='', enviar=True, tipo=, tipo_contenido=, id_objecto=, objecto_contenido=),
        ])
    else:
        pass

    if not ClasificacionRespuesta.objects.all().exists():
        ClasificacionRespuesta.objects.bulk_create([
            ClasificacionRespuesta(nombre='Solucionada', codigo='S'),
            ClasificacionRespuesta(nombre='Pendiente Solución', codigo='PS'),
            ClasificacionRespuesta(nombre='Explicada Causa de No Solución', codigo='ECNS'),
        ])
    else:
        pass

    if not PrensaEscrita.objects.all().exists():
        PrensaEscrita.objects.bulk_create([
            PrensaEscrita(nombre='Periódico Gramma', siglas='GRM'),
            PrensaEscrita(nombre='Revista Mujeres', siglas='MUJ'),
        ])
    else:
        pass

    if Calle.objects.exists() and Municipio.objects.exists():
        for mun in Municipio.objects.exclude(Q(nombre__icontains="centro habana")|Q(nombre__icontains="habana vieja")):
            mun.calle_set.set(Calle.objects.filter(id__gte="30"))
        Municipio.objects.filter(nombre__icontains="centro habana").first().calle_set.set(
            Calle.objects.filter(id__in=[33, 34, 35, ])
        )
