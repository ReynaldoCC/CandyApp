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

    var _initInputs = function () {

        $("#id_destino").selectize({
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
        $("#id_respuesta_a").selectize({
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
        if($("#id_respuesta_a").val() !== '')
            $("#id_respuesta_a").parent().parent().attr("style","display:none");

    };

    var _initValidateForm = function () {

        form.validate({

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
                'asunto': {
                    required: true,
                    maxlength: 400
                },
                'destino': {
                    required: true,
                },
                'responder_a': {
                    required: true,
                }
            },
        });

    };

    return {

        init: function () {
            form = $('#document-form');

            _initInputs();

            _initValidateForm();

        },

    };

} ();

jQuery(document).ready(function() {
    DPVDocumentos.init();
});