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

var DPVTipoProcNom =  function () {
    let tipo_proc_form;
    let validator_form;

    const _initTipoProcPane = function (translations) {
        $('#tproc-table').DataTable({
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
    const _initTipoProcForm =  function () {

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
        validator_form = tipo_proc_form.validate({
			rules: {
				nombre: {
				    maxlength: 90,
				    required: true,
                    letterswithbasicpuncandspace: true,
                    remote: {
                        url: '/nomenclador/verify_tipoprocedencia/',
                        type: 'GET',
                        data: {
                            id: tipo_id,
                        },
                    },
				},
                cant_dias: {
				    maxlength: 3,
                    min: 1,
				    required: true,
                    digits: true,
				},
			},
			messages: {
				nombre: {
				    maxlength: "El nombre del tipo de procedencia no puede tener más de 90 caracteres.",
				    required: "El nombre del tipo de procedencia es obligatorio.",
                    letterswithbasicpuncandspace: "El nombre del tipo de procedencia solo puede tener letras, números, y signos de puntuación básicos.",
                    remote: "Ya existe otro tipo de procedencia registrado con ese nombre.",
				},
                cant_dias: {
				    maxlength: "La cantidad e días no puede tener más de 3 dígitos 3.",
                    min: "La cantidad e días no puede ser menor a 1.",
				    required: "La cantidad e días es obligatorio.",
                    digits: "La cantidad e días solo puede contener dígitos.",
				},
			},
		});
    };

    return {
        init: function (translations) {
            _initTipoProcPane(translations);
        },
        initForm: function () {
            tipo_proc_form = $('#form_tipoprocedencia');
            _initTipoProcForm();
        },
    }
}();