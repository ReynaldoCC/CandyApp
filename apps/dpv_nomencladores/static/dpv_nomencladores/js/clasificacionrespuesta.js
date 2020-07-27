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

var DPVClassResponseNom =  function () {
    let classresp_form;
    let validator_form;

    const _initClassResponsePane = function (translations) {
        $('#classresp-table').DataTable({
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
    const _initClassResponseForm =  function () {

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
        $.validator.addMethod("letterswithoutspace", function(value, element) {
            return this.optional(element) || /^[a-zA-Z0-9\-\s]+$/i.test(value);
        }, "solo puede tener letras y números, y guión medio");
        validator_form = classresp_form.validate({
			rules: {
				nombre: {
				    maxlength: 90,
				    required: true,
                    letterswithbasicpuncandspace: true,
                    remote: {
                        url: '/nomenclador/verify_clasificacionrespuesta/',
                        type: 'GET',
                        data: {
                            id: resp_id,
                        },
                    },
				},
				codigo: {
				    maxlength: 5,
				    required: true,
                    letterswithoutspace: true,
                    remote: {
                        url: '/nomenclador/verify_clasificacionrespuesta/',
                        type: 'GET',
                        data: {
                            id: resp_id,
                        },
                    },
				},
			},
			messages: {
				nombre: {
				    maxlength: "El nombre de la clasificación de respuesta no puede tener más de 90 caracteres.",
				    required: "El nombre de la clasificación de respuesta es obligatorio.",
                    letterswithbasicpuncandspace: "El nombre de la clasificación de respuesta solo puede tener letras, números, y signos de puntuación básicos.",
                    remote: "Ya existe otra clasificación de respuesta registrada con ese nombre.",
				},
				codigo: {
				    maxlength: "El código de la clasificación de respuesta no puede tener más de 5 caracteres.",
				    required: "El código de la clasificación de respuesta es obligatorio.",
                    letterswithoutspace: "El código de la clasificación de respuesta solo puede tener letras, números, y guion medio.",
                    remote: "Ya existe otra clasificación de respuesta registrada con ese código.",
                    },
				},
		});
    };

    return {
        init: function (translations) {
            _initClassResponsePane(translations);
        },
        initForm: function () {
            classresp_form = $('#form_clasificacionrespuesta');
            _initClassResponseForm();
        },
    }
}();