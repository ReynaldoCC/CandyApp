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

    var _initInputs = function (){

        $(".form-select").selectize({
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

    };

    var _initValidateForm = function (){

        var form = $('#document-form').validate({

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

            rules: {
                'no_refer': {
                    required: true,
                },
                'procedencia': {
                    required: true,
                },
                'clasificacion': {
                    required: true,
                },
                'destino': {
                    required: true,
                },
            },
        });

    };

    return {
        init: function () {

            _initInputs();

            _initValidateForm();

        },
    };

} ();

jQuery(document).ready(function() {
    DPVDocumentos.init();
});