'use strict';

function abrir_modal(url, id=null)
{
    $('#popup').load(url, function(id)
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

var DPVDocumento = function () {
    var form_setdatemodal;

    var initTable = function () {
        let table = $('#doc-table').DataTable({
            responsive: true,
            order: [ 0, 'desc' ],
            sScrollX: "100%",
            fixedColumns:   {
                leftColumns: 2,
                rightColumns: 1,
            },
            language: {
                "decimal": "",
                "emptyTable": "No hay Documentos que mostrar",
                "info": "Mostrando _START_ a _END_ de _TOTAL_ Documentos",
                "infoEmpty": "Mostrando 0 a 0 de 0 Documentos",
                "infoFiltered": "(Filtrado de _MAX_ total documentos)",
                "infoPostFix": "",
                "thousands": ",",
                "lengthMenu": "Mostrar _MENU_ Documentos",
                "loadingRecords": "Cargando...",
                "processing": "Procesando...",
                "search": "Buscar...",
                "zeroRecords": "Sin documentos coincidentes encontrados",
                "paginate": {
                        "first": "Primero",
                        "last": "Ultimo",
                        "next": "Siguiente",
                        "previous": "Anterior"
                }
            },
        });
        $('button.toggle-column').on( 'click', function (e) {
            e.preventDefault();
            $(this).toggleClass('btn-secondary').toggleClass('btn-outline-secondary');
            let column = table.column( $(this).attr('data-column') );
            column.visible( ! column.visible() );
        });
    };

    var initInputSetDateModal = function () {
        $("#id_fecha_entrega").val("").closest(".form-group").removeClass("has-success").closest(".form-group").removeClass("has-error");
        $("#id_fecha_entrega-error").remove();
        $("#id_fecha_entrega").datetimepicker({
            isRTL: true,
            format: "yyyy-mm-dd hh:ii",
            showMeridian: true,
            autoclose: true,
            pickerPosition: (true ? "bottom-right" : "bottom-left"),
            todayBtn: true,
            startDate: new Date(),
            language: "es",
        });
    };

    var initValidateSetDateModal = function () {

        form_setdatemodal.validate({

            errorClass: 'text-danger',

            highlight: function(element) {
                $(element).addClass('is-invalid');
            },

            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },
            // Validate only visible fields
			ignore: ":hidden:not([class~=selectized]),:hidden > .selectized, .selectize-control .selectize-input input",

			errorPlacement: function(error, element) {
                error.insertAfter(element);
            },

            rules: {
                'fecha_entrega': {
                    required: true,
                },
            },
        });

    };

    return {
        init: function () {

            initTable();

        },

        initSetDateModal: function () {
            form_setdatemodal = $('#formodal_setdate');

            initInputSetDateModal();

            initValidateSetDateModal();

        }

    };

}();

jQuery(document).ready(function() {
    DPVDocumento.init();
});