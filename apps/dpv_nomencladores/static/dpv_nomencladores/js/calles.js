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

var DPVCalleNom =  function () {
    let calle_form;
    let validator_form;

    const _initCallePane = function (translations) {
        $('#calle-table').DataTable({
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
    const _initCalleForm =  function () {
        $("#filter_municipios").on("keyup", function() {
            var value = $(this).val().toLowerCase();
                $("#id_municipios span").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        });
        $("#check_all_municipios").on("click", function(){
            $("span:not([style='display: none;']) input[name='municipios']").prop('checked', this.checked);
        });

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
        validator_form = calle_form.validate({
			rules: {
				nombre: {
				    maxlength: 90,
				    required: true,
                    alphanumeric: true,
                    remote: {
                        url: '/nomenclador/verify_calle/',
                        type: 'GET',
                        data: {
                            id: calle_id,
                        },
                    },
				},
			},
			messages: {
				nombre: {
				    maxlength: "El nombre de la calle no puede tener más de 90 caracteres.",
				    required: "El nombre de la calle es obligatorio.",
                    alphanumeric: "El nombre de la calle solo puede contener caracteres alfanúmericos.",
                    remote: "Ya existe otra calle registrada con ese nombre.",
				},
			},
		});
    };

    return {
        init: function (translations) {
            _initCallePane(translations);
        },
        initForm: function () {
            calle_form = $('#form_calle');
            _initCalleForm();
        },
    }
}();