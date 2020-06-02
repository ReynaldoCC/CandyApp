$(document).ready(function(){
    $("#filter_permissions").on("keyup", function() {
        var value = $(this).val().toLowerCase();
            $("#id_permissions span").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $("#check_all_permissions").on("click", function(){
        if ($("#check_all_permissions").prop('checked'))
            $("input[name='permissions']").attr('checked', true);
        else
            $("input[name='permissions']").attr('checked', false);
    });

});


const DPVGrupo = function () {
    let group_form;
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
    const _initGroupPane = function () {

    };
    const _initGroupForm = function () {

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

        validator_form = group_form.validate({
			rules: {
                name: {
				    required: true,
                    maxlength: 130,
                    remote: {
                        url: '/admin/group/verify/',
                        type: 'GET',
                        data: {
                            id: grp_id,
                        },
                    },
                },
			},
			messages: {
                name: {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "El nombre no puede contener más de 130 caracteres.",
                    remote: "El nombre es único y ya existe otro grupo registrado con ese nombre.",
                },
			},
		});

    };

    return {
        init: function () {
            _initGroupPane();
        },
        initForm: function () {
            group_form = $("#grp-form");
            _initGroupForm();
        },
    };
}();