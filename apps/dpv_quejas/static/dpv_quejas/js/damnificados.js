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

var DPVDAmnificado = function () {
    let damnificado_form;
    let validator_form;
    let ajax_request = false;
    let ajax_callback = null;
    
    let _init = function (){};
    
    let _initForm = function () {
        //Declarations and Events
        let $tipo_damn = $("#id_tipo_contenido").selectize({
            create: false,
            placeholder: "Selecione el tipo de damnificado",
            allowEmptyOption: false,
            onChange: function(value) {
                _toggleFormDamnificados(value);
            }
        });
        let $empresas = $("#id_empresas").selectize({
            create: false,
            placeholder: "Selecione una entidad",
            allowEmptyOption: false,
        });
        let $personas = $("#id_personas").selectize({
            create: false,
            placeholder: "Selecione una persona",
            allowEmptyOption: false,
        });
        var $pj_municipio = $("#id_pj-municipio").selectize({
            create: false,
            placeholder: "Selecione un municipio",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $.ajax({
                    url: '/nomenclador/consejopopular/filter/' + value,
                    success: function(results) {
                        let current_value = $pj_cpopular[0].selectize.getValue();
                        let exist = false;
                        for (let i = 0; i < results.length; i++)
                            if (results[i].id == current_value) {
                                exist = true;
                            }
                        if (!exist)
                        $pj_cpopular[0].selectize.clear();
                        $pj_cpopular[0].selectize.clearOptions();
                        $pj_cpopular[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
                $.ajax({
                    url: '/nomenclador/calle/filter/' + value,
                    success: function(results) {
                        let current_value1 = $pj_direccion_calle[0].selectize.getValue();
                        let current_value2 = $pj_direccion_entrecalle1[0].selectize.getValue();
                        let current_value3 = $pj_direccion_entrecalle2[0].selectize.getValue();
                        let exist1, exist2, exist3 = false;
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
                        $pj_direccion_calle[0].selectize.clear();
                        $pj_direccion_calle[0].selectize.clearOptions();
                        $pj_direccion_calle[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist2)
                            $pj_direccion_entrecalle1[0].selectize.clear();
                        $pj_direccion_entrecalle1[0].selectize.clearOptions();
                        $pj_direccion_entrecalle1[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist3)
                            $pj_direccion_entrecalle2[0].selectize.clear();
                        $pj_direccion_entrecalle2[0].selectize.clearOptions();
                        $pj_direccion_entrecalle2[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
            },
        });
        var $pj_cpopular = $("#id_pj-cpopular").selectize({
            placeholder: "Selecione un Consejo Popular",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: false,
            create: false,
        });
        var $pj_direccion_calle = $("#id_pj-direccion_calle").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pj_direccion_entrecalle2 = $("#id_pj-direccion_entrecalle2").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pj_direccion_entrecalle1 = $("#id_pj-direccion_entrecalle1").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pn_genero = $("#id_pn-genero").selectize({
            create: false,
            placeholder: "Selecione un género",
            allowEmptyOption: false,
        });
        var $pn_municipio = $("#id_pn-municipio").selectize({
            create: false,
            placeholder: "Selecione un municipio",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $.ajax({
                    url: '/nomenclador/consejopopular/filter/' + value,
                    success: function(results) {
                        let current_value = $pn_cpopular[0].selectize.getValue();
                        let exist = false;
                        for (let i = 0; i < results.length; i++)
                            if (results[i].id == current_value) {
                                exist = true;
                            }
                        if (!exist)
                        $pn_cpopular[0].selectize.clear();
                        $pn_cpopular[0].selectize.clearOptions();
                        $pn_cpopular[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
                $.ajax({
                    url: '/nomenclador/calle/filter/' + value,
                    success: function(results) {
                        let current_value1 = $pn_direccion_calle[0].selectize.getValue();
                        let current_value2 = $pn_direccion_entrecalle1[0].selectize.getValue();
                        let current_value3 = $pn_direccion_entrecalle2[0].selectize.getValue();
                        let exist1, exist2, exist3 = false;
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
                            $pn_direccion_calle[0].selectize.clear();
                        $pn_direccion_calle[0].selectize.clearOptions();
                        $pn_direccion_calle[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist2)
                            $pn_direccion_entrecalle1[0].selectize.clear();
                        $pn_direccion_entrecalle1[0].selectize.clearOptions();
                        $pn_direccion_entrecalle1[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist3)
                            $pn_direccion_entrecalle2[0].selectize.clear();
                        $pn_direccion_entrecalle2[0].selectize.clearOptions();
                        $pn_direccion_entrecalle2[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
            },
        });
        var $pn_cpopular = $("#id_pn-cpopular").selectize({
            placeholder: "Selecione un consejo popular",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pn_direccion_calle = $("#id_pn-direccion_calle").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pn_direccion_entrecalle1 = $("#id_pn-direccion_entrecalle1").selectize({
            placeholder: "Selecione un ",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pn_direccion_entrecalle2 = $("#id_pn-direccion_entrecalle2").selectize({
            placeholder: "Selecione una ",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });

        $(".add-item").on("click", function () {
           let parent = $(this).parents(".procedent");
           let catcher = parent[0].id.split("_")[0];
           parent.find("#" + catcher + "-new-form").removeClass("no-show");
           $(this).siblings(".close-form").removeClass("no-show");
           $(this).addClass("no-show");
           $(this).siblings(".col-12.col-md-8").find(".selectized")[0].selectize.clear();
           $(this).siblings(".col-12.col-md-8").find(".selectized")[0].selectize.disable();
        });
        $(".close-form").on("click", function () {
           let parent = $(this).parents(".procedent");
           let catcher = parent[0].id.split("_")[0];
           parent.find("#" + catcher + "-new-form").addClass("no-show");
           $(this).siblings(".add-item").removeClass("no-show");
           $(this).addClass("no-show");
           $(this).siblings(".col-12.col-md-8").find(".selectized")[0].selectize.enable();
        });

        //Functions declarations
        //This function show or hide the forms of damnificados depends of param value
        let _toggleFormDamnificados =  function (value) {
            if (value === "37") {
                _hideForms();
                _showEmpresaForm();
            } else if (value === "38") {
                _hideForms();
                _showPersonaForm();
            } else {
                _hideForms();
            }
        }
        //This function hide all formularies
        let _hideForms = function () {
            $("#persona_block,#empresa_block").addClass("no-show");
        }
        //This function show persona formulary and reset the fields on others
        let _showPersonaForm = function () {
            _resetEmpresaForm();
            $("#persona_block").removeClass("no-show");
        }
        //This function show empresa formulary and reset the fields on others
        let _showEmpresaForm = function () {
            _resetPersonaForm();
            $("#empresa_block").removeClass("no-show");
        }
        //This function reset persona formulary fields
        let _resetPersonaForm = function () {
            $("#persona_block input").val("");
            $("#persona_block select").each(function (e) {
                $(this)[0].selectize.clear();
            });
        }
        //This function reset empresa formulary fields
        let _resetEmpresaForm = function () {
            $("#empresa_block input").val("");
            $("#persona_block select").each(function (e) {
                $(this)[0].selectize.clear();
            });
        }

        //set the conf of jquery-validation
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
                if (element[0].attributes['type'].nodeValue == 'select-one' || element[0].attributes['type'].nodeValue == 'select-multiple')
                    error.insertBefore(element.parent());
                else
                    error.insertBefore(element);
            },
        });
        // set rules and mesages to validate form
        let validator_form = damnificado_form.validate({
			rules: {
				'tipo_contenido': {
				    required: true,
				},
				'pn-ci': {
				    required: true,
				    digits: true,
                    maxlength: 11,
                    minlength: 11,
				},
				'pn-nombre': {
				    required: true,
				    maxlength: 30,
				},
				'pn-apellidos': {
				    required: true,
                    maxlength: 50,
				},
				'pn-genero': {
				    required: true,
				},
				'pn-email_address': {
				    email: true,
				},
				'pn-movil': {
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                    remote: {
                        url: '/persona/natural/verify',
                        type: 'GET',
                    },
                },
				'pn-telefono': {
				    required: true,
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
				},
				'pn-direccion_calle': {
				    required: true,
				},
				'pn-direccion_numero': {
				    required: true,
				},
				'pn-direccion_entrecalle1': {
				    required: true,
				},
				'pn-direccion_entrecalle2': {
				    required: true,
				},
				'pn-municipio': {
				    required: true,
				},
				'pn-cpopular': {
				    required: true,
				},
				'pj-nombre': {
				    required: true,
				    maxlength: 100,
				},
				'pj-sigla': {
				    required: true,
                    maxlength: 10,
				},
				'pj-telefono': {
				    required: true,
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
				},
				'pj-movil': {
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                    remote: {
                        url: '/persona/natural/verify',
                        type: 'GET',
                    },
                },
				'pj-nombre_contacto': {
				    required: true,
                    maxlength: 200,
				},
				'pj-email_address': {
				    email: true,
				},
				'pj-codigo_nit': {
				    required: true,
				},
				'pj-codigo_reuup': {
				    required: true,
				},
				'pj-municipio': {
				    required: true,
				},
				'pj-cpopular': {
				    required: true,
				},
				'pj-direccion_calle': {
				    required: true,
				},
				'pj-direccion_numero': {
				    required: true,
				},
				'pj-direccion_entrecalle1': {
				    required: true,
				},
				'pj-direccion_entrecalle2': {
				    required: true,
				},
			},
			messages:{
				'tipo_contenido': {
				    required: "Tiene que seleccionar un tipo de damnificado" +
                        "",
				},
				'pn-ci': {
				    required: "El CI no puede quedar en blanco.",
				    digits: "El CI solo puede tener dígitos.",
                    maxlength: "El CI no puede tener más de 11 dígitos.",
                    minlength: "El CI no puede tener menos de 11 dígitos.",
				},
				'pn-nombre': {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "El nombre no puede tener más de 30 caracteres.",
				},
				'pn-apellidos': {
				    required: "Los apellidos no pueden quedar en blanco.",
                    maxlength: "Los apellidos no pueden tener más de 50 caracteres.",
				},
				'pn-genero': {
				    required: "Tiene que seleccionar un género.",
				},
				'pn-email_address': {
				    email: "El email debe ser una dirección de correo electrónico válido.",
				},
				'pn-movil': {
                    digits: "El movil solo puede tener dígitos.",
                    maxlength: "El movil no pueden tener más de 8 dígitos.",
                    minlength: "El movil no puede tener menos de 8 dígitos.",
                    remote: "Ya existe otra persona registrada con ese movil",
                },
				'pn-telefono': {
				    required: "El teléfono no puede quedar en blanco.",
                    digits: "El teléfono solo puede tener dígitos.",
                    maxlength: "El teléfono no pueden tener más de 8 dígitos.",
                    minlength: "El teléfono no puede tener menos de 8 dígitos.",
				},
				'pn-direccion_calle': {
				    required: "Tiene que seleccionar una calle.",
				},
				'pn-direccion_numero': {
				    required: "El número no puede quedar en blanco.",
				},
				'pn-direccion_entrecalle1': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'pn-direccion_entrecalle2': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'pn-municipio': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'pn-cpopular': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'pj-nombre': {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "El nombre no puede tener más de 100 caracteres.",
				},
				'pj-sigla': {
				    required: "Las siglas no pueden quedar en blanco.",
                    maxlength: "Las siglas no pueden tener más de 10 caracteres.",
				},
				'pj-telefono': {
				    required: "El teléfono no puede quedar en blanco.",
                    digits: "El teléfono solo puede tener dígitos.",
                    maxlength: "El teléfono no pueden tener más de 8 dígitos.",
                    minlength: "El teléfono no puede tener menos de 8 dígitos.",
				},
				'pj-movil': {
                    digits: "El movil solo puede tener dígitos.",
                    maxlength: "El movil no pueden tener más de 8 dígitos.",
                    minlength: "El movil no puede tener menos de 8 dígitos.",
                },
				'pj-nombre_contacto': {
				    required: "El nombre de contacto no puede quedar en blanco.",
				    maxlength: "El nombre de contacto no puede tener más de 200 caracteres.",
				},
				'pj-email_address': {
				    email: "El email debe ser una dirección de correo electrónico válido.",
				},
				'pj-codigo_nit': {
				    required: "El código NIT no puede quedar en blanco.",
				},
				'pj-codigo_reuup': {
				    required: "El código REEUP no puede quedar en blanco.",
				},
				'pj-municipio': {
				    required:  "Tiene que seleccionar un municipio.",
				},
				'pj-cpopular': {
				    required:  "Tiene que seleccionar un consejo popular.",
				},
				'pj-direccion_calle': {
				    required: "Tiene que seleccionar una calle.",
				},
				'pj-direccion_numero': {
				    required: "El número no puede quedar en blanco.",
				},
				'pj-direccion_entrecalle1': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'pj-direccion_entrecalle2': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
			},
		});

        damnificado_form.on("submit", function (e) {
            if (ajax_request) {
                e.preventDefault();
                damnificado_form.ajaxSubmit({
                    type: "POST",
                    success: function (response) {
                        if (is_callable(ajax_callback))
                            ajax_callback(response);
                    }
                })
            }
        })
    }
    
    return {
        init: function () {
            _init();
        },
        initForm: function () {
            damnificado_form = $('#formodal_damnificado');
            _initForm();
        },
        setAjax: function (is_ajax, callback = null) {
            ajax_request = !!(is_ajax);
            ajax_callback = callback
        }
    }
}();