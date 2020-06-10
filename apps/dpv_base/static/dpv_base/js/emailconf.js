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

const DPVEmailConf = function () {
    let validator_form;
    let emailconf_form;

    const _initEmailPane = function () {
        $('#custom-nav-profile-tab,#custom-nav-home-tab').on('click', function () {
            if (this.id === 'custom-nav-profile-tab') {
                $('#custom-nav-home-tab').removeClass('no-show');
            } else if ( this.id === 'custom-nav-home-tab') {
                $('#custom-nav-profile-tab').removeClass('no-show');
            } else {
                console.log('ID desconcocido');
            }
            $(this).addClass('no-show');
        });
        $('#none-radio,#id_use_tls,#id_use_ssl').on('change', function () {
            if (this.id === 'none-radio') {
                document.getElementById('id_use_tls').checked = false;
                document.getElementById('id_use_ssl').checked = false;
            }
            if (this.id === 'id_use_tls') {
                document.getElementById('none-radio').checked = false;
                document.getElementById('id_use_ssl').checked = false;
            }
            if (this.id === 'id_use_ssl') {
                document.getElementById('none-radio').checked = false;
                document.getElementById('id_use_tls').checked = false;
            }
        });

        emailconf_form.on('submit', function (event) {
            if (!emailconf_form.valid()) {
                event.preventDefault();
            }
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
                error.insertBefore(element.parent());
            },

        });
        $.validator.addMethod('FQDNOrIP', function(value, element) {
            return this.optional(element) || /^([a-z0-9]*[.])*[a-z0-9]*$/.test(value) || /((^\\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\\s*$)|(^\\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:)))(%.+)?\\s*$))|(^\\s*((?=.{1,255}$)(?=.*[A-Za-z].*)[0-9A-Za-z](?:(?:[0-9A-Za-z]|\\b-){0,61}[0-9A-Za-z])?(?:\\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|\\b-){0,61}[0-9A-Za-z])?)*)\\s*$)/i.test(value);
        }, 'El servidor no es un FQDN ó Dirección IP válida');
        validator_form = emailconf_form.validate({
			rules: {
				servidor: {
				    required: true,
                    maxlength: 150,
                    FQDNOrIP: true,
				},
				puerto: {
				    required: true,
				    digits: true,
                    min: 10,
                    minlength: 2,
                    maxlength: 5,
                    max: 65000,
				},
				usuario: {
				    minlength: 2,
                    maxlength: 120,
				},
				password: {
				    maxlength: 30,
				},
			},
			messages: {
				servidor: {
				    required: "El FQDN o la IP del servidor no puede quedar en blanco.",
                    maxlength: "El FQDN o la IP del servidor no puede tener más de 150 caracteres.",
                    FQDNOrIP: "El FQDN o la IP del servidor no es válido.",
				},
				puerto: {
				    required: "El puerto del servidor no puede quedar en blanco.",
				    digits: "El puerto del servidor solo puede contener dígitos.",
                    min: "El puerto de servidor no puede ser inferior a 10.",
                    minlength: "El puerto dle servidor no puede tener menos de 2 dígitos.",
                    maxlength: "El puerto del servidor no puede tener más de 5 dígitos.",
                    max: "El puerto del servidor no puede ser superior a 65000.",
				},
				usuario: {
				    minlength: "El usuario del servidor no puede tener menos de 2 caracteres.",
                    maxlength: "El usuario dle servidor no puede tener más de 120 caracteres.",
				},
				password: {
				    maxlength: "La contraseña no puede tener más de 30 caracteres.",
				},
			},
		});
    };

    return {
        init: function () {
            emailconf_form = $("#emailconf-form");
            _initEmailPane();
        },
    };
}();