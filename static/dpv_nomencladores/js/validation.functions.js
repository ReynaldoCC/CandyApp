$.validator.addMethod("mname", function (value, element) {
    return this.optional(element) || /^[a-zA-ZáéíóúÁñÉÍÚÓ()",.\ ]+$/i.test(value);
}, '<p class="text-danger">Este campo solo debe contener letras.</p>');

$.validator.addMethod("mci", function (value, element) {
    if (this.optional(element))
        return this.optional(element) || /^[0-9]{11}$/i.test(value);
    if (/^[0-9]{11}$/i.test(value)) {
        var date = new Date();
        var anno = value.substr(0, 2);
        var mes = value.substr(2, 2);
        var dia = value.substr(4, 2);
        if (anno > date.getYear()) {
            return false;
        }
        if (mes < 1 || mes > 12) {
            return false;
        }
        if (dia < 1 || dia > 31) {
            return false;
        }
        if (mes % 2 == 0) {
            if (mes == 2) {
                if (dia < 1 || dia > 29) {
                    return false;
                }
            }
            if (mes == 8 || mes == 10 || mes == 12) {
                if (dia < 1 || dia > 31) {
                    return false;
                }
            } else {
                if (dia < 1 || dia > 30) {
                    return false;
                }
            }
        } else {
            if (mes == 9 || mes == 11) {
                if (dia < 1 || dia > 30) {
                    return false;
                }
            } else {
                if (dia < 1 || dia > 31) {
                    return false;
                }
            }
        }

        if (anno >= 0 && anno <= 18) {
            return false;
        }

        if (anno == (date.getYear() - 17)) {
            if (mes <= (date.getMonth() + 1) && dia < date.getDate())
                return true;
        } else if (anno <= (date.getYear() - 17)) {
            return true;
        } else {
            return false;
        }

    }
    return false;
}, '<p class="text-danger">Este campo no contiene un carnet de identidad válido.</p>');

$.validator.addMethod("mnum", function (value, element) {
    return this.optional(element) || /^[0-9A-Za-z]+$/i.test(value);
}, '<p class="text-danger">Este campo solo debe contener números y/o letras.</p>');

$.validator.addMethod("mnumber", function (value, element) {
    return this.optional(element) || /^[0-9]+$/i.test(value);
}, '<p class="text-danger">Este campo solo debe contener números.</p>');

$.validator.addMethod("malpha", function (value, element) {
    return this.optional(element) || /^[0-9a-zA-ZáéíóñúÁÉÍÚÓ\ ]+$/i.test(value);
}, '<p class="text-danger">Este campo solo debe contener caracteres alfanuméricos.</p>');

$.validator.addMethod("mphone", function (value, element) {
    return this.optional(element) || /^[0-9]{8}$/i.test(value);
}, '<p class="text-danger">El teléfono debe contener 8 números.</p>');

$.validator.addMethod("mcreeup", function (value, element) {
    return this.optional(element) || /^[0-9]{3}.[0-9]{3}.[0-9]{2}.[0-9]{3}$/i.test(value);
}, '<p class="text-danger">Este campo debe contener números de la forma: XXX.XXX.XX.XXX.</p>');

$.validator.addMethod("memail", function (value, element) {
    return this.optional(element) || /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i.test(value);
}, '<p class="text-danger">Por favor introduzca una dirección de correo válida.</p>');

$.validator.addMethod("mtext", function (value, element) {
    return this.optional(element) || /^[a-zA-Z0-9.,:'"áéñíóúÁÉÍÚÓ()\ ]+$/i.test(value);
}, '<p class="text-danger">Este campo solo debe contener caracteres alfanuméricos.</p>');

$.validator.addMethod("mplref", function (value, element) {
    return this.optional(element) || /^[0-9\/-]+$/i.test(value);
}, '<p class="text-danger">Este campo no posee un número de referencia válido.</p>');

$.validator.addMethod("mcontrato", function (value, element) {
    return this.optional(element) || /^[0-9/]+$/i.test(value);
}, '<p class="text-info">Este número de contrato no es válido.</p>');

$.validator.addMethod("manno", function (value, element) {
    var today = new Date();
    if (this.optional(element) || /^[0-9]{4}$/i.test(value)) {
        if (Number(value) <= today.getFullYear() && Number(value) >= '2016') {
            return true;
        }
    }
    return false;
}, '<p class="text-danger">Este campo no contiene un año válido.</p>');

$.validator.addMethod("mlicencia", function (value, element) {
    return this.optional(element) || /^[0-9/]{4}$/i.test(value);
}, '<p class="text-info">Este número de contrato no es válido.</p>');

$.validator.addMethod("mpassword", function (value, element) {
    return this.optional(element) ||
        (/^[A-Za-z0-9!@#$%^&*()\/_+:'=?"-><~`.,\\\[\]\{\}]{8,50}$/i.test(value) &&
        /[a-z]/.test(value) &&
        /\d/.test(value));
}, '<p class="text-danger">La contraseña debe contener más de 8 letras y caracteres especiales.</p>');

$.validator.addMethod("mpassword_confirm", function (value, element) {
    return this.optional(element) || $('.mpassword').val() == value;
}, '<p class="text-danger">Las contraseñas no coinciden.</p>');