$(document).ready(function(){
    $("#filter_groups").on("keyup", function() {
        var value = $(this).val().toLowerCase();
            $("#id_groups span").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $("#filter_user_permissions").on("keyup", function() {
        var value = $(this).val().toLowerCase();
            $("#id_user_permissions span").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $("#check_all_groups").on("click", function(){
        if ($("#check_all_groups").prop('checked'))
            $("input[name='groups']").attr('checked', true);
        else
            $("input[name='groups']").attr('checked', false);
    });
    $("#check_all_user_permissions").on("click", function(){
       if ($("#check_all_user_permissions").prop('checked')) {
            $("input[name='user_permissions']").attr('checked', true);
        }else
            $("input[name='user_permissions']").attr('checked', false);
    });
});

function create_calle()
{
    console.log("creating calle");
}

function abrir_modal(url, id=null)
{
    $('#add_calle').load(url, function(id)
    {
        $(this).modal('show');
    });
    return false;
}

function cerrar_modal()
{
    $('#add_calle').modal('hide');
    return false;
}

const DPVUsuario = function () {
    let user_form;
    let tmp;
    let validator_form;

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
    const _initPersoNatPane = function () {

    };
    const _initPersoNatForm = function () {

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
        let $pj_genero = $("#id_genero").selectize({
            create: false,
            placeholder: "Selecione un género",
            allowEmptyOption: false,
        });
        let $pj_unidad = $("#id_centro_trabajo").selectize({
            create: false,
            placeholder: "Selecione una Unidad",
            allowEmptyOption: false,
        });
        let $pj_dpto = $("#id_depto_trabajo").selectize({
            create: false,
            placeholder: "Selecione un Dpto.",
            allowEmptyOption: false,
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
            if ($("#id_genero").val())
                $pj_genero[0].selectize.setValue($("#id_genero").val());
            if ($("#id_depto_trabajo").val())
                $pj_dpto[0].selectize.setValue($("#id_depto_trabajo").val());
            if ($("#id_centro_trabajo").val())
                $pj_unidad[0].selectize.setValue($("#id_centro_trabajo").val());
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
        $.validator.addMethod('strongPass', function(value, element) {
            return this.optional(element) || /\d/.test(value) && /[a-z]/i.test(value) && /[*.,&^%$#@!<>?\/\\]/i.test(value);
        }, 'La contraseña debe contener al menos un dígito, un caracter alfabético y un caracter especial');
        $.validator.addMethod('ciCorrect', function(value, element) {
            var valid_month = true;
            var valid_date = true;
            if (value.length >= 6){
                var ci_month = value.substring(2,4);
                var ci_day = value.substring(4,6);
                var ci_year = value.substring(0,2);
                var month = parseInt(ci_month);
                var year = parseInt(ci_year);
                var valid_month = month <= 12;
                var day_date = new Date(parseInt(ci_year), parseInt(ci_month)-1, parseInt(ci_day))
                var valid_date = day_date.getMonth() === month-1 && day_date.getYear() === year
            }
            return this.optional(element) || valid_month && valid_date;
        }, 'Los 6 primeros dígitos del No. de identificación deben formar una fecha válida');
        validator_form = user_form.validate({
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
				ci: {
				    required: true,
				    digits: true,
                    maxlength: 11,
                    minlength: 11,
                    ciCorrect: true,
                    remote: {
                        url: '/persona/natural/verify',
                        type: 'GET',
                        data: {
                            id: person_id,
                        },
                    },
				},
				nombre: {
				    maxlength: 30,
				    required: true,
				},
				apellidos: {
				    required: true,
                    maxlength: 50,
				},
				genero: {
				    required: true,
				},
				email: {
				    required: true,
				    email: true,
                    remote: {
                        url: '/admin/users/verify/',
                        type: 'GET',
                        data: {
                            id: user_id,
                        },
                    },
				},
				movil: {
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                    remote: {
                        url: '/persona/natural/verify',
                        type: 'GET',
                        data: {
                            id: person_id,
                        },
                    },
                },
				telefono: {
				    required: true,
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                },
                username: {
				    required: true,
                    maxlength: 50,
                    remote: {
                        url: '/admin/users/verify/',
                        type: 'GET',
                        data: {
                            id: user_id,
                        },
                    },
                },
                first_name: {
				    required: true,
                    maxlength: 30,
                },
                last_name: {
				    required: true,
                    maxlength: 50,
                },
                password: {
				    strongPass: true,
				    required: true,
                    maxlength: 50,
                    minlength: 8,
                },
                confirm_password: {
				    equalTo: '#id_password',
				    required: true,
                },
			},
			messages: {
                username: {
				    required: "El nombre de usuario no puede quedar en blanco.",
                    maxlength: "El nombre de usuario no puede contener más de 50 caracteres.",
                    remote: "El nombre de usuario es único y ya existe otra persona registrada con ese nombre de usuario.",
                },
                first_name: {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "El nombre de usuario no puede contener más de 30 caracteres.",
                },
                last_name: {
				    required: "Los Apellidos no pueden quedar en blanco.",
                    maxlength: "Los Apellidos no pueden contener más de 50 caracteres.",
                },
                password: {
				    required: "La contraseña no puede quedar en blanco.",
                    maxlength: "La contraseña no pueden contener más de 50 caracteres.",
                    minlength: "La contraseña no pueden contener menos de 8 caracteres.",
                },
                confirm_password: {
				    equalTo: "La contraseña y su confirmación no coinciden y deben ser iduales.",
				    required: "La confirmación de la contraseña no puede quedar en blanco.",
                },
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
				ci: {
				    required: "El CI no puede quedar en blanco.",
				    digits: "El CI solo puede contener dígitos.",
                    maxlength: "El CI no puede contener más de 11 dígitos.",
                    minlength: "El CI no puede contener menos de 11 dígitos.",
                    remote: "El CI es único y ya existe otra persona registrada con ese CI.",
				},
				nombre: {
				    maxlength: "El Nombre no puede contener más de 30 caracteres.",
				    required: "El Nombre no puede quedar en blanco.",
				},
				apellidos: {
				    required: "Los Apellidos no pueden quedar en blanco.",
                    maxlength: "Los Apellidos no pueden contener más de 50 caracteres.",
				},
				genero: {
				    required: "Tiene que seleccionar un género.",
				},
				email: {
				    email: "El email no es un email válido.",
				    required: "El Email no puede quedar en blanco.",
                    remote: "El Email es único y ya existe otra persona registrada con ese Email.",
				},
				movil: {
                    digits: "El movil solo puede contener dígitos.",
                    maxlength: "El movil no puede contener más de 8 dígitos.",
                    minlength: "El movil no puede contener menos de 8 dígitos.",
                    remote: "El movil es único y ya existe otra persona registrada con ese movil.",
                },
				telefono: {
                    digits: "El teléfono solo puede contener dígitos.",
                    maxlength: "El teléfono no puede contener más de 8 dígitos.",
                    minlength: "El teléfono no puede contener menos de 8 dígitos.",
                },
			},
		});

        _fill_selectizes_with_values();
    };

    return {
        init: function () {
            _initPersoNatPane();
        },
        initForm: function () {
            user_form = $("#user-form");
            _initPersoNatForm();
        },
    };
}();
