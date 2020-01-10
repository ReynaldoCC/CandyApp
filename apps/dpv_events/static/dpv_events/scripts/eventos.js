var EventosScript = function () {

    var eventos;
    eventos = function () {

        var tableTema = jQuery('#table_1');
        var temas = [];

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
        }

        function initInput() {
            jQuery("#id_type_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_type_evento").select2({placeholder: "Seleccione el Evento...",allowClear: true,escapeMarkup: function (m) {return m;}});
            jQuery("#id_type_evento-error").remove();
            jQuery("#id_date_programed_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_date_programed_evento-error").remove();
            jQuery("#id_site_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_site_evento-error").remove();
            jQuery("#id_site_evento").maxlength({limitReachedClass: "label label-danger",threshold: 5});
            jQuery("#id_month_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_month_evento").select2({placeholder: "Seleccione el Mes...",allowClear: true,escapeMarkup: function (m) {return m;}});
            jQuery("#id_month_evento-error").remove();
            jQuery("#id_is_extraordinario_evento").attr("checked", false).parent().removeClass("checked");
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

        }
        initInput();

        function initTheme() {
            jQuery("#id_asunto_tema_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_asunto_tema_evento-error").remove();
            jQuery("#id_asunto_tema_evento").maxlength({limitReachedClass: "label label-danger",threshold: 5});
            jQuery("#id_responsable_tema_evento").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
            jQuery("#id_responsable_tema_evento").select2({placeholder: "Seleccione el Responsable...",allowClear: true,escapeMarkup: function (m) {return m;}});
            jQuery("#id_responsable_tema_evento-error").remove();
        }
        initTheme();

        jQuery('#cancelar').click(function () {
            jQuery('#nav-home-tab').click();
        });

        jQuery('#close_theme_event').click(function () {
            jQuery('#cancelar_theme_event').click();
        });

        jQuery('#cancelar_theme_event').click(function () {
            initTheme();
        });

        jQuery('#nav-home-tab').click(function () {
            initInput();
            initTheme();

            tableTema.find('.delete').each(function(){
                jQuery(this).click();
            });

        });


        var form = jQuery('#newevento_form');

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

                var formData = new FormData(jQuery("#newevento_form")[0]);

                for(var i = 0; i < temas.length;i++){
                    formData.append("temas[" + i + "][asunto]",temas[i].asunto);
                    formData.append("temas[" + i + "][responsable_id]",temas[i].responsable_id);
                }

                jQuery.ajax({
                    type: "POST",
                    url: "/dpv_events/create_evento/",
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
                        .closest('.form-group').removeClass('has-error').addClass('has-success');
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

        var table = jQuery('#sample_editable_1');

        tableTema.on('click', '.delete', function (e) {
            e.preventDefault();

            var nRow = jQuery(this).parents('tr')[0];
            delTema(jQuery(this).attr('data-tema'));
            nRow.remove();

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
                data: {"type_id":event.val(),"month":month.val()},
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
            eventos();
        }

    };

}();