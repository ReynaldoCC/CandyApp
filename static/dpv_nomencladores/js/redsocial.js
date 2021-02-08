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

var DPVRedSocialNom =  function () {
    let redsocial_form;
    let validator_form;
    let ajax_request = false;

    const _initRedSocialPane = function (translations) {
        $('#rsocial-table').DataTable({
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
    const _initRedSocialForm =  function () {

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
                if (element[0].attributes['type'].nodeValue === 'select-one' || element[0].attributes['type'].nodeValue === 'select-multiple')
                    error.insertBefore(element.parent());
                else
                    error.insertBefore(element);
            },

        });
        $.validator.addMethod("letterswithbasicpuncandspace", function(value, element) {
            return this.optional(element) || /^[a-zA-Z0-9áéíóúÁÉÚÍÓñÑ \-.,()'"\s]+$/i.test(value);
        }, "solo puede tener letras, números, y signos de puntuación básicos");

        redsocial_form.validate({
            rules: {
                'nombre': {
                    required: true,
                    minlength: 3,
                },
                'logo': {
                    required: true,
                },
                'url': {
                    required: true,
                    minlength: 3,
                    url: true,
                },
            },
            messages: {
                'nombre': {
                    required: "El nombre no puede quedar en blanco",
                    minlength: "El nombre no puede tener menos de 3 caracteres",
                },
                'logo': {
                    required: "Tiene que seleccionar un Logo",
                },
                'url': {
                    required: "La URL no puede quedar en blanco",
                    minlength: "La URL no puede tener menos de 3 caracteres",
                    url: "Debe ser una URL valida",
                },
            }
        });
        redsocial_form.on("submit", function (e) {
            if (ajax_request) {
                e.preventDefault();
                $(this).ajaxSubmit();
            }
        });
    };

    return {
        init: function (translations) {
            _initRedSocialPane(translations);
        },
        initForm: function () {
            redsocial_form = $('#form_rsocial');
            _initRedSocialForm();
        },
        setAjax: function (is_ajax) {
            ajax_request = !!(is_ajax);
        }
    }
}();