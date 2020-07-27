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

var DPVCodAsuntoNom =  function () {
    let codasunto_form;
    let validator_form;

    const _initCodAsuntoPane = function (translations) {
        $('#codasunto-table').DataTable({
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
    const _initCodAsuntoForm =  function () {
        $.validator.setDefaults({
            errorClass: 'text-danger',
            highlight: function(element) {
                $(element).addClass('is-invalid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },

			ignore: ":hidden",

            errorPlacement: function(error, element) {
                if (element[0].attributes['type'].nodeValue === 'select-one' || element[0].attributes['type'].nodeValue === 'select-multiple')
                    error.insertBefore(element.parent());
                else
                    error.insertBefore(element);
            },

        });
        $.validator.addMethod("letterswithbasicpuncandspace", function(value, element) {
            return this.optional(element) || /^[a-zA-Z0-9áéíóúÁÉÚÍÓñÑ \-.,()'"\s]+$/i.test(value);
        }, "solo puede tener letras, números, y signos de puntuación básicos");
        validator_form = codasunto_form.validate({
			rules: {
				nombre: {
				    maxlength: 250,
				    required: true,
                    letterswithbasicpuncandspace: true,
                    remote: {
                        url: '/nomenclador/verify_codificadorasunto/',
                        type: 'GET',
                        data: {
                            id: codas_id,
                        },
                    },
				},
				numero: {
				    maxlength: 3,
				    required: true,
                    digits: true,
                    remote: {
                        url: '/nomenclador/verify_codificadorasunto/',
                        type: 'GET',
                        data: {
                            id: codas_id,
                        },
                    },
				},
			},
			messages: {
				nombre: {
				    maxlength: "El nombre del codificador de asunto no puede tener más de 90 caracteres.",
				    required: "El nombre del codificador de asunto es obligatorio.",
                    letterswithbasicpuncandspace: "El nombre del codificador de asunto solo puede tener letras, números, y signos de puntuación básicos.",
                    remote: "Ya existe otro codificador de asunto registrada con ese nombre.",
				},
				numero: {
				    maxlength: "El número del codificador de asunto no puede tener más de 3 dígitos.",
				    required: "El número del codificador de asunto es obligatorio.",
                    digits: "El número del codificador de asunto solo puede tener dígitos.",
                    remote: "Ya existe otro codificador de asunto registrada con ese número.",
				},
			},
		});
    };

    return {
        init: function (translations) {
            _initCodAsuntoPane(translations);
        },
        initForm: function () {
            codasunto_form = $('#form_codificadorasunto');
            _initCodAsuntoForm();
        },
    }
}();