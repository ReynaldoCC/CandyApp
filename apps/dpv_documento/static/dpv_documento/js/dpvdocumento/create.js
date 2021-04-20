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

var DPVDocumentos = function () {
    var form;
    var form_modal;
    var $pj_procedencia;

    var _initInputs = function (){

        var $pj_municipio = $("#id_municipio").selectize({
            create: false,
            placeholder: "Selecione un municipio",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $("#id_dir_cpopular").parent().parent().attr("style","");
                $("#id_dir_calle").parent().parent().attr("style","");
                $("#id_dir_numero").parent().parent().attr("style","");
                $("#id_dir_entrecalle1").parent().parent().attr("style","");
                $("#id_dir_entrecalle2").parent().parent().attr("style","");
                $pj_cpopular.rules( "add", {
                    required: true,
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $('#id_dir_numero').rules( "add", {
                    required: true,
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $pj_direccion_calle.rules( "add", {
                    required: true,
                    myNotEqualTo: "#id_dir_entrecalle2",
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $pj_direccion_entrecalle1.rules( "add", {
                    required: true,
                    myNotEqualTo: "#id_dir_calle",
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $pj_direccion_entrecalle2.rules( "add", {
                    required: true,
                    myNotEqualTo: "#id_dir_entrecalle1",
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
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
                        if (!exist1) {
                            $pj_direccion_calle[0].selectize.clear();
                            $pj_direccion_calle[0].selectize.clearOptions();
                            $pj_direccion_calle[0].selectize.load(function (callback) {
                                callback(results);
                            });
                        }
                        if (!exist2){
                            $pj_direccion_entrecalle1[0].selectize.clear();
                            $pj_direccion_entrecalle1[0].selectize.clearOptions();
                            $pj_direccion_entrecalle1[0].selectize.load(function (callback) {
                                callback(results);
                            });
                        }
                        if (!exist3){
                            $pj_direccion_entrecalle2[0].selectize.clear();
                            $pj_direccion_entrecalle2[0].selectize.clearOptions();
                            $pj_direccion_entrecalle2[0].selectize.load(function (callback) {
                                callback(results);
                            });
                        }
                    }
                });
            },
        });
        var $pj_cpopular = $("#id_dir_cpopular").selectize({
            placeholder: "Selecione un Consejo Popular",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pj_direccion_calle = $("#id_dir_calle").selectize({
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
        var $pj_direccion_entrecalle1 = $("#id_dir_entrecalle1").selectize({
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
        var $pj_direccion_entrecalle2 = $("#id_dir_entrecalle2").selectize({
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
        var $pj_procedencia = $("#id_procedencia").selectize({
            create: false,
            maxItems: 1,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            placeholder: "Selecione una procedencia",
            onChange: function (value){
                if (!value.length) return;

                $.ajax({
                    url: '/nomenclador/procedencia/valid_procedencia_in_personal/' + value + '/',
                    success: function(results) {
                        var display_direccion = results.display_direccion;
                        var display_lugar = results.display_lugar;
                        if(display_direccion){
                            $("#id_municipio").parent().parent().attr("style", "");
                            $("#id_municipio").rules( "add", {
                                required: true,
                                messages: {
                                    required: "Este campo es requerido.",
                                }
                            });
                        }else{
                            $("#id_municipio").parent().parent().attr("style", "display:none;");
                            $("#id_municipio").rules( "add", {
                                required: false,
                            });
                        }
                        if(display_lugar){
                            $("#id_lugar").parent().parent().attr("style", "");
                            $("#id_lugar").rules( "add", {
                                required: true,
                                messages: {
                                    required: "Este campo es requerido.",
                                }
                            });
                        }else{
                            $("#id_lugar").parent().parent().attr("style", "display:none;");
                            $("#id_lugar").rules( "add", {
                                required: false,
                            });
                        }
                    }
                });

            },
        });
        var $pj_destino = $("#id_destino").selectize({
            placeholder: "Seleccione ...",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pj_clasificacion = $("#id_clasificacion").selectize({
            create: false,
            placeholder: "Seleccione ...",
            allowEmptyOption: false,
            onChange: function(value) {
                $.ajax({
                    url: '/docs/tipos/filter/' + value + '/',
                    success: function(results) {
                        // let display = results.display;
                        // if (display){
                        //     $("#id_respuesta_a").parent().parent().attr("style", "");
                        //     $("#id_respuesta_a").rules( "add", {
                        //         required: true,
                        //         messages: {
                        //             required: "Este campo es requerido.",
                        //         }
                        //     });
                        // }else{
                        //     $("#id_respuesta_a").parent().parent().attr("style", "display:none;");
                        //     $("#id_respuesta_a").rules( "add", {
                        //         required: false,
                        //     });
                        // }

                    }
                });
            },
        });
        var $pj_promovente = $("#id_promovente").selectize({
            placeholder: "Seleccione ...",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pj_respuesta_a = $("#id_respuesta_a").selectize({
            placeholder: "Seleccione ...",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pj_lugar = $("#id_lugar").selectize({
            placeholder: "Seleccione un lugar",
            allowEmptyOption: false,
            create: false,
        });

        $pj_lugar.parent().parent().attr("style", "display:none;");
        $pj_municipio.parent().parent().attr("style", "display:none;");
        $pj_cpopular.parent().parent().attr("style","display:none");
        $pj_direccion_calle.parent().parent().attr("style","display:none");
        $("#id_dir_numero").parent().parent().attr("style","display:none");
        $pj_direccion_entrecalle1.parent().parent().attr("style","display:none");
        $pj_direccion_entrecalle2.parent().parent().attr("style","display:none");
        $pj_respuesta_a.parent().parent().attr("style","display:none");

    };

    var _initValidateForm = function (){

        $.validator.addMethod('myNotEqualTo', function( value, element, param ) {

			var target = $( param );

			if ( this.settings.onfocusout && target.not( ".validate-notEqualTo-blur" ).length ) {
				target.addClass( "validate-notEqualTo-blur" ).on( "blur.validate-notEqualTo", function() {
					$( element ).valid();
				} );
			}
			return value !== target.val();

		}, 'Ese no puede ser el valor de este campo.');

        form.validate({

            errorClass: 'text-danger',

            highlight: function(element) {
                $(element).addClass('is-invalid');
            },

            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },
            // Validate only visible fields
			ignore: ":hidden:not([class~=selectized]),:hidden > .selectized, .selectize-control .selectize-input input",

			errorPlacement: function(error, element) {
                error.insertBefore(element);
            },

            rules: {
                'no_refer': {
                    required: true,
                    maxlength: 20,
                },
                'promovente': {
                    required: true,
                },
                'destino': {
                    required: true,
                },
                'asunto': {
                    required: true,
                    maxlength: 400
                },
                'dir_numero': {
                    required: false,
                    maxlength: 8,
                },
            },
        });

    };

    var _initInputsModal = function () {
        var _clearEmail = function (){
            $("#id_email-email").val("");
        };
        var _clearEmpresa = function () {
            $('#id_empresa-nombre').val("");
            $('#id_empresa-sigla').val("");
            $('#id_empresa-telefono').val("");
            $('#id_empresa-movil').val("");
            $('#id_empresa-nombre_contacto').val("");
            $('#id_empresa-email_address').val("");
            $('#id_empresa-codigo_nit').val("");
            $('#id_empresa-codigo_reuup').val("");
            $emp_municipio[0].selectize.clear();
            $emp_cpopular[0].selectize.clear();
            $emp_direccion_calle[0].selectize.clear();
            $('#id_empresa-direccion_numero').val("");
            $emp_direccion_entrecalle1[0].selectize.clear();
            $emp_direccion_entrecalle2[0].selectize.clear();
            $("#id_empresa-cpopular").parent().parent().attr("style","display:none");
            $("#id_empresa-direccion_calle").parent().parent().attr("style","display:none");
            $("#id_empresa-direccion_numero").parent().parent().attr("style","display:none");
            $("#id_empresa-direccion_entrecalle1").parent().parent().attr("style","display:none");
            $("#id_empresa-direccion_entrecalle2").parent().parent().attr("style","display:none");
        };
        var _clearGobierno = function (){
            $("#id_gob-nombre").val("");
        };
        var _clearOrganizacion = function (){
            $("#id_organiza-nombre").val("");
        };
        var _clearPersonal = function (){
            $("#id_person_procedence-ci").val("");
            $("#id_person_procedence-nombre").val("");
            $("#id_person_procedence-apellidos").val("");
            $per_genero[0].selectize.clear();
            $("#id_person_procedence-email_address").val("");
            $("#id_person_procedence-movil").val("");
            $("#id_person_procedence-telefono").val("");
            $per_municipio[0].selectize.clear();
            $per_cpopular[0].selectize.clear();
            $per_direccion_calle[0].selectize.clear();
            $("#id_person_procedence-direccion_numero").val("");
            $per_direccion_entrecalle1[0].selectize.clear();
            $per_direccion_entrecalle2[0].selectize.clear();
            $("#id_person_procedence-cpopular").parent().parent().attr("style","display:none");
            $("#id_person_procedence-direccion_calle").parent().parent().attr("style","display:none");
            $("#id_person_procedence-direccion_numero").parent().parent().attr("style","display:none");
            $("#id_person_procedence-direccion_entrecalle1").parent().parent().attr("style","display:none");
            $("#id_person_procedence-direccion_entrecalle2").parent().parent().attr("style","display:none");
        };
        var _clearPrensaEscrita = function (){
            $("#id_pe-nombre").val("");
            $("#id_pe-siglas").val("");
        };
        var _clearTelefono = function (){
            $("#id_telefono-numero").val("");
        };
        var _clearAllInputs = function (){
            _clearEmpresa();
            _clearEmail();
            _clearGobierno();
            _clearOrganizacion();
            _clearPersonal();
            _clearPrensaEscrita();
            _clearTelefono();
        };
        // PROCEDENCIA
        let $proc_tipo = $("#id_procedencia-tipo").selectize({
            create: false,
            placeholder: "Selecione un tipo de procedencia",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $('#id_procedencia-tipo').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                _clearAllInputs();
                switch (value) {
                    case '1':
                        $('#anon_block').removeClass('no-show');
                        break;
                    case '2':
                        $('#prensa_block').removeClass('no-show');
                        $('#id_pe-nombre').rules( "add", {
                            required: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        $('#id_pe-siglas').rules( "add", {
                            required: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        break;
                    case '3':
                        $('#persona_block').removeClass('no-show');
                        $('#id_person_procedence-ci').rules( "add", {
                            required: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        $('#id_person_procedence-nombre').rules( "add", {
                            required: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        $('#id_person_procedence-apellidos').rules( "add", {
                            required: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        break;
                    case '4':
                        $('#telefono_block').removeClass('no-show');
                        $('#id_telefono-numero').rules( "add", {
                            required: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        break;
                    case '5':
                        $('#correo_block').removeClass('no-show');
                        $('#id_email-email').rules( "add", {
                            required: true,
                            email: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        break;
                    case '6':
                        $('#empresa_block').removeClass('no-show');
                        $('#id_empresa-nombre').rules( "add", {
                            required: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        $('#id_empresa-codigo_nit').rules( "add", {
                            required: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        $('#id_empresa-codigo_reuup').rules( "add", {
                            required: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        break;
                    case '7':
                        $('#gob_block').removeClass('no-show');
                        $('#id_gob-nombre').rules( "add", {
                            required: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        break;
                    case '8':
                        $('#org_block').removeClass('no-show');
                        $('#id_organiza-nombre').rules( "add", {
                            required: true,
                            messages: {
                                required: "Este campo es requerido.",
                            }
                        });
                        break;
                }
            },
        });
        // EMPRESA
        let $emp_municipio = $("#id_empresa-municipio").selectize({
            create: false,
            placeholder: "Selecione un municipio",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $("#id_empresa-cpopular").parent().parent().attr("style","");
                $("#id_empresa-direccion_calle").parent().parent().attr("style","");
                $("#id_empresa-direccion_numero").parent().parent().attr("style","");
                $("#id_empresa-direccion_entrecalle1").parent().parent().attr("style","");
                $("#id_empresa-direccion_entrecalle2").parent().parent().attr("style","");
                $emp_cpopular.rules( "add", {
                    required: true,
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $('#id_empresa-direccion_numero').rules( "add", {
                    required: true,
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $emp_direccion_calle.rules( "add", {
                    required: true,
                    myNotEqualTo: "#id_dir_entrecalle2",
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $emp_direccion_entrecalle1.rules( "add", {
                    required: true,
                    myNotEqualTo: "#id_dir_calle",
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $emp_direccion_entrecalle2.rules( "add", {
                    required: true,
                    myNotEqualTo: "#id_dir_entrecalle1",
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $.ajax({
                    url: '/nomenclador/consejopopular/filter/' + value,
                    success: function(results) {
                        let current_value = $emp_cpopular[0].selectize.getValue();
                        let exist = false;
                        for (let i = 0; i < results.length; i++)
                            if (results[i].id == current_value) {
                                exist = true;
                            }
                        if (!exist)
                        $emp_cpopular[0].selectize.clear();
                        $emp_cpopular[0].selectize.clearOptions();
                        $emp_cpopular[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
                $.ajax({
                    url: '/nomenclador/calle/filter/' + value,
                    success: function(results) {
                        let current_value1 = $emp_direccion_calle[0].selectize.getValue();
                        let current_value2 = $emp_direccion_entrecalle1[0].selectize.getValue();
                        let current_value3 = $emp_direccion_entrecalle2[0].selectize.getValue();
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
                        $emp_direccion_calle[0].selectize.clear();
                        $emp_direccion_calle[0].selectize.clearOptions();
                        $emp_direccion_calle[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist2)
                        $emp_direccion_entrecalle1[0].selectize.clear();
                        $emp_direccion_entrecalle1[0].selectize.clearOptions();
                        $emp_direccion_entrecalle1[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist3)
                        $emp_direccion_entrecalle2[0].selectize.clear();
                        $emp_direccion_entrecalle2[0].selectize.clearOptions();
                        $emp_direccion_entrecalle2[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
            },
        });
        let $emp_cpopular = $("#id_empresa-cpopular").selectize({
            placeholder: "Selecione un Consejo Popular",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        let $emp_direccion_calle = $("#id_empresa-direccion_calle").selectize({
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
        let $emp_direccion_entrecalle1 = $("#id_empresa-direccion_entrecalle1").selectize({
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
        let $emp_direccion_entrecalle2 = $("#id_empresa-direccion_entrecalle2").selectize({
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

        $("#id_empresa-cpopular").parent().parent().attr("style","display:none");
        $("#id_empresa-direccion_calle").parent().parent().attr("style","display:none");
        $("#id_empresa-direccion_numero").parent().parent().attr("style","display:none");
        $("#id_empresa-direccion_entrecalle1").parent().parent().attr("style","display:none");
        $("#id_empresa-direccion_entrecalle2").parent().parent().attr("style","display:none");
        //PERSONA PROCEDENTE
        let $per_genero = $("#id_person_procedence-genero").selectize({
            placeholder: "Selecione un genero",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        let $per_municipio = $("#id_person_procedence-municipio").selectize({
            create: false,
            placeholder: "Selecione un municipio",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $("#id_person_procedence-cpopular").parent().parent().attr("style","");
                $("#id_person_procedence-direccion_calle").parent().parent().attr("style","");
                $("#id_person_procedence-direccion_numero").parent().parent().attr("style","");
                $("#id_person_procedence-direccion_entrecalle1").parent().parent().attr("style","");
                $("#id_person_procedence-direccion_entrecalle2").parent().parent().attr("style","");
                $per_cpopular.rules( "add", {
                    required: true,
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $('#id_person_procedence-direccion_numero').rules( "add", {
                    required: true,
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $per_direccion_calle.rules( "add", {
                    required: true,
                    myNotEqualTo: "#id_dir_entrecalle2",
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $per_direccion_entrecalle1.rules( "add", {
                    required: true,
                    myNotEqualTo: "#id_dir_calle",
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
                $per_direccion_entrecalle2.rules( "add", {
                    required: true,
                    myNotEqualTo: "#id_dir_entrecalle1",
                    messages: {
                        required: "Este campo es requerido.",
                    }
                });
            },
        });
        let $per_cpopular = $("#id_person_procedence-cpopular").selectize({
            placeholder: "Selecione un Consejo Popular",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        let $per_direccion_calle = $("#id_person_procedence-direccion_calle").selectize({
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
        let $per_direccion_entrecalle1 = $("#id_person_procedence-direccion_entrecalle1").selectize({
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
        let $per_direccion_entrecalle2 = $("#id_person_procedence-direccion_entrecalle2").selectize({
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

        $("#id_person_procedence-cpopular").parent().parent().attr("style","display:none");
        $("#id_person_procedence-direccion_calle").parent().parent().attr("style","display:none");
        $("#id_person_procedence-direccion_numero").parent().parent().attr("style","display:none");
        $("#id_person_procedence-direccion_entrecalle1").parent().parent().attr("style","display:none");
        $("#id_person_procedence-direccion_entrecalle2").parent().parent().attr("style","display:none");
    };

    var _initValidateModalForm = function (){

        form_modal.validate({

            errorClass: 'text-danger',

            highlight: function(element) {
                $(element).addClass('is-invalid');
            },

            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },

            ignore: ":hidden:not([class~=selectized]),:hidden > .selectized, .selectize-control .selectize-input input",

            errorPlacement: function(error, element) {
                error.insertBefore(element);
            },

            rules: {
                'procedencia-tipo': {
                    required: true
                }
            },

			submitHandler: function (form) {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                var csrftoken = getCookie('csrftoken');

                function csrfSafeMethod(method) {
                    // these HTTP methods do not require CSRF protection
                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                }
                function sameOrigin(url) {
                    // test that a given url is a same-origin URL
                    // url could be relative or scheme relative or absolute
                    var host = document.location.host; // host + port
                    var protocol = document.location.protocol;
                    var sr_origin = '//' + host;
                    var origin = protocol + sr_origin;
                    // Allow absolute or scheme relative URLs to same origin
                    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                        // or any other URL that isn't scheme relative or absolute i.e relative.
                        !(/^(\/\/|http:|https:).*/.test(url));
                }

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                            // Send the token to same-origin, relative URLs only.
                            // Send the token only if the method warrants CSRF protection
                            // Using the CSRFToken value acquired earlier
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });

                let form_data = new FormData($("#formodal_procedencia")[0]);

                $.ajax({
                    type: 'POST',
                    url: '/docs/procedencia/add/',
                    data: form_data,
                    contentType: false,
                    processData: false,
                    success: function (data){
                        $('#close_md').click();
                        var control = $pj_procedencia[0].selectize;
                        control.addOption({value:data.id,text:data.nombre});
                        control.addItem(data.id);
                    },
                });
			},

        });

    };

    return {

        init: function () {
            form = $('#document-form');

            _initInputs();

            _initValidateForm();

        },

        initModal: function () {
            form_modal = $('#formodal_procedencia');

            _initInputsModal();

            _initValidateModalForm();

        },

    };

} ();

jQuery(document).ready(function() {
    DPVDocumentos.init();
});

var setProcedencia = function (response) {
	let modal = $("#popup");
	let procedence_selectize = $("#id_procedencia");
	let current_value = response;
	let url = json_proc_url || "/nomenclador/procedencia/json";
	$.ajax({
		url: url,
		success: function (response) {
			procedence_selectize[0].selectize.clear();
			procedence_selectize[0].selectize.clearOptions();
			procedence_selectize[0].selectize.load(function (callback) {
				callback(response);
			    procedence_selectize[0].selectize.setValue(current_value.id);
			});
			modal.modal('hide');
		}
	});
}