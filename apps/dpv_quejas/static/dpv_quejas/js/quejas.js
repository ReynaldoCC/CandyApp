'use strict'

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

    var _makeAlert = function(type, text) {

    };

    var _initQuejas = function () {

    };
    var _initTabWizard = function () {
        var prev_button = $('#previous_tab');
        var next_button = $('#next_tab');
        var tab_list = $('ul#myTab li.nav-item');
        var first_tab = $('ul#myTab li.nav-item:first');
        var last_tab = $('ul#myTab li.nav-item:last');
        var content_list = $('div#myTabContent.tab-content div.tab-pane');

        $('#procedencia_tab').on('click', function (e) {
            _disableOrEnablePNButton($(this));
        });
        $('#aquejado_tab').on('click', function (e) {
            let ok_tab1 = _verifyProcedence();
            if (ok_tab1.error) {
                e.preventDefault();
                _makeAlert('error', ok_tab1.error_list)
            };
            _disableOrEnablePNButton($(this));

        });
        $('#queja_tab').on('click', function (e) {
            let ok_tab1 = _verifyProcedence();
            let ok_tab2 = _verifyDammed();
            if (!ok_tab1 || !ok_tab2) {
                e.preventDefault();

            };
            _disableOrEnablePNButton($(this));
        });
        $('#sumario_tab').on('click', function (e) {
            let ok_tab1 = _verifyProcedence();
            let ok_tab2 = _verifyDammed();
            let ok_tab3 = _verifyComplaint();
            if (!ok_tab1 || !ok_tab2 || !ok_tab3) {
                e.preventDefault();

            };
            _disableOrEnablePNButton($(this));
        });
        $('#previous_tab').on('click', function (e) {
            let current_tab = $('ul#myTab li.nav-item.active');
            current_tab.find('a.nav-link').removeClass('active show');
            let previous_tab = $('ul#myTab li.nav-item.active').prev("ul#myTab li.nav-item");
            //console.log(previous_tab.find('a.nav-link')[0].hash);
            //let conten_id = previous_tab.find('a.nav-link')[0].attributes['aria-controls'].value;
            let conten_selector = previous_tab.find('a.nav-link')[0].hash;
            previous_tab.find('a.nav-link').click();
            previous_tab.find('a.nav-link').addClass('active show');
            content_list.removeClass('active show in');
            $(conten_selector).addClass('active show in');
            if (previous_tab[0] == first_tab[0]) {
                prev_button.addClass('disabled');
            }
            if (next_button.hasClass('disabled')) {
                next_button.removeClass('disabled');
            }
        });
        $('#next_tab').on('click', function (e) {
            let current_tab = $('ul#myTab.nav.nav-tabs.row li.nav-item.active');
            current_tab.find('a.nav-link').removeClass('active show');
//            console.log('current', current_tab);
            let next_tab = $('ul#myTab li.nav-item.active').next("ul#myTab li.nav-item");
            next_tab.find('a.nav-link').click();
            next_tab.find('a.nav-link').addClass('active show');
            let conten_selector = next_tab.find('a.nav-link')[0].hash;
            content_list.removeClass('active show in');
            $(conten_selector).addClass('active show in');
            if (next_tab[0] == last_tab[0]) {
                next_button.addClass('disabled');
            }
            if (prev_button.hasClass('disabled')) {
                prev_button.removeClass('disabled');
            }
            //console.log(next_button);
        });
        $("#id_tipo_procedencia").on('change', function (e) {
            if ($('#id_tipo_procedencia').val() == '') {
                $('#id_tipo_procedencia').parent('.row.form-group.col-lg-6').addClass('col-lg-12').removeClass('col-lg-6');
                $('.procedent').addClass('no-show');
            } else if ($('#id_tipo_procedencia').val() == '1') {
                $('#id_tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#anon_block').removeClass('no-show');
            } else if ($('#id_tipo_procedencia').val() == '2') {
                $('#id_tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#prensa_block').removeClass('no-show');
            } else if ($('#id_tipo_procedencia').val() == '3') {
                $('#id_tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#persona_block').removeClass('no-show');
            } else if ($('#id_tipo_procedencia').val() == '4') {
                $('#id_tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#telefono_block').removeClass('no-show');
            } else if ($('#id_tipo_procedencia').val() == '5') {
                $('#id_tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#correo_block').removeClass('no-show');
            } else if ($('#id_tipo_procedencia').val() == '6') {
                $('#id_tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#empresa_block').removeClass('no-show');
            } else if ($('#id_tipo_procedencia').val() == '7') {
                $('#id_tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#gob_block').removeClass('no-show');
            } else if ($('#id_tipo_procedencia').val() == '8') {
                $('#id_tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#org_block').removeClass('no-show');
            };
        });
        $("#id_damnificado_not_indb").on('change', function (e) {
            if (this.checked) {
                $("#is_indb").addClass('no-show')
                $("#not_indb").removeClass('no-show');
                $("#id_persona_natural").val('');
            } else {
                $("#is_indb").removeClass('no-show');
                $("#not_indb").addClass('no-show')
                //console.log(queja_form);
            }
        });
        $("#same_address").on('change', function (e) {
            if (this.checked) {
                $("#id_dir_calle").val($("#id_direccion_calle").val());
                $("#id_dir_num").val($("#id_direccion_calle").val());
                $("#id_dir_entrecalle1").val($("#id_direccion_entrecalle1").val());
                $("#id_dir_entrecalle2").val($("#id_direccion_entrecalle2").val());
                $("#id_dir_municipio").val($("#id_municipio").val());
                $("#id_dir_cpopular").val($("#id_cpopular").val());
            } else {
                $("#id_dir_calle").val('');
                $("#id_dir_num").val('');
                $("#id_dir_entrecalle1").val('');
                $("#id_dir_entrecalle2").val('');
                $("#id_dir_municipio").val('');
                $("#id_dir_cpopular").val('');
            }
        });
        $("#")

        var _disableOrEnablePNButton = function (element) {
            //console.log('element', element);
            let element_li;
            if (element[0].nodeName === "DIV") {
                element_li = element;

            } else {
                element_li = element.parent(".nav-item");
            };
            //console.log('elementLi', element_li);
            if (element_li[0] == last_tab[0]) {
                next_button.addClass('disabled');
            } else {
                if (next_button.hasClass('disabled'))
                    next_button.removeClass('disabled');
            };
            if (element_li[0] == first_tab[0]) {
                prev_button.addClass('disabled');
            } else {
                if (prev_button.hasClass('disabled'))
                    prev_button.removeClass('disabled');
            }
        };
        var _verifyProcedence = function() {
            let result = {
                error: false,
                error_list: [],
            };
            if ($('#id_tipo_procedencia').val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar un tipo de procedencia";
                result.error_list.push(error_name);
            };
            if ($('#id_procedencia').val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar una procedencia";
                result.error_list.push(error_name);
            };
            console.log('re',result);
            return result;
        };
        var _verifyDammed = function () {
            let result = {
                error: false,
                error_list: [],
            };
            if ($("#id_persona_natural").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar una persona de la lista";
                result.error_list.push(error_name);
            };
            if ($("#id_nombre").val() === '') {
                result.error = true;
                let error_name = "El Nombre es obligatorio";
                result.error_list.push(error_name);
            };
            if ($("#id_apellidos").val() === '') {
                result.error = true;
                let error_name = "Los Apellidos son abligatorios";
                result.error_list.push(error_name);
            };
            if ($("#id_ci").val() === '') {
                result.error = true;
                let error_name = "El CI es obligatorio";
                result.error_list.push(error_name);
            };
            if ($("#id_genero").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar un género";
                result.error_list.push(error_name);
            };
            if ($("#id_email_address").val() === '' &&  $("#id_movil").val() === '' && $("#id_telefono").val() === '') {
                result.error = true;
                let error_name = "Es obligatorio poner al menos una forma de contacto (Movil, Email, Teléfono)";
                result.error_list.push(error_name);
            };
            if ($("#id_direccion_calle").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar una calle";
                result.error_list.push(error_name);
            };
            if ($("#id_direccion_numero").val() === '') {
                result.error = true;
                let error_name = "El número es obligatorio";
                result.error_list.push(error_name);
            };
            if ($("#id_direccion_entrecalle1").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar una primera entrecalle";
                result.error_list.push(error_name);
            };
            if ($("#id_direccion_entrecalle2").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar una segunda entrecalle";
                result.error_list.push(error_name);
            };
            if ($("#id_cpopular").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar un consejo popular";
                result.error_list.push(error_name);
            };
            if ($("#id_municipio").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar un municipio";
                result.error_list.push(error_name);
            };
            return result;
        };
        var _verifyComplaint = function () {
            let result = {
                error: false,
                error_list: [],
            };
            if ($("#id_dir_calle").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar una calle";
                result.error_list.push(error_name);
            };
            if ($("#id_dir_num").val() === '') {
                result.error = true;
                let error_name = "El número es obligatorio";
                result.error_list.push(error_name);
            };
            if ($("#id_dir_entrecalle1").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar una primera entrecalle";
                result.error_list.push(error_name);
            };
            if ($("#id_dir_entrecalle2").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar una segunda entrecalle";
                result.error_list.push(error_name);
            };
            if ($("#id_dir_municipio").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar un municipio";
                result.error_list.push(error_name);
            };
            if ($("#id_dir_cpopular").val() === '') {
                result.error = true;
                let error_name = "Debe seleccionar un consejo popular";
                result.error_list.push(error_name);
            };
            if ($("#id_referencia").val() === '') {
                result.error = true;
                let error_name = "La referencia es obligatoria";
                result.error_list.push(error_name);
            };
            if ($("#id_asunto").val() === '') {
                result.error = true;
                let error_name = "El Asunto es obligatorio";
                result.error_list.push(error_name);
            };
            if ($("#id_texto").val() === '') {
                result.error = true;
                let error_name = "El Cuerpo de la queja es obligatorio";
                result.error_list.push(error_name);
            };
            return result;
        };

    };
    var _initQuejaForm = function () {
        $.validator.setDefaults({
            errorClass: 'kt-font-danger',
            highlight: function(element) {
                $(element).addClass('is-invalid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },
            // Validate only visible fields
			ignore: ":hidden",
            // Error Placement
            errorPlacement: function(error, element) {
                if (element[0].name == 'blood_pressure_low') {
                    error.insertAfter(element.parent().parent());
                } else {
                    error.insertBefore(element.parent().parent());
                }
            },
            invalidHandler: function(event, validator) {
				KTUtil.scrollTop();

				swal.fire({
					"title": "Error",
					"text": "Existen algunos campos con errores en su formulario. Por favor corríjalos para guardar.",
					"type": "error",
					"buttonStyling": false,
					"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
				});
			},
        });
        queja_form.validate({
			rules: {
				tipo_procedencia: {
				    required: true,
				},
				procedencia: {
				},
				persona_natural: {
				},
				nombre: {
				    required: true,
                    maxlength: 30,
				},
				apellidos: {
				    required: true,
                    maxlength: 50,
				},
				ci: {
				    required: true,
				    digits: true,
                    maxlength: 11,
                    minlength: 11,
				},
				genero: {
				    required: true,
				},
				email_address: {
				    email: true,
				},
                movil: {
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                },
                telefono: {
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                },
				direccion_calle: {
				    required: true,
				},
				direccion_numero: {
				    required: true,
				},
				direccion_entrecalle1: {
				    required: true,
                },
                direccion_entrecalle2: {
				    required: true,
                },
                cpopular: {
				    required: true,
                },
                municipio: {
				    required: true,
                },
                dir_calle: {
				    required: true,
                },
                dir_num: {
				    required: true,
                },
                dir_entrecalle1: {
				    required: true,
                },
                dir_entrecalle2: {
				    required: true,
                },
                dir_municipio: {
				    required: true,
                },
                dir_cpopular: {
				    required: true,
                },
                referencia: {
				    required: true,
                },
                asunto: {
				    required: true,
                },
                texto: {
				    required: true,
                    maxlength: 20,
                    minlength: 3000,
                },
			},
			messages:{
				short_name: {
				    required: "El nombre corto no puede quedar en blanco",
                    maxlength: "La temperatura no puede tener más de 100 caracteres",
				},
				nursing_service: {
				    required: "Por favor debe seleccionar al menos un servicio de la lista.",
				},
				bach_flower: {
				    required: "Por favor debe seleccionar un elemento de la lista.",
				},
				blood_pressure_high: {
				    required: "La presion arterial no puede quedar en blanco",
				    digits: "La presión arterial alta debe contener solo dígitos",
				    min: "La presión arterial no puede ser negativa",
                    greaterThan: "La presion arterial alta no puede ser menor que la baja \n",
				},
				blood_pressure_low: {
				    required: "La presion arterial no puede quedar en blanco",
				    min: "La presión arterial no puede ser negativa",
                    lessThan: "La presion arterial baja no puede ser mayor que la alta",
				    digits: "La presión arterial baja debe contener solo dígitos",
				},
				heart_rate: {
				    required: "La frecuencia cardiaca no puede quedar en blanco",
				    min: "La frecuencia cardiaca no puede ser negativa",
				    digits: "La frecuencia cardiaca debe contener solo dígitos",
				},
				respiratory_rate: {
				    required: "La frecuencia respiratoria no puede quedar en blanco",
				    min: "La frecuencia respiratoria no puede ser negativa",
				    digits: "La frecuencia respiratoria debe contener solo dígitos",
				},
				temperature: {
				    required: "La temperatura no puede quedar en blanco",
				    min: "La temperatura no puede ser negativa",
				    number: "La temperatura debe ser un número válido",
                    maxlength: "La temperatura no puede tener más de 4 caracteres",
                    maxdecimalplaces: "Por favor, la temperatura debe tener a lo sumo 1 lugar decimal",
				},
				current_size: {
				    required: "El tamaño  no puede quedar en blanco",
				    min: "El tamaño no puede ser negativo",
                    maxlength: "La temperatura no puede tener más de 6 caracteres",
                    maxdecimalplaces: "Por favor, la temperatura debe tener a lo sumo 2 lugares decimales",
				    number: "El tamaño debe ser un número válido",
				},
				current_weight: {
				    required: "El peso no puede quedar en blanco",
				    min: "El peso no puede ser negativo",
                    maxlength: "La temperatura no puede tener más de 6 caracteres",
                    maxdecimalplaces: "Por favor, la temperatura debe tener a lo sumo 2 lugares decimales",
				    number: "El peso debe ser un número válido",
				},
				observations_results: {
                    maxlength: "Las observaciones no pueden tener más de 600 caracteres",
                },
			},
		});
		queja_form[0].reset();
    };
    return {
        init: function () {

            _initQuejas();
        },
        initForm: function () {
            queja_form = $("#queja_form");
            _initTabWizard();
        },
    };
}();

jQuery(document).ready(function() {

    DPVQuejas.init();
	DPVQuejas.initForm();
});