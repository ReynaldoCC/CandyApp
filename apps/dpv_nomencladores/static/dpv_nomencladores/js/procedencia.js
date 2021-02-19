'use strict';

function abrir_modal(url, id=null)
{
    $('#popup').load(url, function()
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

var DPVProcedenciaNom =  function () {
    let procedencia_form;
    let validator_form;
    let ajax_request = false;
    let ajax_callback = null;

    const _initProcedenciaPane = function (translations) {
        $('#procedencia-table').DataTable({
            responsive: true,
            order: [ 0, 'desc' ],
            lengthMenu: [20, 35, 50, "All"],
            sScrollX: "100%",
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
    };
    const _initProcedenciaForm =  function () {

        var $tipo_procedencia = $("#id_procedencia-tipo").selectize({
            create: false,
            placeholder: "Selecione una tipo de procedencia",
            allowEmptyOption: false,
        });
        var $pj_municipio = $("#id_empresa-municipio").selectize({
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
        var $pj_cpopular = $("#id_empresa-cpopular").selectize({
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
        var $pj_direccion_calle = $("#id_empresa-direccion_calle").selectize({
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
        var $pj_direccion_entrecalle2 = $("#id_empresa-direccion_entrecalle2").selectize({
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
        var $pj_direccion_entrecalle1 = $("#id_empresa-direccion_entrecalle1").selectize({
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
        var $pn_genero = $("#id_person_procedence-genero").selectize({
            create: false,
            placeholder: "Selecione un género",
            allowEmptyOption: false,
        });
        var $pn_municipio = $("#id_person_procedence-municipio").selectize({
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
        var $pn_cpopular = $("#id_person_procedence-cpopular").selectize({
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
        var $pn_direccion_calle = $("#id_person_procedence-direccion_calle").selectize({
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
        var $pn_direccion_entrecalle1 = $("#id_person_procedence-direccion_entrecalle1").selectize({
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
        var $pn_direccion_entrecalle2 = $("#id_person_procedence-direccion_entrecalle2").selectize({
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
        var $wp_red_social = $("#id_web-red_social").selectize({
            placeholder: "Selecione una red social",
            allowEmptyOption: true,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $list_emails = $("#id_procedencia-emails").selectize({
            placeholder: "Selecione un email",
            allowEmptyOption: true,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $list_empresas = $("#id_procedencia-empresas").selectize({
            placeholder: "Selecione una empresa",
            allowEmptyOption: true,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $list_prensas = $("#id_procedencia-prensas").selectize({
            placeholder: "Selecione una prensa",
            allowEmptyOption: true,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $list_personas = $("#id_procedencia-personas").selectize({
            placeholder: "Selecione una persona",
            allowEmptyOption: true,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $list_phones = $("#id_procedencia-phones").selectize({
            placeholder: "Selecione un teléfono",
            allowEmptyOption: true,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $list_organiz = $("#id_procedencia-organizaciones").selectize({
            placeholder: "Selecione una organización",
            allowEmptyOption: true,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $list_organis = $("#id_procedencia-organismos").selectize({
            placeholder: "Selecione un organismo",
            allowEmptyOption: true,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $list_webs = $("#id_procedencia-webs").selectize({
            placeholder: "Selecione un perfil web",
            allowEmptyOption: true,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });

        $("#id_procedencia-tipo").on('change', function (e) {
            _toggleProcedenciaForms();
        });
        $(".add-item").on("click", function () {
           $(this).siblings(".col-12.col-md-8").find(".selectized")[0].selectize.clear();
           $(this).siblings(".col-12.col-md-8").find(".selectized")[0].selectize.disable();
        });
        $(".close-form").on("click", function () {
           $(this).siblings(".col-12.col-md-8").find(".selectized")[0].selectize.enable();
        });
        $("#prensa_block .add-item").on('click', function () {
            $("#prensa-new-form").removeClass("no-show");
            $("#id_procedencia-prensas").siblings(".selectize-control.form-control").addClass("disabled");
            $(this).siblings('.close-form').removeClass('no-show');
            $(this).addClass('no-show');

        });
        $("#prensa_block .close-form").on('click', function () {
            $("#prensa-new-form").addClass("no-show");
            $("#id_procedencia-prensas").siblings(".selectize-control.form-control").removeClass("disabled");
            $(this).siblings('.add-item').removeClass('no-show');
            $(this).addClass('no-show');
            $("#prensa-new-form").find("input,select").each(function () { $(this).val( this.defaultValue); })
        });
        $("#persona_block .add-item").on('click', function () {
            $("#persona-new-form").removeClass("no-show");
            $("#id_procedencia-personas").siblings(".selectize-control.form-control").addClass("disabled");
            $(this).siblings('.close-form').removeClass('no-show');
            $(this).addClass('no-show');
        });
        $("#persona_block .close-form").on('click', function () {
            $("#persona-new-form").addClass("no-show");
            $("#id_procedencia-personas").siblings(".selectize-control.form-control").removeClass("disabled");
            $(this).siblings('.add-item').removeClass('no-show');
            $(this).addClass('no-show');
            $("#persona-new-form").find("input,select").each(function () { $(this).val( this.defaultValue); })
        });
        $("#telefono_block .add-item").on('click', function () {
            $("#phone-new-form").removeClass("no-show");
            $("#id_procedencia-phones").siblings(".selectize-control.form-control").addClass("disabled");
            $(this).siblings('.close-form').removeClass('no-show');
            $(this).addClass('no-show');
        });
        $("#telefono_block .close-form").on('click', function () {
            $("#phone-new-form").addClass("no-show");
            $("#id_procedencia-phones").siblings(".selectize-control.form-control").removeClass("disabled");
            $(this).siblings('.add-item').removeClass('no-show');
            $(this).addClass('no-show');
            $("#phone-new-form").find("input,select").each(function () {  $(this).val( this.defaultValue); })
        });
        $("#correo_block .add-item").on('click', function () {
            $("#email-new-form").removeClass("no-show");
            $("#id_procedencia-emails").siblings(".selectize-control.form-control").addClass("disabled");
            $(this).siblings('.close-form').removeClass('no-show');
            $(this).addClass('no-show');
        });
        $("#correo_block .close-form").on('click', function () {
            $("#email-new-form").addClass("no-show");
            $("#id_procedencia-emails").siblings(".selectize-control.form-control").removeClass("disabled");
            $(this).siblings('.add-item').removeClass('no-show');
            $(this).addClass('no-show');
            $("#email-new-form").find("input,select").each(function () { $(this).val( this.defaultValue); })
        });
        $("#empresa_block .add-item").on('click', function () {
            $("#empresa-new-form").removeClass("no-show");
            $("#id_procedencia-empresas").siblings(".selectize-control.form-control").addClass("disabled");
            $(this).siblings('.close-form').removeClass('no-show');
            $(this).addClass('no-show');
        });
        $("#empresa_block .close-form").on('click', function () {
            $("#empresa-new-form").addClass("no-show");
            $("#id_procedencia-empresas").siblings(".selectize-control.form-control").removeClass("disabled");
            $(this).siblings('.add-item').removeClass('no-show');
            $(this).addClass('no-show');
            $("#empresa-new-form").find("input,select").each(function () {  $(this).val( this.defaultValue);  })
        });
        $("#orgz_block .add-item").on('click', function () {
            $("#organiz-new-form").removeClass("no-show");
            $("#id_procedencia-organizaciones").siblings(".selectize-control.form-control").addClass("disabled");
            $(this).siblings('.close-form').removeClass('no-show');
            $(this).addClass('no-show');
        });
        $("#orgz_block .close-form").on('click', function () {
            $("#organiz-new-form").addClass("no-show");
            $("#id_procedencia-organizaciones").siblings(".selectize-control.form-control").removeClass("disabled");
            $(this).siblings('.add-item').removeClass('no-show');
            $(this).addClass('no-show');
            $("#organiz-new-form").find("input,select").each(function () { $(this).val( this.defaultValue); })
        });
        $("#org_block .add-item").on('click', function () {
            $("#organis-new-form").removeClass("no-show");
            $("#id_procedencia-organismos").siblings(".selectize-control.form-control").addClass("disabled");
            $(this).siblings('.close-form').removeClass('no-show');
            $(this).addClass('no-show');
        });
        $("#org_block .close-form").on('click', function () {
            $("#organis-new-form").addClass("no-show");
            $("#id_procedencia-organismos").siblings(".selectize-control.form-control").removeClass("disabled");
            $(this).siblings('.add-item').removeClass('no-show');
            $(this).addClass('no-show');
            $("#organis-new-form").find("input,select").each(function () { $(this).val( this.defaultValue); })
        });
        $("#web_block .add-item").on('click', function () {
            $("#web-new-form").removeClass("no-show");
            $("#id_procedencia-webs").siblings(".selectize-control.form-control").addClass("disabled");
            $(this).siblings('.close-form').removeClass('no-show');
            $(this).addClass('no-show');
        });
        $("#web_block .close-form").on('click', function () {
            $("#web-new-form").addClass("no-show");
            $("#id_procedencia-webs").siblings(".selectize-control.form-control").removeClass("disabled");
            $(this).siblings('.add-item').removeClass('no-show');
            $(this).addClass('no-show');
            $("#web-new-form").find("input,select").each(function () { $(this).val( this.defaultValue); })
        });
        $("#id_procedencia-emails,#id_procedencia-empresas,#id_procedencia-organismos,#id_procedencia-organizaciones,#id_procedencia-personas,#id_procedencia-prensas,#id_procedencia-phones,#id_procedencia-webs").on("change", function (e) {
            if ($(this).val()) {
                $(this).parent().siblings('.add-item').addClass('disabled');
            } else {
                $(this).parent().siblings('.add-item').removeClass('disabled');
            }
        });

        $.validator.setDefaults({
            errorClass: 'text-danger',
            highlight: function(element) {
                $(element).addClass('is-invalid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },

			ignore: ":hidden:not([class~=selectized]),:hidden > .selectized, .selectize-control .selectize-input input",

            errorPlacement: function(error, element) {
                if (element[0].hasAttribute('type')) {
                    if (element[0].attributes['type'].nodeValue === 'select-one' || element[0].attributes['type'].nodeValue === 'select-multiple')
                        error.insertBefore(element.parent());
                    else
                        error.insertBefore(element);
                } else
                    error.insertBefore(element);
            },

        });
        $.validator.addMethod("letterswithbasicpuncandspace", function(value, element) {
            return this.optional(element) || /^[a-zA-Z0-9áéíóúÁÉÚÍÓñÑ \-.,()'"\s]+$/i.test(value);
        }, "solo puede tener letras, números, y signos de puntuación básicos");

        procedencia_form.validate({
            rules: {
                'procedencia-tipo': {
                    required: true,
                },
                'organiza-nombre': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 90,
                    remote: {
                        url: '/nomenclador/organizacion/verify',
                        type: 'get',
                    },
                },
                'organiza-siglas': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 15,
                },
                'organiza-email': {
                    required: true,
                    email: true,
                },
                'organiza-telefono': {
                    required: true,
                    digits: true,
                    minlength: 8,
                    maxlength: 8,
                },
                'organiza-nombre_contacto': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 200,
                    minlength: 3,
                },
                'email-email': {
                    required: true,
                    email: true,
                    remote: {
                        url: '/nomenclador/email/verify',
                        type: 'get',
                    },
                },
                'email-nombre_contacto': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 220,
                },
                'empresa-nombre': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 100,
                    remote: {
                        url: '/persona/juridica/verify',
                        type: 'get',
                    },
                },
                'empresa-sigla': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 15,
                },
                'empresa-telefono': {
                    required: true,
                    digits: true,
                    minlength: 8,
                    maxlength: 8,
                },
                'empresa-movil': {
                    required: true,
                    digits: true,
                    minlength: 8,
                    maxlength: 8,
                },
                'empresa-nombre_contacto': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 200,
                },
                'empresa-email_address': {
                    required: true,
                    email: true,
                },
                'empresa-codigo_nit': {
                    required: true,
                    remote: {
                        url: '/persona/juridica/verify',
                        type: 'get',
                    },
                },
                'empresa-codigo_reuup': {
                    required: true,
                    remote: {
                        url: '/persona/juridica/verify',
                        type: 'get',
                    },
                },
                'empresa-municipio': {
                    required: true,
                },
                'empresa-cpopular': {
                    required: true,
                },
                'empresa-direccion_calle': {
                    required: true,
                },
                'empresa-direccion_numero': {
                    required: true,
                },
                'empresa-direccion_entrecalle1': {
                    required: true,
                },
                'empresa-direccion_entrecalle2': {
                    required: true,
                },
                'organism-nombre': {
                    required: true,
                    maxlength: 90,
                    letterswithbasicpuncandspace: true,
                },
                'organism-siglas': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 15,
                },
                'organism-email': {
                    required: true,
                    email: true,
                },
                'organism-telefono': {
                    required: true,
                    digits: true,
                    minlength: 8,
                    maxlength: 8,
                },
                'organism-nombre_contacto': {
                    required: true,
                    maxlength: 200,
                    minlength: 3,
                    letterswithbasicpuncandspace: true,
                },
                'person_procedence-nombre': {
                    required: true,
                    maxlength: 30,
                    letterswithbasicpuncandspace: true,
                },
                'person_procedence-apellidos': {
                    required: true,
                    maxlength: 50,
                    letterswithbasicpuncandspace: true,
                },
                'person_procedence-ci': {
                    required: true,
                    digits: true,
                    maxlength: 11,
                    minlength: 11,
                    remote: {
                        url: '/persona/natural/verify',
                        type: 'get',
                    },
                },
                'person_procedence-email_address': {
                    required: true,
                    email: true,
                },
                'person_procedence-telefono': {
                    digits: true,
                    minlength: 8,
                    maxlength: 8,
                },
                'person_procedence-movil': {
                    digits: true,
                    minlength: 8,
                    maxlength: 8,
                },
                'person_procedence-genero': {
                    required: true,
                },
                'person_procedence-municipio': {
                    required: true,
                },
                'person_procedence-cpopular': {
                    required: true,
                },
                'person_procedence-direccion_calle': {
                    required: true,
                },
                'person_procedence-direccion_numero': {
                    required: true,
                },
                'person_procedence-direccion_entrecalle1': {
                    required: true,
                },
                'person_procedence-direccion_entrecalle2': {
                    required: true,
                },
                'pe-nombre': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 90,
                    remote: {
                        url: '/nomenclador/prensaescrita/verify',
                        type: 'get',
                    },
                },
                'pe-siglas': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 15,
                },
                'pe-nombre_contacto': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 200,
                },
                'pe-email': {
                    required: true,
                    email: true,
                },
                'pe-telefono': {
                    required: true,
                    digits: true,
                    minlength: 8,
                    maxlength: 8,
                },
                'telefono-numero': {
                    required: true,
                    digits: true,
                    minlength: 8,
                    maxlength: 8,
                    remote: {
                        url: '/nomenclador/telefono/verfy',
                        type: 'get',
                        data: {
                            nombre_contacto: $('#id_telefono-nombre_contacto').val(),
                        }
                    },
                },
                'telefono-nombre_contacto': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 220,
                },
                'web-nombre': {
                    required: true,
                    letterswithbasicpuncandspace: true,
                    maxlength: 200,
                    minlength: 3,
                },
                'web-perfil': {
                    required: true,
                    minlength: 3,
                    maxlength: 200,
                    letterswithbasicpuncandspace: true,
                    // remote: {
                    //     url: '/nomenclador/verify_pweb/',
                    //     type: 'get',
                    //     data: {
                    //         red_social: $("#id_web-red_social").val(),
                    //     }
                    // },
                },
                'web-email': {
                    required: true,
                    email: true,
                    // remote: {
                    //     url: '/nomenclador/verify_pweb/',
                    //     type: 'get',
                    //     data: {
                    //         red_social: $wp_red_social.val(),
                    //     }
                    // },
                },
                'web-red_social': {
                    required: true,
                },
            },
            messages: {
                'procedencia-tipo': {
                    required: "Tiene que seleccionar un tipo de procedencia",
                },
                'organiza-nombre': {
                    required: "El nombre de la organización no puede quedar en blanco",
                    letterswithbasicpuncandspace: "El nombre de la organización no puede tener caracteres especiales",
                    maxlength: "El nombre de la organización no puede tener más de 90 caracteres",
                    remote: "Ya existe una organización registrada con ese nombre",
                },
                'organiza-siglas': {
                    required: "Las siglas de la organización no puede quedar en blanco",
                    letterswithbasicpuncandspace: "Las siglas de la organización no puede tener caracteres especiales",
                    maxlength: "Las siglas de la organización no puede tener más de 15 caracteres",
                },
                'organiza-email': {
                    required: "El correo electrónico de la organización no puede quedar en blanco",
                    email: "El correo electrónico de la organización tiene que ser un correo electrónico válido",
                },
                'organiza-telefono': {
                    required: "El teléfono de la organización no puede quedar en blanco",
                    digits: "El teléfono de la organización no puede tener dígitos",
                    minlength: "El teléfono de la organización no puede tener más de 8 dígitos",
                    maxlength: "El teléfono de la organización no puede tener menos de 8 dígitos",
                },
                'organiza-nombre_contacto': {
                    required: "El nombre del contacto de la organización no puede quedar en blanco",
                    letterswithbasicpuncandspace: "El nombre del contacto de la organización no puede tener caracteres especiales",
                    maxlength: "El nombre del contacto de la organización no puede tener más de 200 caracteres",
                    minlength: "El nombre del contacto de la organización no puede tener menos de 3 caracteres",
                },
                'email-email': {
                    required: "El correo electrónico no puede quedar en blanco",
                    email: "El correo electrónico tiene que ser un correo electrónico válido",
                    remote: "Ya existe ese email registrado con el mismo nombre de contacto",
                },
                'email-nombre_contacto': {
                    required: "El nombre del contacto no puede quedar en blanco",
                    letterswithbasicpuncandspace: "El nombre del contacto no puede tener caracteres especiales",
                    maxlength: "El nombre del contacto de la organización no puede tener más de 220 caracteres",
                },
                'empresa-nombre': {
                    required: "El nombre de la empresa no puede quedar en blanco",
                    letterswithbasicpuncandspace: "El nombre de la empresa no puede tener caracteres especiales",
                    maxlength: "El nombre de la empresa no puede tener más de 100 caracteres",
                    remote: "Ya existe una empresa registrada con ese nombre",
                },
                'empresa-sigla': {
                    required: "Las siglas de la empresa no puede quedar en blanco",
                    letterswithbasicpuncandspace: "Las siglas de la empresa no puede tener caracteres especiales",
                    maxlength: "Las siglas de la empresa no puede tener más de 15 caracteres",
                },
                'empresa-telefono': {
                    required: "El teléfono de la empresa no puede quedar en blanco",
                    digits: "El teléfono de la empresa solo puede tener dígitos",
                    minlength: "El teléfono de la empresa no puede tener menos de 8 dígitos",
                    maxlength: "El teléfono de la empresa no puede tener más de 8 dígitos",
                },
                'empresa-movil': {
                    digits: "El móvil solo puede tener dígitos",
                    minlength: "El móvil solo no puede tener menos de 8 dígitos",
                    maxlength: "El móvil solo no puede tener más de 8 dígitos",
                },
                'empresa-nombre_contacto': {
                    required: "El nombre del contacto de la empresa no puede quedar en blanco",
                    letterswithbasicpuncandspace: "El nombre del contacto de la empresa no puede tener caracteres especiales",
                    maxlength: "El nombre del contacto de la empresa no puede tener más de 200 caracteres",
                },
                'empresa-email_address': {
                    required: "El correo electrónico no puede quedar en blanco",
                    email: "El correo electrónico tiene que ser un correo electrónico válido",
                },
                'empresa-codigo_nit': {
                    required: "El código NiT no puede quedar en blanco",
                    remote: "Ya existe una empresa registrada con ese código NiT",
                },
                'empresa-codigo_reuup': {
                    required: "El código Reuup no puede quedar en blanco",
                    remote: "Ya existe una empresa registrada con ese código Reuup",
                },
                'empresa-municipio': {
                    required: "Tiene que seleccionar un municipio",
                },
                'empresa-cpopular': {
                    required: "Tiene que seleccionar un consejo popular",
                },
                'empresa-direccion_calle': {
                    required: "Tiene que seleccionar una calle",
                },
                'empresa-direccion_numero': {
                    required: "El número de la dirección no puede quedar en blanco",
                },
                'empresa-direccion_entrecalle1': {
                    required: "Tiene que seleccionar una calle",
                },
                'empresa-direccion_entrecalle2': {
                    required: "Tiene que seleccionar una calle",
                },
                'organism-nombre': {
                    required: "El nombre del organismo no puede quedar en blanco",
                    maxlength: "El nombre del organismo no puede tener más de 90 caracteres",
                    letterswithbasicpuncandspace: "El nombre del organismo no puede tener caracteres especiales",
                    remote: "Ya existe un organismo registrado con ese nombre",
                },
                'organism-siglas': {
                    required: "Las siglas del organismo no puede quedar en blanco",
                    letterswithbasicpuncandspace: "Las siglas del organismo no puede tener caracteres especiales",
                    maxlength: "Las siglas del organismo no puede tener más de 15 caracteres",
                },
                'organism-email': {
                    required: "El correo electrónico del organismo no puede quedar en blanco",
                    email: "El correo electrónico del organismo tiene que ser un correo electrónico válido",
                },
                'organism-telefono': {
                    required: "El teléfono del organismo no puede quedar en blanco",
                    digits: "El teléfono del organismo solo puede tener dígitos",
                    minlength: "El teléfono del organismo no puede tener más de 8 dígitos",
                    maxlength: "El teléfono del organismo no puede tener menos de 8 dígitos",
                },
                'organism-nombre_contacto': {
                    required: "El nombre de contacto del organismo no puede quedar en blanco",
                    maxlength: "El nombre de contacto del organismo no puede tener más de 200 caracteres",
                    minlength: "El nombre de contacto del organismo no puede tener menos de 3 caracteres",
                    letterswithbasicpuncandspace: "El nombre de contacto del organismo no puede tener caracteres especiales",
                },
                'person_procedence-nombre': {
                    required: "El nombre no puede quedar en blanco",
                    maxlength: "El nombre no puede tener más de 30 caracteres",
                    letterswithbasicpuncandspace: "El nombre no puede tener caracteres especiales",
                },
                'person_procedence-apellidos': {
                    required: "Los apellidos no pueden quedar en blanco",
                    maxlength: "Los apellidos no pueden tener más de 50 caracteres",
                    letterswithbasicpuncandspace: "Los apellidos no pueden tener caracteres especiales",
                },
                'person_procedence-ci': {
                    required: "El CI no puede quedar en blanco",
                    digits: "El CI solo puede tener dígitos",
                    maxlength: "El CI no puede tener más de 11 dígitos",
                    minlength: "El CI no puede tener menos de 11 dígitos",
                    remote: "Ya existe una persona registrada con ese CI",
                },
                'person_procedence-email_address': {
                    required: "El correo electrónico no puede quedar en blanco",
                    email: "El correo electrónico tiene que ser un correo electrónico válido",
                },
                'person_procedence-telefono': {
                    digits: "El teléfono solo puede tener dígitos",
                    minlength: "El teléfono no puede tener menos de 8 dígitos",
                    maxlength: "El teléfono no puede tener más de 8 dígitos",
                },
                'person_procedence-movil': {
                    digits: "El móvil solo puede tener dígitos",
                    minlength: "El móvil no puede tener menos de 8 dígitos",
                    maxlength: "El móvil no puede tener más de 8 dígitos",
                },
                'person_procedence-genero': {
                    required: "Tiene que seleccionar un género",
                },
                'person_procedence-municipio': {
                    required: "Tiene que seleccionar un municipio",
                },
                'person_procedence-cpopular': {
                    required: "Tiene que seleccionar un consejo popular",
                },
                'person_procedence-direccion_calle': {
                    required: "Tiene que seleccionar una calle",
                },
                'person_procedence-direccion_numero': {
                    required: "El número de la dirección no puede quedar en blanco",
                },
                'person_procedence-direccion_entrecalle1': {
                    required: "Tiene que seleccionar una calle",
                },
                'person_procedence-direccion_entrecalle2': {
                    required: "Tiene que seleccionar una calle",
                },
                'pe-nombre': {
                    required: "El nombre de la prensa no puede quedar en blanco",
                    letterswithbasicpuncandspace: "El nombre de la prensa no puede tener caracteres especiales",
                    maxlength: "El nombre de la prensa no puede tener más de 90 caracteres",
                    remote: "Ya existe una prensa registrada con ese nombre",
                },
                'pe-siglas': {
                    required: "Las siglas de la prensa no puede quedar en blanco",
                    letterswithbasicpuncandspace: "Las siglas de la prensa no puede tener caracteres especiales",
                    maxlength: "Las siglas de la prensa no puede tener más de 15 caracteres",
                },
                'pe-nombre_contacto': {
                    required: "El nombre de contacto de la prensa no puede quedar en blanco",
                    letterswithbasicpuncandspace: "El nombre de contacto de la prensa no puede tener caracteres especiales",
                    maxlength: "El nombre de contacto de la prensa no puede tener más de 200 caracteres",
                },
                'pe-email': {
                    required: "El correo electrónico de la prensa no puede quedar en blanco",
                    email: "El correo electrónico de la prensa tiene que ser un correo electrónico válido",
                },
                'pe-telefono': {
                    required: "El teléfono de la prensa no puede quedar en blanco",
                    digits: "El teléfono de la prensa solo puede tener dígitos",
                    minlength: "El teléfono de la prensa no puede tener más de 8 dígitos",
                    maxlength: "El teléfono de la prensa no puede tener menos de 8 dígitos",
                },
                'telefono-numero': {
                    required: "El número de teléfono no puede quedar en blanco",
                    digits: "El número de teléfono solo puede tener dígitos",
                    minlength: "El número de teléfono no puede tener menos de 8 dígitos",
                    maxlength: "El número de teléfono no puede tener más de 8 dígitos",
                    remote: "Ya existe registrado ese número de telefono con el mismo nombre de contacto",
                },
                'telefono-nombre_contacto': {
                    required: "El nombre de contacto no puede quedar en blanco",
                    letterswithbasicpuncandspace: "El nombre de contacto no puede tener caracteres especiales",
                    maxlength: "El nombre de contacto no puede tener más de 220 caracteres",
                },
                'web-nombre': {
                    required: "El nombre no puede quedar en blanco",
                    letterswithbasicpuncandspace: "El nombre no puede tener caracteres especiales",
                    maxlength: "El nombre no puede tener más de 200 caracteres",
                    minlength: "El nombre no puede tener menos de 3 caracteres",
                },
                'web-perfil': {
                    required: "El perfil no puede quedar en blanco",
                    minlength: "El perfil no puede tener menos de 3 caracteres",
                    maxlength: "El perfil no puede tener más de 200 caracteres",
                    letterswithbasicpuncandspace: "El perfil no puede tener caracteres especiales",
                    // remote: "Ya existe un prefil web igual en la misma red social registrado",
                },
                'web-email': {
                    required: "El correo electrónico no puede quedar en blanco",
                    email: "El correo electrónico tiene que ser un correo electrónico válido",
                    // remote: "Ya existe un perfil web registrado con este email en el misma red social",
                },
                'web-red_social': {
                    required: "Tiene que seleccionar una red social",
                },

            }
        });
        procedencia_form.on("submit", function (e) {
            if (ajax_request) {
                e.preventDefault();
                $(this).ajaxSubmit({
                    type: "POST",
                    success: function (response) {
                        if (typeof ajax_callback === "function")
                            ajax_callback(response);
                    }
                });
            }
        });

        const _clearEmpProcedence = function () {
                $pj_municipio[0].selectize.clear();
                $pj_cpopular[0].selectize.clear();
                $pj_direccion_calle[0].selectize.clear();
                $pj_direccion_entrecalle2[0].selectize.clear();
                $pj_direccion_entrecalle1[0].selectize.clear();
                $("#id_empresa-nombre").val("");
                $("#id_empresa-sigla").val("");
                $("#id_empresa-telefono").val("");
                $("#id_empresa-movil").val("");
                $("#id_empresa-nombre_contacto").val("");
                $("#id_empresa-codigo_nit").val("");
                $("#id_empresa-codigo_reuup").val("");
                $("#id_empresa-direccion_numero").val("");
        };
        const _clearPersonProcedence = function () {
                $pn_genero[0].selectize.clear();
                $pn_direccion_calle[0].selectize.clear();
                $pn_direccion_entrecalle1[0].selectize.clear();
                $pn_direccion_entrecalle2[0].selectize.clear();
                $pn_municipio[0].selectize.clear();
                $pn_cpopular[0].selectize.clear();
                $("#id_person_procedence-ci").val("");
                $("#id_person_procedence-direccion_numero").val("");
                $("#id_person_procedence-nombre").val("");
                $("#id_person_procedence-apellidos").val("");
                $("#id_person_procedence-movil").val("");
                $("#id_person_procedence-email_address").val("");
                $("#id_person_procedence-telefono").val("");
        };
        const _clearEmailProcedence = function () {
            $("#id_email-email").val("");
            $("#id_email-nombre_contacto").val("");
        };
        const _clearOrgsProcedence = function () {
            $("#id_organism-nombre").val("");
            $("#id_organism-siglas").val("");
            $("#id_organism-email").val("");
            $("#id_organism-telefono").val("");
            $("#id_organism-nombre_contacto").val("");
        };
        const _clearOrgzProcedence = function () {
            $("#id_organiza-nombre").val("");
            $("#id_organiza-siglas").val("");
            $("#id_organiza-email").val("");
            $("#id_organiza-telefono").val("");
            $("#id_organiza-nombre_contacto").val("");
        };
        const _clearWebProcedence = function () {
            $("#id_web-nombre").val("");
            $("#id_web-perfil").val("");
            $("#id_web-email").val("");
            $wp_red_social[0].selectize.clear();
        };
        const _clearPrensaProcedence = function () {
            $("#id_pe-nombre").val("");
            $("#id_pe-siglas").val("");
            $("#id_pe-nombre_contacto").val("");
            $("#id_pe-email").val("");
            $("#id_pe-telefono").val("");
        };
        const _clearPhoneProcedence = function () {
            $("#id_telefono-numero").val("");
            $("#id_email-nombre_contacto").val("");
        };
        const _clearAllProcedence = function () {
            _clearEmpProcedence();
            _clearPersonProcedence();
            _clearEmailProcedence();
            _clearOrgsProcedence();
            _clearOrgzProcedence();
            _clearPrensaProcedence();
            _clearPhoneProcedence();
            _clearWebProcedence();
        };
        var _toggleProcedenciaForms = function () {

            if ($('#id_procedencia-tipo').val() == '') {
                _clearAllProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').addClass('col-lg-12').removeClass('col-lg-6');
                $('.modal-body .procedent').addClass('no-show');
                if ($('button[type="submit"]').hasClass('disabled')){
                    $('button[type="submit"]').removeClass('disabled');}
            } else if ($('#id_procedencia-tipo').val() == '1') {
                _clearAllProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.modal-body .procedent').addClass('no-show');
                $('#anon_block').removeClass('no-show');
                if (anon)
                    $('button[type="submit"]').addClass('disabled');
            } else if ($('#id_procedencia-tipo').val() == '2') {
                _clearEmpProcedence();
                _clearPersonProcedence();
                _clearOrgsProcedence();
                _clearOrgzProcedence();
                _clearWebProcedence();
                _clearEmailProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.modal-body .procedent').addClass('no-show');
                $('#prensa_block').removeClass('no-show');
                if ($('button[type="submit"]').hasClass('disabled')){
                    console.log("la iene");
                    $('button[type="submit"]').removeClass('disabled');}
            } else if ($('#id_procedencia-tipo').val() == '3') {
                _clearEmpProcedence();
                _clearEmailProcedence();
                _clearPrensaProcedence();
                _clearOrgsProcedence();
                _clearOrgzProcedence();
                _clearWebProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.modal-body .procedent').addClass('no-show');
                $('#persona_block').removeClass('no-show');
                if ($('button[type="submit"]').hasClass('disabled'))
                    $('button[type="submit"]').removeClass('disabled');
            } else if ($('#id_procedencia-tipo').val() == '4') {
                _clearEmpProcedence();
                _clearPersonProcedence();
                _clearOrgsProcedence();
                _clearOrgzProcedence();
                _clearWebProcedence();
                _clearEmailProcedence();
                _clearPrensaProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.modal-body .procedent').addClass('no-show');
                $('#telefono_block').removeClass('no-show');
                if ($('button[type="submit"]').hasClass('disabled'))
                    $('button[type="submit"]').removeClass('disabled');
            } else if ($('#id_procedencia-tipo').val() == '5') {
                _clearEmpProcedence();
                _clearPersonProcedence();
                _clearPrensaProcedence();
                _clearOrgsProcedence();
                _clearOrgzProcedence();
                _clearWebProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.modal-body .procedent').addClass('no-show');
                $('#correo_block').removeClass('no-show');
                if ($('button[type="submit"]').hasClass('disabled'))
                    $('button[type="submit"]').removeClass('disabled');
            } else if ($('#id_procedencia-tipo').val() == '6') {
                _clearPersonProcedence();
                _clearEmailProcedence();
                _clearOrgsProcedence();
                _clearOrgzProcedence();
                _clearWebProcedence();
                _clearPrensaProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.modal-body .procedent').addClass('no-show');
                $('#empresa_block').removeClass('no-show');
                if ($('button[type="submit"]').hasClass('disabled'))
                    $('button[type="submit"]').removeClass('disabled');
            } else if ($('#id_procedencia-tipo').val() == '7') {
                _clearEmpProcedence();
                _clearPersonProcedence();
                _clearOrgsProcedence();
                _clearWebProcedence();
                _clearEmailProcedence();
                _clearPrensaProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.modal-body .procedent').addClass('no-show');
                $('#orgz_block').removeClass('no-show');
                if ($('button[type="submit"]').hasClass('disabled'))
                    $('button[type="submit"]').removeClass('disabled');
            } else if ($('#id_procedencia-tipo').val() == '8') {
                _clearEmpProcedence();
                _clearPersonProcedence();
                _clearEmailProcedence();
                _clearOrgzProcedence();
                _clearWebProcedence();
                _clearPrensaProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.modal-body .procedent').addClass('no-show');
                $('#org_block').removeClass('no-show');
                if ($('button[type="submit"]').hasClass('disabled'))
                    $('button[type="submit"]').removeClass('disabled');
            } else if ($('#id_procedencia-tipo').val() == '9') {
                _clearEmpProcedence();
                _clearPersonProcedence();
                _clearEmailProcedence();
                _clearOrgsProcedence();
                _clearOrgzProcedence();
                _clearPrensaProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.modal-body .procedent').addClass('no-show');
                $('#web_block').removeClass('no-show');
                if ($('button[type="submit"]').hasClass('disabled'))
                    $('button[type="submit"]').removeClass('disabled');
            }
            $('#prensa-new-form,#persona-new-form,#phone-new-form,#email-new-form,#empresa-new-form,#organiz-new-form,#organis-new-form,#web-new-form').addClass('no-show')
        };
    };

    return {
        init: function (translations) {
            _initProcedenciaPane(translations);
        },
        initForm: function () {
            procedencia_form = $('#formodal_procedencia');
            _initProcedenciaForm();
        },
        setAjax: function (is_ajax, callback = null) {
            ajax_request = !!(is_ajax);
            ajax_callback = callback;
        }
    }
}();