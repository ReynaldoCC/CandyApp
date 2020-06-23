
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

        let $pj_propietario = $("#id_propietario").selectize({
            create: false,
            placeholder: "Selecione un propietario",
            allowEmptyOption: false,
        });

        let pj_concepto = $("#id_concepto").selectize({
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
            ($("#id_destino").val())?($pj_destino[0].selectize.setValue($("#id_destino").val())):'';
            ($("#id_propietario").val())?($pj_propietario[0].selectize.setValue($("#id_propietario").val())):'';
            ($("#id_concepto").val())?(pj_concepto[0].selectize.setValue($("#id_concepto").val())):'';
            ($("#id_local_dado").val())?($pj_direccion_entrecalle2[0].selectize.setValue($("#id_local_dado").val())):'';
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

        validator_form = vivienda_form.validate({
			rules: {
				numero: {
				    required: true,
				    digits: true,
				},
                destino: {
				    required: true,
				    digits: true,
				},
                cantidad_persona: {
				    required: true,
				    digits: true,
                    maxlength: 5,
				},
                propietario: {
				    required: true,
				    digits: true,
				},
                local_dado: {
				    required: true,
				    digits: true,
				},
                fecha_propietario: {
				    required: true,
				},
                aprobada: {
				    required: true,
				},
                add_concepto: {
				    required: true,
                    maxlength: 200,
                    minlength: 1,
				},
			},
			messages: {
				numero: {
				    required: "Este campo es obligatorio.",
				    digits: "Este campo solo puede contener dígitos.",
				},
                destino: {
				    required: "Este campo es obligatorio.",
				    digits: "Este campo solo puede contener dígitos.",
				},
                cantidad_persona: {
				    required: "Este campo es obligatorio.",
				    digits: "Este campo solo puede contener dígitos.",
				},
                propietario: {
				    required: "Este campo es obligatorio.",
				    digits: "Este campo solo puede contener dígitos.",
				},
                local_dado: {
				    required: "Este campo es obligatorio.",
				    digits: "Este campo solo puede contener dígitos.",
				},
                aprobada: {
				    required: "Este campo es obligatorio.",
				    digits: "Este campo solo puede contener dígitos.",
				},
                add_concepto: {
				    required: "Este campo es obligatorio.",
				    digits: "Este campo solo puede contener dígitos.",
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