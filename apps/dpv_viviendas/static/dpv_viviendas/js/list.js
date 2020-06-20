
function abrir_modal(url)
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

var DPVViviendas = function () {
    let vivienda_form;
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
            }else {
                if (negate != null) {
                    negate(dataplus);
                }
            }
        });
    };

    const _initUserPane = function (translations) {
        $('#users-table').DataTable({
            responsive: true,
            order: [ 0, 'desc' ],
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
    };

    const _initViviendaForm = function () {

        let $pj_destino = $("#id_destino").selectize({
            create: false,
            placeholder: "Selecione un destino",
            allowEmptyOption: false,
        });

        let $pj_cpopular = $("#id_propietario").selectize({
            create: false,
            placeholder: "Selecione un propietario",
            allowEmptyOption: false,
        });

        let $pj_direccion_calle = $("#id_concepto").selectize({
            create: false,
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
        });

        let $pj_direccion_entrecalle2 = $("#id_local_dado").selectize({
            create: false,
            placeholder: "Selecione un local",
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
        validator_form = vivienda_form.validate({
			rules: {
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
                            id: 12,
                        },
                    },
				},
			},
			messages: {
				ci: {
				    required: "El CI no puede quedar en blanco.",
				    digits: "El CI solo puede contener dígitos.",
                    maxlength: "El CI no puede contener más de 11 dígitos.",
                    minlength: "El CI no puede contener menos de 11 dígitos.",
                    remote: "El CI es único y ya existe otra persona registrada con ese CI.",
				},
			},
		});

        _fill_selectizes_with_values();
    };

    return {
        // init: function (translations) {
        //     _initUserPane(translations);
        // },
        initForm: function () {
            vivienda_form = $("#vivienda-form");
            _initViviendaForm();
        },
    };
}();