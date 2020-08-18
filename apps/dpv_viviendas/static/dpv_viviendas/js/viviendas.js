'use strict';

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

    const _initViviendaPane = function (translations) {
        $('#vivienda-table').DataTable({
            responsive: true,
            order: [0, 'desc'],
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
                "search": translations.search,
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

        let $pj_local = $("#id_local_dado").selectize({
            create: false,
            placeholder: "Selecione un local",
            allowEmptyOption: false,
        });

        $.datepicker.regional['es'] = {
            closeText: 'Cerrar',
            prevText: '<Ant',
            nextText: 'Sig>',
            currentText: 'Hoy',
            monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
            'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
            dayNamesShort: ['Dom', 'Lun', 'Mar', 'Mié;', 'Juv', 'Vie', 'Sáb'],
            dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'],
            weekHeader: 'Sm',
            dateFormat: 'dd/mm/yy',
            firstDay: 1,
            isRTL: false,
            endDate: "today",
            maxDate: 0,
            showMonthAfterYear: false,
            yearSuffix: ''
        };
        $.datepicker.setDefaults($.datepicker.regional['es']);
        $('#id_fecha_propietario').datepicker();

        const _fill_selectizes_with_values = function () {
            ($("#id_destino").val())?($pj_destino[0].selectize.setValue($("#id_destino").val())):'';
            ($("#id_propietario").val())?($pj_propietario[0].selectize.setValue($("#id_propietario").val())):'';
            ($("#id_concepto").val())?(pj_concepto[0].selectize.setValue($("#id_concepto").val())):'';
            ($("#id_local_dado").val())?($pj_local[0].selectize.setValue($("#id_local_dado").val())):'';
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
                if(element[0].attributes['type']){
                    if (element[0].attributes['type'].nodeValue === 'select-one' || element[0].attributes['type'].nodeValue === 'select-multiple')
                        error.insertAfter(element.parent());
                    else
                        error.insertAfter(element);
                }
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
				},
                cantidad_persona: {
				    required: true,
				    digits: true,
                    maxlength: 3,
                    min:1,
				},
                cantidad_menores: {
				    required: true,
				    digits: true,
                    maxlength: 2,
                    min: 0,
				},
                cantidad_mujeres: {
				    required: true,
				    digits: true,
                    maxlength: 2,
                    min: 0,
				},
                cantidad_aclifim: {
				    required: true,
				    digits: true,
                    maxlength: 2,
                    min: 0,
				},
                cantidad_anciano: {
				    required: true,
				    digits: true,
                    maxlength: 2,
                    min: 0,
				},
                propietario: {
				    required: true,
				},
                local_dado: {
				    required: true,
				},
                fecha_propietario: {
				    required: true,
				},
                aprobada: {
				    required: false,
				},
                add_concepto: {
				    required: true,
                    maxlength: 500,
				},
			},
			messages: {
				numero: {
				    required: "El número de la vivienda es requerido.",
				    digits: "El número de la vivienda solo puede contener dígitos.",
				},
                destino: {
				    required: "Tiene que seleccionar un destino.",
				},
                cantidad_persona: {
				    required: "La cantidad e personas es requerido.",
				    digits: "La cantidad e personas solo puede contener dígitos.",
                    maxlength: "La cantidad e personas solo puede tener hasta 3 dígitos",
				},
                propietario: {
				    required: "Tiene que seleccionar un propietario.",
				},
                local_dado: {
				    required: "Tiene que seleccionar un local.",
				},
                fecha_propietario:{
                    required: "Tiene que seleccionar una fecha de habitado.",
                },
                add_concepto: {
				    required: "Debe argumentar algo.",
                    maxlength: "Su argumento debe tener hasta 200 caracteres.",
				},
			},
		});

        _fill_selectizes_with_values();
    };

    return {
        init: function (translations) {
            _initViviendaPane(translations);
        },
        initForm: function () {
            vivienda_form = $("#vivienda-form")
            _initViviendaForm();
        },
    }
}();




$(function(){
   $.datepicker.regional['es'] = {
    closeText: 'Cerrar',
    prevText: '<Ant',
    nextText: 'Sig>',
    currentText: 'Hoy',
    monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
    monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
    dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
    dayNamesShort: ['Dom', 'Lun', 'Mar', 'Mié;', 'Juv', 'Vie', 'Sáb'],
    dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'],
    weekHeader: 'Sm',
    dateFormat: 'dd/mm/yy',
    firstDay: 1,
    isRTL: false,

    endDate: "today",
    maxDate: 0,
    showMonthAfterYear: false,
    yearSuffix: ''
    };
    $.datepicker.setDefaults($.datepicker.regional['es']);
   $('.date').datepicker();
});


