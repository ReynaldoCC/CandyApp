var TipoEventoScript = function () {

    var tipoevento;
    tipoevento = function () {

        var id = null;

        function initInput(){
            jQuery("#id_type_tipoevento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_type_tipoevento-error").remove();
            jQuery("#id_type_tipoevento").maxlength({limitReachedClass: "label label-danger",threshold: 5});
            jQuery("#id_frecuencia_tipoevento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_frecuencia_tipoevento").select2({placeholder: "Seleccione Frecuencia...",allowClear: true,escapeMarkup: function (m) {return m;}});
            jQuery("#id_frecuencia_tipoevento-error").remove();
        };
        initInput();

        jQuery('#close').click(function () {
            jQuery('#cancelar').click();
        });

        jQuery('#cancelar').click(function () {
            initInput();
        });

        var form = jQuery('#newtipoevento_form');

        form.validate({
            doNotHideMessage: true,
            errorElement: 'span',
            errorClass: 'help-block help-block-error',
            focusInvalid: false,

            rules: {
                type_tipoevento: {required: true,},
                frecuencia_tipoevento: {required: false,},
                
            },

            errorPlacement: function (error, element) {
                error.insertAfter(element);
            },

            highlight: function (element) {
                jQuery(element)
                    .closest('.form-group').removeClass('has-success').addClass('has-error');
            },

            unhighlight: function (element) {
                jQuery(element)
                    .closest('.form-group').removeClass('has-error');
            },

            success: function (label, element) {
                label
                        .addClass('valid')
                        .closest('.form-group').removeClass('has-error').addClass('has-success');
            },

            submitHandler: function (form) {

                var form = jQuery("#newtipoevento_form");
                var formData = new FormData(form[0]);

                if(form.hasClass('agregar')){
                    jQuery.ajax({
                        type: "POST",
                        url: "/dpv_events/create_tipoevento/",
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
                        url: "/dpv_events/update_tipoevento/",
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
        
        jQuery('#btn_create_tipoevento').on('click',function(){
            id = null;
            if(!jQuery("#newtipoevento_form").hasClass('agregar')){
                jQuery("#newtipoevento_form").removeClass('modificar').addClass('agregar');
            }
            jQuery('#form_tipoevento').find('.action_tipoevento').each(function(){
                jQuery(this).html('agregar');
            });
        });
        
        table.on('click','.edit',function(){
            var model = jQuery(this);
            id = model.attr('data-id');
            if(jQuery("#newtipoevento_form").hasClass('agregar')){
                jQuery("#newtipoevento_form").removeClass('agregar').addClass('modificar');
            }
            jQuery('#form_tipoevento').find('.action_tipoevento').each(function(){
                jQuery(this).html('modificar');
            });
            jQuery('#id_type_tipoevento').val(model.attr('data-type'));
            jQuery('#id_frecuencia_tipoevento').val(model.attr('data-frecuencia'));
            jQuery("#id_frecuencia_tipoevento").select2({placeholder: "Seleccione Frecuencia...",allowClear: true,escapeMarkup: function (m) {return m;}});
        });

    };

    return {

        init: function () {
            tipoevento();
        }

    };

}();