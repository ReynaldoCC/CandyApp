function abrir_modal(url, id=null)
{
    $('#popup').load(url, function(id)
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


var DPVEntidad = function () {
    let entidad_form;
    let validator_form;
    let tmp;

    const _makeAlert = function(type, text, success, negate, title=null, accept=null, cancel=null, plus=null) {
        let dataplus = plus || tmp;
        Swal.fire({
            title: title || "Error",
            html: text,
            icon: type,
            showCloseButton: true,
            showCancelButton: true,
            focusConfirm: false,
            confirmButtonText: accept || '<i class="fa fa-thumbs-up"></i> Si',
            confirmButtonAriaLabel: 'Correto',
            cancelButtonText: cancel || '<i class="fa fa-thumbs-down"></i> No',
            cancelButtonAriaLabel: 'Cancelar',
            showClass: {
                popup: 'animated fadeInDown faster',
            },
            hideClass: {
                popup: 'animated fadeOutUp faster',
            },
        }).then((result) => {
            if (result.value) {
                if (success != null) {
                    if (typeof(success) == 'function')
                        success(dataplus);
                }
            } else {
                if (negate != null) {
                    negate(dataplus);
                }
            }
        });
    };
    const _initEntidadPane = function (translations) {
        $('#entidad-table').DataTable({
            responsive: true,
            order: [ 0, 'desc' ],
            sScrollX: "100%",
            lengthMenu: [20, 35, 50, "All"],
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
    const _initEntidadForm = function () {
        let $pj_municipio = $("#id_municipio").selectize({
            create: false,
            placeholder: "Selecione un municipio",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $.ajax({
                    url: '/nomenclador/consejopopular/filter/' + value,
                    success: function(results) {
                        let current_value = $pj_cpopular[0].selectize.getValue();
                        let exist = false;
                        for (let i = 0; i < results.length; i++)
                            if (results[i].id == current_value) {
                                exist = true;
                            }
                        if (!exist)
                        $pj_cpopular[0].selectize.clear();
                        $pj_cpopular[0].selectize.clearOptions();
                        $pj_cpopular[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
                $.ajax({
                    url: '/nomenclador/calle/filter/' + value,
                    success: function(results) {
                        let current_value1 = $pj_direccion_calle[0].selectize.getValue();
                        let current_value2 = $pj_direccion_entrecalle1[0].selectize.getValue();
                        let current_value3 = $pj_direccion_entrecalle2[0].selectize.getValue();
                        let exist1 = false;
                        let exist2 = false;
                        let exist3 = false;
                        for (let i = 0; i < results.length; i++) {
                            if (results[i].id == current_value1) {
                                exist1 = true;
                            }
                            if (results[i].id == current_value2) {
                                exist2 = true;
                            }
                            if (results[i].id == current_value3) {
                                exist3 = true;
                            }
                        }
                        if (!exist1)
                        $pj_direccion_calle[0].selectize.clear();
                        $pj_direccion_calle[0].selectize.clearOptions();
                        $pj_direccion_calle[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist2)
                            $pj_direccion_entrecalle1[0].selectize.clear();
                        $pj_direccion_entrecalle1[0].selectize.clearOptions();
                        $pj_direccion_entrecalle1[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist3)
                            $pj_direccion_entrecalle2[0].selectize.clear();
                        $pj_direccion_entrecalle2[0].selectize.clearOptions();
                        $pj_direccion_entrecalle2[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
            },
        });
        let $pj_cpopular = $("#id_cpopular").selectize({
            placeholder: "Selecione un Consejo Popular",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        let $pj_direccion_calle = $("#id_direccion_calle").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        let $pj_direccion_entrecalle2 = $("#id_direccion_entrecalle2").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        let $pj_direccion_entrecalle1 = $("#id_direccion_entrecalle1").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });

        const _fill_selectizes_with_values = function () {
            if ($("#id_municipio").val())
                $pj_municipio[0].selectize.setValue($("#id_municipio").val());
            if ($("#id_cpopular").val())
                $pj_cpopular[0].selectize.setValue($("#id_cpopular").val());
            if ($("#id_direccion_calle").val())
                $pj_direccion_calle[0].selectize.setValue($("#id_direccion_calle").val());
            if ($("#id_direccion_entrecalle1").val())
                $pj_direccion_entrecalle1[0].selectize.setValue($("#id_direccion_entrecalle1").val());
            if ($("#id_direccion_entrecalle2").val())
                $pj_direccion_entrecalle2[0].selectize.setValue($("#id_direccion_entrecalle2").val());
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
                    error.insertAfter(element.parent());
                else
                    error.insertAfter(element);
            },

        });
        validator_form = entidad_form.validate({
			rules: {
				direccion_calle: {
				    required: true,
				},
				direccion_numero: {
				    required: true,
				},
				direccion_entrecalle1: {
				    required: true,
				},
				direccion_entrecalle2: {
				    required: true,
				},
				municipio: {
				    required: true,
				},
				cpopular: {
				    required: true,
				},
				nombre: {
				    maxlength: 100,
				    required: true,
                    remote: {
                        url: '/persona/juridica/verify',
                        type: 'GET',
                        data: {
                            id: entidad_id,
                        },
                    },
				},
				email_address: {
				    email: true,
                    remote: {
                        url: '/persona/juridica/verify',
                        type: 'GET',
                        data: {
                            id: entidad_id,
                        },
                    },
				},
                nombre_contacto: {
				    maxlength: 200,
				    required: true,
				},
                sigla: {
				    maxlength: 15,
				    required: true,
				},
                codigo_nit: {
				    maxlength: 11,
                    minlength:11,
				    required: true,
                    remote: {
                        url: '/persona/juridica/verify',
                        type: 'GET',
                        data: {
                            id: entidad_id,
                        },
                    },
				},
                codigo_reuup: {
				    maxlength: 11,
                    minlength:11,
				    required: true,
                    remote: {
                        url: '/persona/juridica/verify',
                        type: 'GET',
                        data: {
                            id: entidad_id,
                        },
                    },
				},
				movil: {
				    required: false,
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                    remote: {
                        url: '/persona/juridica/verify',
                        type: 'GET',
                        data: {
                            id: entidad_id,
                        },
                    },
                },
				telefono: {
				    required: true,
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                    remote: {
                        url: '/persona/juridica/verify',
                        type: 'GET',
                        data: {
                            id: entidad_id,
                        },
                    },
                },
			},
			messages: {
				direccion_calle: {
				    required: "Tiene que seleccionar una calle.",
				},
				direccion_numero: {
				    required: "El número de la dirección no puede quedar en blanco.",
				},
				direccion_entrecalle1: {
				    required: "Tiene que seleccionar una calle.",
				},
				direccion_entrecalle2: {
				    required: "Tiene que seleccionar una calle.",
				},
				municipio: {
				    required: "Tiene que seleccionar un municipio.",
				},
				cpopular: {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				nombre: {
				    maxlength: "El nombre no puede tener más de 100 caracteres.",
				    required:  "El nombre es obligatorio.",
                    remote: "Ya existe otra entidad con el mismo nombre.",
				},
				email_address: {
				    email: "El correo electrónico es obligatorio.",
                    remote: "Ya existe otra entidad con el mismo correo electrónico.",
				},
                nombre_contacto: {
				    maxlength: "El nombre no puede tener más de 200 caracteres.",
				    required: "El nombre de contacto es obligatorio.",
				},
                sigla: {
				    maxlength: "La sigla no puede tener más de 15 caracteres.",
				    required: "la sigla es obligatoria.",
				},
                codigo_nit: {
				    maxlength: "El código NiT no puede tener más de 11 caracteres.",
                    minlength: "El código NiT no puede tener menos de 11 caracteres.",
				    required: "El código NiT es obligatorio.",
                    remote: "Ya existe otra entidad con ese mismo codigo NiT.",
				},
                codigo_reuup: {
				    maxlength: "El código Reuup no puede tener más de 11 caracteres.",
                    minlength: "El código Reuup no puede tener menos de 11 caracteres.",
				    required: "El código Reuup es obligatorio.",
                    remote: "Ya existe otra entidad con ese mismo codigo Reuup.",
				},
				movil: {
                    digits: "El número del móvil solo puede tener dígitos.",
                    maxlength: "El número del móvil no puede tener más de 8 dígitos.",
                    minlength: "El número del móvil no puede tener menos de 8 dígitos.",
                    remote: "Ya existe Otra entidad con ese mismo número de movil.",
                },
				telefono: {
				    required: "El número de teléfono es obligatorio.",
                    digits: "El número de teléfono solo puede tener dígitos.",
                    maxlength: "El número de teléfono no puede tener más de 8 dígitos.",
                    minlength: "El número de teléfono no puede tener menos de 8 dígitos.",
                    remote: "Ya existe Otra entidad con ese mismo número de teléfono.",
                },
			},
		});

        _fill_selectizes_with_values();
    };

    return {
        init: function (translations) {
            _initEntidadPane(translations)
        },
        initForm: function () {
            entidad_form = $("#entidad-form");
            _initEntidadForm();
        },
    }

}();