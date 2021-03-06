'use strict';

function abrir_modal(url, id=null)
{
    $('#popup').load(url, function(id)
    {
        $(this).modal('show');
    });
    return false;
}

function cerrar_modal()
{
    $('#popup').modal('hide');
    return false;
}

var DPVQuejas = function () {
    var queja_form;
    var asigne_form;
    var response_form;
    var tmp;
    let persona = null;


    var _makeAlert = function(type, text, success, negate, title=null, accept=null, cancel=null, plus=null) {
        let dataplus = plus || tmp;
        Swal.fire({
            title: title || "Error",
            html: text,
            icon: type,
            showCloseButton: true,
            showCancelButton: true,
            focusConfirm: false,
            confirmButtonText: accept || '<i class="fa fa-thumbs-up"></i> Si',
            confirmButtonAriaLabel: 'Correto',
            cancelButtonText: cancel || '<i class="fa fa-thumbs-down"></i> No',
            cancelButtonAriaLabel: 'Cancelar',
            showClass: {
                popup: 'animated fadeInDown faster',
            },
            hideClass: {
                popup: 'animated fadeOutUp faster',
            },
        }).then((result) => {
            if (result.value) {
                if (success != null) {
                    if (typeof(success) == 'function')
                        success(dataplus);
                }
            } else {
                if (negate != null) {
                    negate(dataplus);
                }
            }
        });
    };
    var _initQuejas = function () {

    };
    var _initQuejaForm = function () {

    	let $procedencias = $('#id_queja-procedencia').selectize({
            create: false,
            maxItems: 1,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            placeholder: "Selecione una procedencia",
        });
    	let $damnificados = $('#id_queja-damnificado').selectize({
            create: false,
            maxItems: 1,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            placeholder: "Selecione un damnificado",
			onChange: function (value) {
				if (!value.length) return;
				if (!persona || value !== persona.id)
					_getDamnData(value);
			},
        });
    	var $dir_calle = $("#id_queja-dir_calle").selectize({
            placeholder: "Selecione una calle",
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            allowEmptyOption: false,
            selectOnTab: true,
            createOnBlur: false,
            create: false,
        });
        var $dir_entrecalle1 = $("#id_queja-dir_entrecalle1").selectize({
            placeholder: "Selecione una calle ",
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            allowEmptyOption: false,
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $dir_entrecalle2 = $("#id_queja-dir_entrecalle2").selectize({
            required: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            placeholder: "Selecione una calle ",
            allowEmptyOption: false,
            selectOnTab: true,
            createOnBlur: false,
            create: false,
        });
        var $dir_municipio = $("#id_queja-dir_municipio").selectize({
            create: false,
            placeholder: "Selecione un municipio",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $.ajax({
                    url: '/nomenclador/consejopopular/filter/' + value,
                    success: function(results) {
                        let current_value = $dir_cpopular[0].selectize.getValue();
                        let exist = false;
                        for (let i = 0; i < results.length; i++)
                            if (results[i].id == current_value) {
                                exist = true;
                            }
                        // console.log(exist, 'pop');
                        if (!exist)
                            $dir_cpopular[0].selectize.clear();
                        $dir_cpopular[0].selectize.clearOptions();
                        $dir_cpopular[0].selectize.load(function (callback) {
                            callback(results);
                        });

                    }
                });
                $.ajax({
                    url: '/nomenclador/calle/filter/' + value,
                    success: function(results) {
                        let current_value1 = $dir_calle[0].selectize.getValue();
                        let current_value2 = $dir_entrecalle1[0].selectize.getValue();
                        let current_value3 = $dir_entrecalle2[0].selectize.getValue();
                        let exist1 = false;
                        let exist2 = false;
                        let exist3 = false;
                        for (let i = 0; i < results.length; i++) {
                            if (results[i].id == current_value1) {
                                exist1 = true;
                            }
                            if (results[i].id == current_value2) {
                                exist2 = true;
                            }
                            if (results[i].id == current_value3) {
                                exist3 = true;
                            }
                        }
                        if (!exist1)
                            $dir_calle[0].selectize.clear();
                        $dir_calle[0].selectize.clearOptions();
                        $dir_calle[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist2)
                            $dir_entrecalle1[0].selectize.clear();
                        $dir_entrecalle1[0].selectize.clearOptions();
                        $dir_entrecalle1[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist3)
                            $dir_entrecalle2[0].selectize.clear();
                        $dir_entrecalle2[0].selectize.clearOptions();
                        $dir_entrecalle2[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
            },
        });
        var $dir_cpopular = $("#id_queja-dir_cpopular").selectize({
            placeholder: "Selecione un consejo popular",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: false,
            create: false,
        });
        var $asunto = $("#id_queja-asunto").selectize({
            create: false,
            placeholder: "Selecione un asunto",
            allowEmptyOption: false,
        });
        var $tipo = $("#id_queja-tipo").selectize({
            create: false,
            placeholder: "Selecione un tipo",
            allowEmptyOption: false,
        });

        $.validator.setDefaults({
            errorClass: 'text-danger',
            highlight: function(element) {
                $(element).addClass('is-invalid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },
            // Validate only visible fields
			ignore: ":hidden",

            errorPlacement: function(error, element) {
                if (element[0].attributes['type'].nodeValue === 'select-one' || element[0].attributes['type'].nodeValue === 'select-multiple')
                    error.insertBefore(element.parent());
                else
                    error.insertBefore(element);
            },

        });
        let validator_form = queja_form.validate({
			rules: {
				'queja-procedencia': {
				    required: true,
				},
				'queja-damnificado': {
				    required: true,
				},
				'queja-no_procendencia': {},
				'queja-no_radicacion': {},
				'queja-dir_calle': {
				    required: true,
				},
				'queja-dir_num': {
				    required: true,
				},
				'queja-dir_entrecalle1': {
				    required: true,
				},
				'queja-dir_entrecalle2': {
				    required: true,
				},
				'queja-dir_municipio': {
				    required: true,
				},
				'queja-dir_cpopular': {
				    required: true,
				},
				'queja-referencia': {},
				'queja-asunto': {
				    required: true,
				},
				'queja-tipo': {
				    required: true,
				},
				'queja-asunto_texto': {
				    required: true,
                    maxlength: 300,
				},
				'queja-texto': {
				    required: true,
                    maxlength: 3000,
                    minlength: 20,
				},
			},
			messages:{
				'queja-tipo_procedencia': {
				    required: "Tiene que seleccionar un tipo de procedencia.",
				},
				'queja-tipo_procedencia-selectized': {
				    required: "Tiene que seleccionar un tipo de procedencia.",
				},
				'email-email': {
				    required: "El email no puede quedar en blanco.",
				    email: "El email debe ser una dirección de correo electrónico válido.",
				},
				'pe-nombre': {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "El nombre no puede tener más de 30 caracteres.",
				},
				'pe-siglas': {
				    required: "Las siglas no pueden quedar en blanco.",
                    maxlength: "Las siglas no pueden más de 10 caracteres.",
				},
				'person_procedence-ci': {
				    required: "El CI no puede quedar en blanco.",
				    digits: "El CI solo puede tener dígitos.",
                    maxlength: "El CI no puede tener más de 11 dígitos.",
                    minlength: "El CI no puede tener menos de 11 dígitos.",
				},
				'person_procedence-nombre': {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "El nombre no puede tener más de 30 caracteres.",
				},
				'person_procedence-apellidos': {
				    required: "Los apellidos no pueden quedar en blanco.",
                    maxlength: "Los apellidos no pueden tener más de 50 caracteres.",
				},
				'person_procedence-genero': {
				    required: "Tiene que seleccionar un género.",
				},
				'person_procedence-genero-selectized': {
				    required: "Tiene que seleccionar un género.",
				},
				'person_procedence-email_address': {
				    email: "El email debe ser una dirección de correo electrónico válido.",
				},
				'person_procedence-movil': {
                    digits: "El movil solo puede tener dígitos.",
                    maxlength: "El movil no pueden tener más de 8 dígitos.",
                    minlength: "El movil no puede tener menos de 8 dígitos.",
                    remote: "Ya existe otra persona registrada con ese movil",
                },
				'person_procedence-telefono': {
				    required: "El teléfono no puede quedar en blanco.",
                    digits: "El teléfono solo puede tener dígitos.",
                    maxlength: "El teléfono no pueden tener más de 8 dígitos.",
                    minlength: "El teléfono no puede tener menos de 8 dígitos.",
				},
				'person_procedence-direccion_calle': {
				    required: "Tiene que seleccionar una calle.",
				},
				'person_procedence-direccion_calle-selectized': {
				    required: "Tiene que seleccionar una calle.",
				},
				'person_procedence-direccion_numero': {
				    required: "El número no puede quedar en blanco.",
				},
				'person_procedence-direccion_entrecalle1': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'person_procedence-direccion_entrecalle1-selectized': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'person_procedence-direccion_entrecalle2': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'person_procedence-direccion_entrecalle2-selectized': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'person_procedence-municipio': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'person_procedence-municipio-selectized': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'person_procedence-cpopular': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'person_procedence-cpopular-selectized': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'telefono-numero': {
				    required: "El núemro de teléfono no puede quedar en blanco.",
                    digits: "El núemro de teléfono solo puede tener dígitos.",
                    maxlength: "El núemro de teléfono no pueden tener más de 8 dígitos.",
                    minlength: "El núemro de teléfono no puede tener menos de 8 dígitos.",
				},
				'empresa-nombre': {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "El nombre no puede tener más de 100 caracteres.",
				},
				'empresa-sigla': {
				    required: "Las siglas no pueden quedar en blanco.",
                    maxlength: "Las siglas no pueden tener más de 10 caracteres.",
				},
				'empresa-telefono': {
				    required: "El teléfono no puede quedar en blanco.",
                    digits: "El teléfono solo puede tener dígitos.",
                    maxlength: "El teléfono no pueden tener más de 8 dígitos.",
                    minlength: "El teléfono no puede tener menos de 8 dígitos.",
				},
				'empresa-movil': {
                    digits: "El movil solo puede tener dígitos.",
                    maxlength: "El movil no pueden tener más de 8 dígitos.",
                    minlength: "El movil no puede tener menos de 8 dígitos.",
                },
				'empresa-nombre_contacto': {
				    required: "El nombre de contacto no puede quedar en blanco.",
				    maxlength: "El nombre de contacto no puede tener más de 200 caracteres.",
				},
				'empresa-email_address': {
				    email: "El email debe ser una dirección de correo electrónico válido.",
				},
				'empresa-codigo_nit': {
				    required: "El código NIT no puede quedar en blanco.",
				},
				'empresa-codigo_reuup': {
				    required: "El código REEUP no puede quedar en blanco.",
				},
				'empresa-municipio': {
				    required:  "Tiene que seleccionar un municipio.",
				},
				'empresa-cpopular': {
				    required:  "Tiene que seleccionar un consejo popular.",
				},
				'empresa-municipio-selectized': {
				    required:  "Tiene que seleccionar un municipio.",
				},
				'empresa-cpopular-selectized': {
				    required:  "Tiene que seleccionar un consejo popular.",
				},
				'empresa-direccion_calle': {
				    required: "Tiene que seleccionar una calle.",
				},
				'empresa-direccion_calle-selectized': {
				    required: "Tiene que seleccionar una calle.",
				},
				'empresa-direccion_numero': {
				    required: "El número no puede quedar en blanco.",
				},
				'empresa-direccion_entrecalle1': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'empresa-direccion_entrecalle1-selectized': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'empresa-direccion_entrecalle2': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'empresa-direccion_entrecalle2-selectized': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'gob-nombre': {
				    required: "El nombre no puede quedar en blanco.",
				    maxlength: "El nombre no puede tener más 50 caracteres.",
				},
				'organiza-nombre': {
				    required: "El nombre no puede quedar en blanco.",
				    maxlength: "El nombre no puede tener más 50 caracteres.",
				},
				'personas_list': {
				    required: "Tiene que seleccionar una persona de la lista.",
				},
				'personas_list-selectized': {
				    required: "Tiene que seleccionar una persona de la lista.",
				},
				'person_queja-ci': {
				    required: "El CI no puede quedar en blanco.",
				    digits: "El CI solo puede tener dígitos.",
                    maxlength: "El CI no puede tener más de 11 dígitos.",
                    minlength: "El CI no puede tener menos de 11 dígitos.",
				},
				'person_queja-nombre': {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "Los apellidos no pueden tener más de 30 caracteres.",
				},
				'person_queja-apellidos': {
				    required: "Los apellidos no pueden quedar en blanco.",
                    maxlength: "Los apellidos no pueden tener más de 50 caracteres.",
				},
				'person_queja-genero': {
				    required: "Tiene que seleccionar un género.",
				},
				'person_queja-genero-selectized': {
				    required: "Tiene que seleccionar un género.",
				},
				'person_queja-email_address': {
				    email: "El email debe ser una dirección de correo electrónico válido.",
				},
				'person_queja-movil': {
                    digits: "El movil solo puede tener dígitos.",
                    maxlength: "El movil no pueden tener más de 8 dígitos.",
                    minlength: "El movil no puede tener menos de 8 dígitos.",
                    remote: "Ya existe otra persona registrada con ese movil",
                },
				'person_queja-telefono': {
				    required: "El teléfono no puede quedar en blanco.",
                    digits: "El teléfono solo puede tener dígitos.",
                    maxlength: "El teléfono no pueden tener más de 8 dígitos.",
                    minlength: "El teléfono no puede tener menos de 8 dígitos.",
                },
				'person_queja-direccion_calle': {
				    required: "Tiene que seleccionar una calle.",
				},
				'person_queja-direccion_calle-selectized': {
				    required: "Tiene que seleccionar una calle.",
				},
				'person_queja-direccion_numero': {
				    required: "El número no puede quedar en blanco.",
				},
				'person_queja-direccion_entrecalle1': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'person_queja-direccion_entrecalle1-selectized': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'person_queja-direccion_entrecalle2': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'person_queja-direccion_entrecalle2-selectized': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'person_queja-cpopular': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'person_queja-cpopular-selectized': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'person_queja-municipio': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'person_queja-municipio-selectized': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'queja-no_procendencia': {},
				'queja-no_radicacion': {},
				'queja-dir_calle': {
				    required: "Tiene que seleccionar una calle.",
				},
				'queja-dir_calle-selectized': {
				    required: "Tiene que seleccionar una calle.",
				},
				'queja-dir_num': {
				    required: "El número no puede quedar en blanco.",
				},
				'queja-dir_entrecalle1': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'queja-dir_entrecalle1-selectized': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'queja-dir_entrecalle2': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'queja-dir_entrecalle2-selectized': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'queja-dir_municipio': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'queja-dir_municipio-selectized': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'queja-dir_cpopular': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'queja-dir_cpopular-selectized': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'queja-referencia': {},
				'queja-asunto': {
				    required: "Tiene que seleccionar un código de asunto.",
				},
				'queja-asunto-selectized': {
				    required: "Tiene que seleccionar un código de asunto.",
				},
				'queja-tipo': {
				    required: "Tiene que seleccionar un tipo de queja.",
				},
				'queja-tipo-selectized': {
				    required: "Tiene que seleccionar un tipo de queja.",
				},
				'queja-asunto_texto': {
				    required: "El texto del asunto no puede quedar en blanco.",
                    maxlength: "El texto del asunto no puede más de 300 caracteres.",
				},
				'queja-texto': {
				    required: "El cuerpo de la queja no puede quedar en blanco.",
                    maxlength: "El cuerpo de la queja no puede tener más de 3000 caracteres.",
                    minlength: "El cuerpo de la queja no puede tener menos de 20 caracteres.",
				},
				'queja-responder_a': {
				    required: "El responder a no puede quedar en blanco.",
				},
				'queja-responder_a-selectized': {
				    required: "El responder a no puede quedar en blanco.",
				},
			},
		});

		$('input[id$="-selectized"]').attr('name', function () {
            let name = this.id.slice(3);
            return name;
        });
		$("#id_queja-same_address").on("click", function () {
			if (this.checked) {
				if ($("#id_queja-damnificado").val())
					_setValuesAddressQueja();
				else
					this.checked = false;
			} else {
				$dir_calle[0].selectize.setValue('', false);
				$dir_entrecalle1[0].selectize.setValue('', false);
				$dir_entrecalle2[0].selectize.setValue('', false);
				$dir_municipio[0].selectize.setValue('', false);
				$dir_cpopular[0].selectize.setValue('', false);
				$("#id_queja-dir_num").val('');
			}
		});

        var _setValuesAddressQueja = function () {
        	if (persona && persona.objecto_contenido) {
				$("#id_queja-dir_municipio")[0].selectize.setValue(persona.objecto_contenido.municipio, false);
				$("#id_queja-dir_cpopular")[0].selectize.setValue(persona.objecto_contenido.cpopular, false);
				$("#id_queja-dir_calle")[0].selectize.setValue(persona.objecto_contenido.direccion_calle, false);
				$("#id_queja-dir_entrecalle1")[0].selectize.setValue(persona.objecto_contenido.direccion_entrecalle1, false);
				$("#id_queja-dir_entrecalle2")[0].selectize.setValue(persona.objecto_contenido.direccion_entrecalle2, false);
				$("#id_queja-dir_num").val(persona.objecto_contenido.direccion_numero);
			} else{
        		$("#id_queja-same_address").trigger("click");
			}

        };
        var _getDamnData = function (value) {
        	let url = damn_detail_url.replace('0', value)
			$.ajax({
				type: "GET",
				url: url,
				success: function (response) {
					persona = response;
				}
			})
		};
		// validator_form.resetForm();
    };
    var _initQuejaAsignaForm = function () {
        var $personas_list = $('#id_tecnico').selectize({
            create: false,
            maxItems: 1,
            placeholder: "Selecione un técnico",
            allowEmptyOption: false,
        });

        $.validator.setDefaults({
            errorClass: 'text-danger',
            highlight: function(element) {
                $(element).addClass('is-invalid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },
            // Validate only visible fields
			ignore: ":hidden",

            errorPlacement: function(error, element) {
                if (element[0].attributes['type']) {
                    if (element[0].attributes['type'].nodeValue == 'select-one' || element[0].attributes['type'].nodeValue == 'select-multiple')
                        error.insertBefore(element.parent());
                    else
                        error.insertBefore(element);
                } else {
                    error.insertBefore(element);
                }
            },

        });
        let validator_form = asigne_form.validate({
			rules: {
				tecnico: {
				    required: true,
				},
				observaciones: {
                    maxlength: 500,
				},
			},
			messages:{
				tecnico: {
				    required: "Tiene que seleccionar un técnico.",
				},
				observaciones: {
                    maxlength: "las observaciones no puede tener más de 500 caracteres.",
				},
            },
		});
    };
    var _initResponse = function () {
        $("#show_form").on("click", function (e) {
            $("#show_detail").removeClass("my-hidden");

            $("#show_form").addClass("my-hidden");
            $("#show_form_div").removeClass("my-hidden");
            $("#show_detail_div").addClass("my-hidden");
            if ($('button[type="submit"]').hasClass("disabled")) $('button[type="submit"]').removeClass("disabled");
        });
        $("#show_detail").on("click", function (e) {
            $("#show_detail").addClass("my-hidden");
            $("#show_form").removeClass("my-hidden");
            $("#show_form_div").addClass("my-hidden");
            $("#show_detail_div").removeClass("my-hidden");
            $('button[type="submit"]').addClass("disabled");
        });
        var $nivel_solucion = $("#id_nivel_solucion").selectize({
            create: false,
            placeholder: "Selecione un nivel",
            allowEmptyOption: false,
        });
        var $clasificacion = $("#id_clasificacion").selectize({
            create: false,
            placeholder: "Selecione una clasificación",
            allowEmptyOption: false,
        });
        var $conclusion_caso = $("#id_conclusion_caso").selectize({
            create: false,
            placeholder: "Selecione una conclusión",
            allowEmptyOption: false,
        });
    };
    var _initResponseForm = function () {
        $.validator.setDefaults({
            errorClass: 'text-danger',
            highlight: function(element) {
                $(element).addClass('is-invalid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },
            // Validate only visible fields
			ignore: ":hidden",

            errorPlacement: function(error, element) {
                error.insertBefore(element);
            },

        });
        let validator_form = response_form.validate({
			rules: {
				'gestion': {
				    required: true,
                    maxlength: 3000,
                    minlength: 20,
				},
				'texto': {
				    required: true,
                    maxlength: 3000,
                    minlength: 20,
				},
			},
			messages:{
				'gestion': {
				    required: "No puede dejar texto de la gestion en blanco.",
                    maxlength: "El texto de la gestion no puede tener mas de 3000 caracteres.",
                    minlength: "El texto de la gestion no puede tener menos de 20 caracteres.",
				},
				'texto': {
				    required: "No puede dejar el texto de la respuesta en blanco.",
                    maxlength: "El texto de la respuesta no puede tener mas de 3000 caracteres.",
                    minlength: "El texto de la respuesta no puede tener menos de 20 caracteres.",
				},
			},
		});
    };
    var _initApruebaForm = function () {
        let aprobe_form = $("#aprobe_form");
        let reject_form = $("#reject_form");
        $(".do-ok").on("click", function (e) {
            e.preventDefault();
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: 'btn btn-success ml-1',
                    cancelButton: 'btn btn-danger mr-1'
                },
                buttonsStyling: false
            })
            const swalWithArgumentButtons = Swal.mixin({
                customClass: {
                    confirmButton: 'btn btn-success ml-1',
                    cancelButton: 'btn btn-danger mr-1'
                },
                confirmButtonText: 'Aprobar',
                input: 'textarea',
                inputAttributes: {
                    autocapitalize: 'off',
                    col: '2',
                    placeholder: 'Argumente ...',
                },
                buttonsStyling: false
            })

            swalWithBootstrapButtons.fire({
                title: 'Está seguro?',
                text: "Desea aprobar esta respuesta",
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Si, Aprobarla!',
                cancelButtonText: 'Cancelar',
                reverseButtons: true
                }).then((result) => {
                if (result) {
                    swalWithArgumentButtons.fire(
                        'Bien!',
                        'Si desea puede argumentar su aprobación.',
                        'warning'
                    ).then((result) => {
                        console.log(result);
                        if (!result.dismiss){
                            $('#id_observacion_jefe').val(result.value);
                            aprobe_form.submit();
                        }
                    })
                }
            })
        });
        $(".do-reject").on("click", function (e) {
            e.preventDefault();
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: 'btn btn-danger ml-1',
                    cancelButton: 'btn btn-secondary mr-1'
                },
                buttonsStyling: false
            })
            const swalWithArgumentButtons = Swal.mixin({
                customClass: {
                    confirmButton: 'btn btn-danger ml-1',
                    cancelButton: 'btn btn-secondary mr-1'
                },
                confirmButtonText: 'Rechazar',
                input: 'textarea',
                // validationMessage: {
                //     required: 'Este campo es obligatorio',
                // },
                inputValidator: (value) => {
                    return !value && 'El argumento es obligatorio!'
                },
                inputAttributes: {
                    autocapitalize: 'off',
                    col: '2',
                    required: 'required',
                    placeholder: 'Argumente ...',
                },
                buttonsStyling: false
            })

            swalWithBootstrapButtons.fire({
                title: 'Está seguro?',
                text: "Desea rechazar esta respuesta",
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Si, Rechazarla!',
                cancelButtonText: 'Cancelar',
                reverseButtons: true
                }).then((result) => {
                if (result) {
                    swalWithArgumentButtons.fire(
                        'Bien!',
                        'Para poder rechazar la respuesta tiene que argumentar la razón.',
                        'error'
                    ).then((result) => {
                        console.log(result);
                        if (!result.dismiss){
                            $('#id_argumento').val(result.value);
                            reject_form.submit();
                        }
                    }).catch(error => {
                        Swal.showValidationMessage(
                            `Request failed: ${error}`
                        )
                    })
                }
            })
        })
    };
	var _initStats = function (translations = null, dataGraph = null) {
		if (translations) {
			$('#stats-table').DataTable({
				responsive: true,
				order: [ 0, 'desc' ],
				pageLength: 20,
				lengthMenu: [[20, 30, 50 , -1], [20, 30, 50 , "Todos"]],
				sScrollX: "100%",
				// fixedColumns:   {
				// 	leftColumns: 1,
				// },
				language: {
					"decimal": "",
					"emptyTable": translations.emptyTable,
					"info": translations.info_init + " _START_ a _END_ de _TOTAL_ " + translations.info_end,
					"infoEmpty": translations.infoEmpty,
					"infoFiltered": "(" + translations.infoFiltered_init + " _MAX_ " + translations.infoFiltered_end + ")",
					"infoPostFix": "",
					"thousands": ",",
					"lengthMenu": translations.lengthMenu_init + " _MENU_ " + translations.lengthMenu_end,
					"loadingRecords": translations.loadingRecords,
					"processing": translations.processing,
					"search":  translations.search,
					"zeroRecords": translations.zeroRecords,
					"paginate": {
							"first": translations.first,
							"last": translations.last,
							"next": translations.next,
							"previous": translations.previous,
					}
				},
			});
		}
		if (dataGraph && dataGraph.count > 0) {
            $(window).on('load', function () {
                var canvas = $('#Graph_result');
                let stepSizeCalc = function () {
                	let max = 0
					dataGraph.cantquejas.map(function (num) {
						if (num > max) {
							max = num;
						}
					})
					return (max / 5 >= 1)?Math.floor(max / 5):1;
				}
				let stepSize = stepSizeCalc()
				let MaxCalc = function() {
                	let max = 0
					dataGraph.cantquejas.map(function (num) {
						if (num > max) {
							max = num;
						}
					})
					return max;
				}
				let Max = MaxCalc() + 3 * stepSize;
                new Chart(canvas, {
                    type: 'bar',
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            position: 'top',
                            text: 'Gráfico de Quejas'
                        },
                        scales: {
                            yAxes: [{
                                id: 'left',
                                type: 'linear',
                                position: 'left',
                                ticks: {
                                    min: 0,
									max: Max,
									stepSize: stepSize,
                                }
                            }, {
                                id: 'right',
                                type: 'linear',
                                position: 'right',
                                ticks: {
                                    min: 0,
									max: Max,
									stepSize: stepSize,
                                }
                            }]
                        }
                    },
                    data: {
                        labels: dataGraph.columns,
                        datasets: [{
                            label: 'Total',
                            yAxisID: 'right',
                            data: dataGraph.cantquejas,
                            backgroundColor: "#007bff",
                            borderColor: "#007bff",
                            borderWidth: 1,
                        }, {
                            label: 'Asignadas a Dpto',
                            yAxisID: 'right',
                            data: dataGraph.asignadadpto,
                            backgroundColor: "#28a745",
                            borderColor: "#28a745",
                            borderWidth: 1,
                        }, {
                            label: 'Asignada a Técnico',
                            yAxisID: 'right',
                            data: dataGraph.asignadatec,
                            backgroundColor: "#ffc107",
                            borderColor: "#ffc107",
                            borderWidth: 1,
                        }, {
                            label: 'Con Respuesta',
                            yAxisID: 'right',
                            data: dataGraph.quejarespondida,
                            backgroundColor: "#dc3545",
                            borderColor: "#dc3545",
                            borderWidth: 1,
                        }, {
                            label: 'Con Respuesta Aprobada J',
                            yAxisID: 'right',
                            data: dataGraph.aprobada_jefe,
                            backgroundColor: "#753ede",
                            borderColor: "#753ede",
                            borderWidth: 1,
                        }, {
                            label: 'Con Respuesta Aprobada D',
                            yAxisID: 'right',
                            data: dataGraph.aprobada_dtr,
                            backgroundColor: "#de933e",
                            borderColor: "#de933e",
                            borderWidth: 1,
                        }, {
                            label: 'Rechazada',
                            yAxisID: 'left',
                            data: dataGraph.quejarechaza,
                            type: 'line',
                            backgroundColor: "#fff",
                            borderColor: "#007bff",
                            borderWidth: 3,
                        }, {
                            label: 'Redirigida',
                            yAxisID: 'left',
                            data: dataGraph.quejaredirige,
                            type: 'line',
                            backgroundColor: "#fff",
                            borderColor: "#28a745",
                            borderWidth: 3,
                        }, {
                            label: 'Notificada',
                            yAxisID: 'left',
                            data: dataGraph.quejanotificada,
                            type: 'line',
                            backgroundColor: "#fff",
                            borderColor: "#ffc107",
                            borderWidth: 3,
                        }, {
                            label: 'Menos de 30 Dias',
                            yAxisID: 'left',
                            data: dataGraph.menos_30d,
                            type: 'line',
                            backgroundColor: "#fff",
                            borderColor: "#dc3545",
                            borderWidth: 3,
                        }, {
                            label: 'Entre 30 y 60 Dias',
                            yAxisID: 'left',
                            data: dataGraph.between_30d_60d,
                            type: 'line',
                            backgroundColor: "#fff",
                            borderColor: "#f07932",
                            borderWidth: 3,
                        }, {
                            label: 'Entre 60 y 90 Dias',
                            yAxisID: 'left',
                            data: dataGraph.between_60d_90d,
                            type: 'line',
                            backgroundColor: "#fff",
                            borderColor: "#df0202",
                            borderWidth: 3,
                        },{
                            label: 'Más de 90 Dias',
                            yAxisID: 'left',
                            data: dataGraph.older_90d,
                            type: 'line',
                            backgroundColor: "#fff",
                            borderColor: "#753ede",
                            borderWidth: 3,
                        }]
                    },
                });
            });
        }
	}

    return {
        init: function () {
            _initQuejas();
        },
        initForm: function () {
            queja_form = $("#queja_form");
            _initQuejaForm();
        },
        initAsigneTech: function () {
            asigne_form = $("#form_asig_tecnico");
            _initQuejaAsignaForm();
        },
        initResponse: function () {
            response_form = $("#response_form");
            _initResponse();
            _initResponseForm();
        },
        initAprueba: function () {
            _initApruebaForm();
        },
        initStats: function (translations = null, dataGraph = null) {
            _initStats(translations, dataGraph);
        },
    };
}();

jQuery(document).ready(function() {
    DPVQuejas.init();
});

var setDamnificado = function (response) {
	let modal = $("#popup");
	let damn_selectize = $("#id_queja-damnificado");
	let current_value = response;
	let url = json_damn_url || "/quejas/damnificados/json";
	$.ajax({
		url: url,
		success: function (response) {
			damn_selectize[0].selectize.clear();
			damn_selectize[0].selectize.clearOptions();
			damn_selectize[0].selectize.load(function (callback) {
				callback(response);
				damn_selectize[0].selectize.setValue(current_value.id);
			});
			modal.modal('hide');
		}
	});
}

var setProcedencia = function (response) {
	let modal = $("#popup");
	let procedence_selectize = $("#id_queja-procedencia");
	let current_value = response;
	let url = json_proc_url || "/nomenclador/procedencia/json";
	$.ajax({
		url: url,
		success: function (response) {
		    console.log("success json");
			procedence_selectize[0].selectize.clear();
			procedence_selectize[0].selectize.clearOptions();
			procedence_selectize[0].selectize.load(function (callback) {
		        console.log("success loaded");
				callback(response);
			    procedence_selectize[0].selectize.setValue(current_value.id);
			});
			modal.modal('hide');
		}
	});
}

var setCalle = function (response) {
	let modal = $("#popup");
	let id_select_element = $("#selected[type='hidden']").val();
	let mun_select = $(':not(#form_calle) select[id$=municipio]');
	mun_select[0].selectize.setValue(mun_select[0].selectize.getValue());
	if (response && response.id) {
		$("#"+id_select_element)[0].selectize.on('load', function() {
			$("#"+id_select_element)[0].selectize.setValue(response.id);
		});
	}
	modal.modal('hide');
}
