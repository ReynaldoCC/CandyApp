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

var DPVMunicipioNom =  function () {
    let municipio_form;
    let validator_form;

    const _initMunicipioPane = function (translations) {
        $('#municipio-table').DataTable({
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
    const _initMunicipioForm =  function () {
        $("#filter_calles").on("keyup", function() {
            var value = $(this).val().toLowerCase();
                $("#id_calles span").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        });
        $("#check_all_calles").on("click", function(){
            $("span:not([style='display: none;']) input[name='calles']").prop('checked', this.checked);
        });
        let $pj_prov = $("#id_provincia").selectize({
            create: false,
            placeholder: "Selecione una Provincia",
            allowEmptyOption: false,
        });

        const _fill_selectizes_with_values = function () {
            if ($("#id_provincia").val())
                $pj_prov[0].selectize.setValue($("#id_provincia").val());
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
        validator_form = municipio_form.validate({
			rules: {
				nombre: {
				    maxlength: 90,
				    required: true,
                    remote: {
                        url: '/nomenclador/verify_municipio/',
                        type: 'GET',
                        data: {
                            id: mun_id,
                        },
                    },
				},
				numero: {
				    required: true,
                    maxlength: 50,
                    min: 1,
                    remote: {
                        url: '/nomenclador/verify_municipio/',
                        type: 'GET',
                        data: {
                            id: mun_id,
                        },
                    },
				},
				provincia: {
				    required: true,
				},
			},
			messages: {
				nombre: {
				    maxlength: "El nombre no puede tener más de 90 caracteres.",
				    required: "El nombre es obligatorio.",
                    remote: "Ya existe otra provincia registrada con ese nombre.",
				},
				numero: {
				    required: "El número es obligatorio.",
                    maxlength: "El número no puede tener más de 3 dígitos.",
                    min: "El número no puede ser menor que 1.",
                    remote: "Ya existe otra provincia registrada con ese número",
				},
				provincia: {
				    required: "Tiene que seleccionar una provincia.",
				},
			},
		});
        _fill_selectizes_with_values();
    };

    return {
        init: function (translations) {
            _initMunicipioPane(translations);
        },
        initForm: function () {
            municipio_form = $('#form_municipio');
            _initMunicipioForm();
        },
    }
}();