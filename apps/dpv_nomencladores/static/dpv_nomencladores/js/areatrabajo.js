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

var DPVDptoNom =  function () {
    let dpto_form;
    let validator_form;

    const _initDptoPane = function (translations) {
        $('#dpto-table').DataTable({
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
    const _initDptoForm =  function () {


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
        validator_form = dpto_form.validate({
			rules: {
				nombre: {
				    maxlength: 90,
				    required: true,
                    letterswithbasicpuncandspace: true,
                    remote: {
                        url: '/nomenclador/verify_departamento/',
                        type: 'GET',
                        data: {
                            id: dpto_id,
                        },
                    },
				},
				numero: {
				    min: 1,
				    required: true,
                    digits: true,
                    remote: {
                        url: '/nomenclador/verify_departamento/',
                        type: 'GET',
                        data: {
                            id: dpto_id,
                        },
                    },
				},
			},
			messages: {
				nombre: {
				    maxlength: "El nombre del departamento no puede tener más de 90 caracteres.",
				    required: "El nombre del departamento es obligatorio.",
                    letterswithbasicpuncandspace: "El nombre del departamento solo puede tener letras, números, y signos de puntuación básicos.",
                    remote: "Ya existe otro departamento registrado con ese nombre.",
				},
				numero: {
				    min: "El número del departamento no puede ser menor que 1.",
				    required: "El número del departamento es obligatorio.",
                    digits: "El número del departamento solo puede tener dígitos.",
                    remote: "Ya existe otro departamento registrado con ese número.",
				},
			},
		});
    };

    return {
        init: function (translations) {
            _initDptoPane(translations);
        },
        initForm: function () {
            dpto_form = $('#form_areatrab');
            _initDptoForm();
        },
    }
}();