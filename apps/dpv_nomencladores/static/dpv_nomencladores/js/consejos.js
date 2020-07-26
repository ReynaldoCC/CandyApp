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

var DPVConsejoPNom =  function () {
    let consejo_form;
    let validator_form;

    const _initConsejoPPane = function (translations) {
        $('#consejo-table').DataTable({
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
    const _initConsejoPForm =  function () {

        let $pj_prov = $("#id_municipio").selectize({
            create: false,
            placeholder: "Selecione un Municipio",
            allowEmptyOption: false,
        });

        const _fill_selectizes_with_values = function () {
            if ($("#id_municipio").val())
                $pj_prov[0].selectize.setValue($("#id_municipio").val());
        };
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
        validator_form = consejo_form.validate({
			rules: {
				nombre: {
				    maxlength: 90,
				    required: true,
                    letterswithbasicpuncandspace: true,
                    remote: {
                        url: '/nomenclador/verify_consejopopular/',
                        type: 'GET',
                        data: {
                            id: cpop_id,
                        },
                    },
				},
                numero: {
				    required: true,
                    digits: true,
                    min: 1,
                    remote: {
                        url: '/nomenclador/verify_consejopopular/',
                        type: 'GET',
                        data: {
                            id: cpop_id,
                        },
                    },
                },
                municipio: {
				    required: true,
                },
			},
			messages: {
				nombre: {
				    maxlength: "El nombre del consejo popular no puede tener más de 90 caracteres.",
				    required: "El nombre del consejo popular es obligatorio.",
                    letterswithbasicpuncandspace: "El nombre del consejo popular solo puede tener letras, números, y signos de puntuación básicos.",
                    remote: "Ya existe otro consejo popular registrado con ese nombre.",
				},
                numero: {
				    required: "El número del consejo popular es obligatorio.",
                    digits: "El número del consejo popular solo puede tener dígitos.",
                    min: "El número del consejo popular no puede ser menor que 1.",
                    remote: "Ya existe otro consejo popular registrado con ese número.",
                },
                municipio: {
				    required: "Tiene que seleccionar un municipio.",
                },
			},
		});
        _fill_selectizes_with_values();
    };

    return {
        init: function (translations) {
            _initConsejoPPane(translations);
        },
        initForm: function () {
            consejo_form = $('#form_consejopopular');
            _initConsejoPForm();
        },
    }
}();