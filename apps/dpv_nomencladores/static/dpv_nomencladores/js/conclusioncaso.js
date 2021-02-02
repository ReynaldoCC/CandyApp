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

var DPVConclusionCasoNom =  function () {
    let conclucioncaso_form;
    let validator_form;

    const _initConclusionCasoPane = function (translations) {
        $('#nivelsolucion-table').DataTable({
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
    const _initConclusionCasoForm =  function () {


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
        validator_form = nivelsolucion_form.validate({
			rules: {
				nombre: {
				    maxlength: 40,
				    required: true,
                    letterswithbasicpuncandspace: true,
                    remote: {
                        url: verify_url,
                        type: 'GET',
                        data: {
                            id: nivelsolucion_id,
                        },
                    },
				},
                codigo: {
				    maxlength: 3,
				    required: true,
				    lettersonly: true,
                    remote: {
                        url: verify_url,
                        type: 'GET',
                        data: {
                            id: nivelsolucion_id,
                        },
                    },
                }
			},
			messages: {
				nombre: {
				    maxlength: "El nombre de la conclusión del caso no puede tener más de 40 caracteres.",
				    required: "El nombre de la conclusión del caso es obligatorio.",
                    letterswithbasicpuncandspace: "El nombre de la conclusión del caso solo puede tener letras, números, y signos de puntuación básicos.",
                    remote: "Ya existe otra conclusión del caso registrada con ese nombre.",
				},
				codigo: {
				    maxlength: "El código no puede tener más de 3 caracteres.",
				    required: "El código es obligatorio.",
                    remote: "Ya existe otra conclusión del caso registrada con ese código.",
				},
			},
		});
    };

    return {
        init: function (translations) {
            _initConclusionCasoPane(translations);
        },
        initForm: function () {
            conclucioncaso_form = $('#form_conclusioncaso');
            _initConclusionCasoForm();
        },
    }
}();