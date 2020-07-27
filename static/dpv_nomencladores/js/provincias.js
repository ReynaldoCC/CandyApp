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

var DPVProvinciaNom =  function () {
    let provincia_form;
    let validator_form;

    const _initProvinciaPane = function (translations) {
        $('#provincia-table').DataTable({
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
    const _initProvinciaForm =  function () {

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
        validator_form = provincia_form.validate({
			rules: {
				nombre: {
				    maxlength: 90,
				    required: true,
                    letterswithbasicpuncandspace: true,
                    remote: {
                        url: '/nomenclador/verify_provincia/',
                        type: 'GET',
                        data: {
                            id: prov_id,
                        },
                    },
				},
                numero: {
				    required: true,
                    digits: true,
                    min: 1,
                    remote: {
                        url: '/nomenclador/verify_provincia/',
                        type: 'GET',
                        data: {
                            id: prov_id,
                        },
                    },
                },
			},
			messages: {
				nombre: {
				    maxlength: "El nombre de la provincia no puede tener más de 90 caracteres.",
				    required: "El nombre de la provincia es obligatorio.",
                    letterswithbasicpuncandspace: "El nombre de la provincia solo puede tener letras, números, y signos de puntuación básicos.",
                    remote: "Ya existe otra provincia registrada con ese nombre.",
				},
                numero: {
				    required: "El número de la provincia es obligatorio.",
                    digits: "El número de la provincia solo puede tener dígitos.",
                    min: "El número de la provincia no puede ser menor que 1.",
                    remote: "Ya existe otra provincia registrada con ese número.",
                }
			},
		});
    };

    return {
        init: function (translations) {
            _initProvinciaPane(translations);
        },
        initForm: function () {
            provincia_form = $('#form_provincia');
            _initProvinciaForm();
        },
    }
}();