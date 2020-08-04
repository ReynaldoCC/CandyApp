var EventoScript = function () {

    var evento;
    evento = function () {

        var tableTema = jQuery('#table_1');
        var tableThemes = jQuery('#table_themes');
        var tableThemesSugeridos = jQuery('#table_themes_sugeridos');
        var temas = [];
        var inform = jQuery('#tab_1_1');
        var infoacta = jQuery('#tab_1_2');
        var tableAcuerdos = jQuery('#table_2');

        function addTema(id,asunto,responsable_id,responsable_name) {

            temas.push({
                "id": id,
                "asunto": asunto,
                "responsable_id": responsable_id,
            });

            tableTema.append('<tr>' +
                '<td>' + id + '</td>' +
                '<td>' + asunto + '</td>' +
                '<td>' + responsable_name + '</td>' +
                '<td><button class="delete btn btn-xm default" type="button" data-tema="' + id + '"><i class="fa fa-trash-o"></i></button></td>' +
                '</tr>');
        }

        function delTema(id) {
            for(var i = 0; i < temas.length; i++){
                if(temas[i].id == id){
                    temas.splice(i,1);
                }
            }

            // borrar la fila de la tabla
        }

        function setInput() {
            jQuery("#id_type_evento").val(model.type).closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_type_evento").select2({placeholder: "Seleccione el Evento...",allowClear: true,escapeMarkup: function (m) {return m;}});
            jQuery("#id_type_evento-error").remove();
            jQuery("#id_date_programed_evento").val(model.date_programed).closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_date_programed_evento-error").remove();
            jQuery("#id_site_evento").val(model.site).closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_site_evento-error").remove();
            jQuery("#id_site_evento").maxlength({limitReachedClass: "label label-danger",threshold: 5});
            jQuery("#id_month_evento").val(model.month).closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_month_evento").select2({placeholder: "Seleccione el Mes...",allowClear: true,escapeMarkup: function (m) {return m;}});
            jQuery("#id_month_evento-error").remove();
            var is_extraordinario = model.is_extraordinario ? jQuery("#id_is_extraordinario_evento").attr("checked", true).parent().addClass("checked") : jQuery("#id_is_extraordinario_evento").attr("checked", false).parent().removeClass("checked");
            if (jQuery().datepicker) {jQuery(".date-picker").datepicker({rtl: true,orientation: "left", autoclose: true, language: "es"});}

            jQuery(".form_meridian_datetime").datetimepicker({
                isRTL: true,
                format: "yyyy-mm-dd hh:ii",
                showMeridian: true,
                autoclose: true,
                pickerPosition: (true ? "bottom-right" : "bottom-left"),
                todayBtn: true,
                startDate: new Date(),
                language: "es",
            });

            tableTema.find('.delete').each(function(){
                jQuery(this).click();
            });

            for(theme of model.themes){
                addTema(theme.id,theme.asunto,theme.responsable_id,theme.responsable_name)
            }

        }
        setInput();

        function initTheme() {
            jQuery("#id_asunto_tema_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_asunto_tema_evento-error").remove();
            jQuery("#id_asunto_tema_evento").maxlength({limitReachedClass: "label label-danger",threshold: 5});
            jQuery("#id_responsable_tema_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_responsable_tema_evento").select2({placeholder: "Seleccione el Responsable...",allowClear: true,escapeMarkup: function (m) {return m;}});
            jQuery("#id_responsable_tema_evento-error").remove();
        }
        initTheme();

        function initThemeSugerido() {
            jQuery("#id_asunto_tema_sugerido_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_asunto_tema_sugerido_evento-error").remove();
            jQuery("#id_asunto_tema_sugerido_evento").maxlength({limitReachedClass: "label label-danger",threshold: 5});
        }
        initThemeSugerido();

        function initActa() {
            jQuery("#id_body_acta_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_body_acta_evento-error").remove();
        }
        initActa();

        function initAcuerdo() {
            jQuery("#id_asunto_acuerdo_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_asunto_acuerdo_evento-error").remove();
            jQuery("#id_asunto_acuerdo_evento").maxlength({limitReachedClass: "label label-danger",threshold: 5});
            jQuery("#id_date_finish_acuerdo_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_date_finish_acuerdo_evento-error").remove();
            jQuery("#id_responsables_acuerdo_evento").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery('#id_responsables_acuerdo_evento').select2({placeholder: "Seleccione los Responsables",allowClear: true});
            jQuery("#id_responsables_acuerdo_evento-error").remove();

            jQuery('#id_date_finish_acuerdo_evento').datepicker({
                rtl: false,
                format: 'yyyy-mm-dd',
                orientation: "left",
                autoclose: true,
                language: "es",
            });
        }
        initAcuerdo();

        jQuery('#cancelar').click(function () {
            jQuery('#nav-home-tab').click();
        });

        jQuery('#close_theme_event').click(function () {
            jQuery('#cancelar_theme_event').click();
        });

        jQuery('#cancelar_theme_event').click(function () {
            initTheme();
        });

        jQuery('#close_theme_sugerido').click(function () {
            jQuery('#cancelar_theme_sugerido').click();
        });

        jQuery('#cancelar_theme_sugerido').click(function () {
            initThemeSugerido();
        });

        jQuery('#close_acta_evento').click(function () {
            jQuery('#cancelar_acta_evento').click();
        });

        jQuery('#cancelar_acta_evento').click(function () {
            initActa();
        });

        jQuery('#close_acuerdo_evento').click(function () {
            jQuery('#cancelar_acuerdo_evento').click();
        });

        jQuery('#cancelar_acuerdo_evento').click(function () {
            initAcuerdo();
        });

        jQuery('#to_info_evento').click(function () {

            setInput();
            initTheme();

        });

        var form = jQuery('#editevento_form');

        form.validate({
            doNotHideMessage: true,
            errorElement: 'span',
            errorClass: 'help-block help-block-error',
            focusInvalid: false,

            rules: {
                user_evento: {required: true,},
                type_evento: {required: true,},
                date_programed_evento: {required: true,date: true},
                site_evento: {required: true,},
                month_evento: {required: true,digits: true,},
                is_extraordinario_evento: {required: false,},

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

                if(temas.length == 0){
                    alert('Debe añadir al menos otro tema.');
                    return;
                }

                var formData = new FormData(jQuery("#editevento_form")[0]);
                formData.append("id",model.id);

                for(var i = 0; i < temas.length;i++){
                    formData.append("temas[" + i + "][asunto]",temas[i].asunto);
                    formData.append("temas[" + i + "][responsable_id]",temas[i].responsable_id);
                }

                jQuery.ajax({
                    type: "POST",
                    url: "/dpv_events/update_evento/",
                    data: formData,
                    contentType: false,
                    processData: false,
                    success: function (data) {
                        model.set(data.event);

                        inform.find('.type_evento').each(function () {
                            jQuery(this).html(data.event.type.type.toUpperCase());
                        });
                        // PONER EL FORMATO BIEN
                        inform.find('.date_programed_evento').each(function () {
                            jQuery(this).html(data.event.get_date_programed);
                        });

                        inform.find('.time_programed_evento').each(function () {
                            jQuery(this).html(data.event.time_programed);
                        });
                        // FIN DEL FORMATO QUE NECESITO
                        inform.find('.site_evento').each(function () {
                            jQuery(this).html(data.event.site.toUpperCase());
                        });

                        inform.find('.month_evento').each(function () {
                            jQuery(this).html(data.event.get_month.toUpperCase());
                        });

                        inform.find('.is_extraordinario_evento').each(function () {
                            jQuery(this).html(data.event.get_is_extraordinario.toUpperCase());
                        });

                        tableThemes.html('');
                        for(theme of model.themes){
                            tableThemes.append('<tr><td>' + theme.id + '</td><td>' + theme.asunto + '</td><td>' + theme.responsable_name + '</td></tr>');
                        }

                        jQuery('#cancelar').click();
                        alert('Se Ha Modificado Exitosamente El Evento.');
                    },
                });

            }

        });

        var form_tema = jQuery('#newtheme_event_form');

        form_tema.validate({
            doNotHideMessage: true,
            errorElement: 'span',
            errorClass: 'help-block help-block-error',
            focusInvalid: false,

            rules: {
                asunto_tema_evento: {
                    required: true
                },
                responsable_tema_evento: {
                    required: true
                },
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
                        .closest('.form-group').removeClass('has-error').addClass('has-success'); // set success class to the control group
            },

            submitHandler: function (form) {
                var id = jQuery('#table_1 tbody').find('tr').length + 1;
                var asunto = jQuery('#id_asunto_tema_evento').val();
                var responsable_id = jQuery('#id_responsable_tema_evento').val();
                var responsable_name = jQuery('#id_responsable_tema_evento').text();
                addTema(id,asunto,responsable_id,responsable_name);
                jQuery('#cancelar_theme_event').click();
            }

        });

        var form_tema_sugerido = jQuery('#newtheme_sugerido_form');

        form_tema_sugerido.validate({
            doNotHideMessage: true,
            errorElement: 'span',
            errorClass: 'help-block help-block-error',
            focusInvalid: false,

            rules: {
                asunto_tema_sugerido_evento: {
                    required: true
                },
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
                        .closest('.form-group').removeClass('has-error').addClass('has-success'); // set success class to the control group
            },

            submitHandler: function (form) {

                var formData = new FormData(jQuery("#newtheme_sugerido_form")[0]);
                formData.append("event_id",model.id);

                jQuery.ajax({
                    type: "POST",
                    url: "/dpv_events/create_temaevento/",
                    data: formData,
                    contentType: false,
                    processData: false,
                    success: function(data){
                        setTimeout(function() {
                            jQuery(location).attr('href',"");
                        }, 0);
                    }
                });

            }

        });

        var form_acta_evento = jQuery('#newacta_evento_form');

        form_acta_evento.validate({
            doNotHideMessage: true,
            errorElement: 'span',
            errorClass: 'help-block help-block-error',
            focusInvalid: false,

            rules: {
                body_acta_evento: {
                    required: true
                },
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
                        .closest('.form-group').removeClass('has-error').addClass('has-success'); // set success class to the control group
            },

            submitHandler: function (form) {

                var formData = new FormData(jQuery("#newacta_evento_form")[0]);
                formData.append("event_id",model.id);

                jQuery.ajax({
                    type: "POST",
                    url: "/dpv_events/create_acta/",
                    data: formData,
                    contentType: false,
                    processData: false,
                    success: function(data){
                        setTimeout(function() {
                            jQuery(location).attr('href',"");
                        }, 0);
                    }
                });

            }

        });

        var form_acuerdo_evento = jQuery('#newacuerdo_evento_form');

        form_acuerdo_evento.validate({
            doNotHideMessage: true,
            errorElement: 'span',
            errorClass: 'help-block help-block-error',
            focusInvalid: false,

            rules: {
                asunto_acuerdo_evento: {
                    required: true
                },
                date_finish_acuerdo_evento: {
                    required: true
                },
                responsables_acuerdo_evento: {
                    required: true
                },
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
                        .closest('.form-group').removeClass('has-error').addClass('has-success'); // set success class to the control group
            },

            submitHandler: function (form) {

                var formData = new FormData(jQuery("#newacuerdo_evento_form")[0]);
                formData.append("event_id",model.id);

                jQuery.ajax({
                    type: "POST",
                    url: "/dpv_events/create_acuerdo/",
                    data: formData,
                    contentType: false,
                    processData: false,
                    success: function(data){

                        setTimeout(function() {
                            jQuery(location).attr('href',"");
                        }, 0);
                    }
                });

            }

        });

        tableTema.on('click', '.delete', function (e) {
            e.preventDefault();

            var nRow = jQuery(this).parents('tr')[0];
            delTema(jQuery(this).attr('data-tema'));
            nRow.remove();

        });

        tableThemesSugeridos.on('click', '.done', function (e) {

            var input = jQuery(this);

            jQuery.ajax({
                type: "POST",
                url: "/dpv_events/aprobar_temaevento/",
                data: {"theme_id":input.attr('data-theme')},
                success: function(data){
                    setTimeout(function() {
                            jQuery(location).attr('href',"");
                    }, 0);
                }
            });
        });

        function verify_event () {
            var month = jQuery('#id_month_evento');
            var event = jQuery('#id_type_evento');
            var is_extraordinario = jQuery('#id_is_extraordinario_evento');

            if(event.val() === ""){
                is_extraordinario.attr("disabled", false);
                return;
            }

            if (month.val() === "") {
                is_extraordinario.attr("disabled", false);
                return;
            }

            month.attr("readonly", true).attr("disabled", true);

            jQuery.ajax({
                type: "POST",
                url: "/dpv_events/verify_evento/",
                data: {"type_id":event.val(),"month":month.val(), "event_id": model.id},
                success: function(data){
                    month.attr("readonly", false).attr("disabled", false);

                    if(data.exist){
                        alert('Para El Mes Seleccionado Existe Un(a) "' + data.type + '" Ordinario.');
                        is_extraordinario.attr("checked", true).attr("disabled", true);
                    }
                    if(!data.exist){
                        is_extraordinario.attr("disabled", false);
                    }
                },
                error: function(jqXHR){
                    month.attr("readonly", false).attr("disabled", false).removeClass("spinner");
                }
            });
        }

        jQuery('#id_month_evento').on('change',function(){
            verify_event();
        });

        jQuery('#id_type_evento').on('change',function(){
            verify_event();
        });

    };

    return {

        init: function () {
            evento();
        }

    };

}();