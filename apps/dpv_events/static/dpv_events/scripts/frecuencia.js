var FrecuenciaScript = function () {

    var frecuencia;
    frecuencia = function () {

        var id = null;

        var initInput = function (){
            jQuery("#id_name_frecuencia").val("").removeClass("is-valid").removeClass("is-invalid");
            jQuery("#id_name_frecuencia-error").remove();
            jQuery("#id_name_frecuencia").maxlength({limitReachedClass: "label label-danger",threshold: 5});
            jQuery("#id_days_frecuencia").val("").removeClass("is-valid").removeClass("is-invalid");
            jQuery("#id_days_frecuencia-error").remove();
        };
        initInput();

        jQuery('#cancelar').click(function () {
            initInput();
        });

        var form = jQuery('#newfrecuencia_form');

        form.validate({
            doNotHideMessage: true,
            errorElement: 'span',
            errorClass: 'help-block help-block-error',
            focusInvalid: false,

            rules: {
                name_frecuencia: {required: true,},
                days_frecuencia: {required: true,digits: true,},
            },

            errorPlacement: function (error, element) {
                error.insertAfter(element);
            },

            highlight: function (element) {
                jQuery(element).removeClass('is-valid').addClass('is-invalid');
            },

            unhighlight: function (element) {
                jQuery(element).removeClass('is-invalid');
            },

            success: function (label, element) {
                jQuery(element).removeClass('is-invalid').addClass('is-valid');
            },

            submitHandler: function (form) {

                var form = jQuery("#newfrecuencia_form");
                var formData = new FormData(form[0]);

                if(form.hasClass('agregar')){
                    jQuery.ajax({
                        type: "POST",
                        url: "/dpv_events/create_frecuencia/",
                        data: formData,
                        contentType: false,
                        processData: false,
                        success: function (data) {

                            setTimeout(function() {
                                jQuery(location).attr('href',"");
                            }, 0);

                        },
                    });
                }

                if(form.hasClass('modificar')){
                    formData.append("id",id);

                    jQuery.ajax({
                        type: "POST",
                        url: "/dpv_events/update_frecuencia/",
                        data: formData,
                        contentType: false,
                        processData: false,
                        success: function (data) {

                            setTimeout(function() {
                                jQuery(location).attr('href',"");
                            }, 0);

                        },
                    });
                }

            }

        });

        var table = jQuery('#sample_editable_1');

        jQuery('#btn_create_frecuencia').on('click',function(){
            id = null;
            if(!jQuery("#newfrecuencia_form").hasClass('agregar')){
                jQuery("#newfrecuencia_form").removeClass('modificar').addClass('agregar');
            }
            jQuery('#form_frecuencia').find('.action_frecuencia').each(function(){
                jQuery(this).html('agregar');
            });
        });

        table.on('click','.edit',function(){
            var model = jQuery(this);
            id = model.attr('data-id');
            if(jQuery("#newfrecuencia_form").hasClass('agregar')){
                jQuery("#newfrecuencia_form").removeClass('agregar').addClass('modificar');
            }
            jQuery('#form_frecuencia').find('.action_frecuencia').each(function(){
                jQuery(this).html('modificar');
            });
            jQuery('#id_name_frecuencia').val(model.attr('data-name'));
            jQuery('#id_days_frecuencia').val(model.attr('data-days'));
        });

    };

    return {

        init: function () {
            frecuencia();
        }

    };

}();