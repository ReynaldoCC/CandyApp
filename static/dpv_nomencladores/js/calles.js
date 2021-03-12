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

var DPVCalleNom = function () {
    let calle_form;
    let validator_form;
    let ajax_request = false;
    let ajax_callback = null;

    let _make_alert = function (type, text) {
        Swal.fire({
            position: 'top-end',
            icon: type || 'success',
            title: text || 'Your work has been saved',
            showConfirmButton: false,
            timer: 2500
        })
    }
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
    const _initCalleForm = function () {
        $("#filter_municipios").on("keyup", function() {
            var value = $(this).val().toLowerCase();
                $("#id_municipios span").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        });
        $("#check_all_municipios").on("click", function(){
            $("span:not([style='display: none;']) input[name='municipios']").prop('checked', this.checked);
        });
        $('#save_more').on('click', function (e) {
            e.preventDefault();
            if (!$('#form_calle').valid())
                return;
            create_post(true);
        });
        $('#form_calle').on('submit', function (e) {
            if (ajax_request) {
                e.preventDefault();
                $(this).ajaxSubmit({
                    type: "POST",
                    success: function (response) {
                        if (typeof ajax_callback === "function")
                            ajax_callback(response);
                    }
                });
            }
        })

        var error_do = function (xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! Hemos encontrado un error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            _make_alert('error', 'No se ha popido agregar la calle');
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        };
        var success_agree = function (json) {
            $('#id_nombre').val("");
            _make_alert('success', 'La calle ha sido agregada con exito');
        };
        var create_post = function () {

            let form_data = $("#form_calle").serialize();
            $.ajax({
                url : "/nomenclador/new_calle/", // the endpoint
                type : "POST", // http method
                data : form_data,
                success : function(json) {
                    // console.log(json);
                    success_agree(json);
                },
                error : function(xhr,errmsg,err) {
                    error_do(xhr,errmsg,err);
                }
            });
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
        validator_form = calle_form.validate({
			rules: {
				nombre: {
				    maxlength: 90,
				    required: true,
                    letterswithbasicpuncandspace: true,
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
                    letterswithbasicpuncandspace: "El nombre de la calle solo puede tener letras, números, y signos de puntuación básicos.",
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
        setAjax: function (is_ajax, callback = null) {
            ajax_request = !!(is_ajax);
            ajax_callback = callback;
        }
    }
}();
