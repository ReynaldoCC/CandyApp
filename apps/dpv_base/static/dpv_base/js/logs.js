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


var DPVLog = function () {

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
    const _initLogPane = function (translations) {
        $('#logs-table').DataTable({
            responsive: true,
            order: [ 0, 'asc' ],
            sScrollX: "100%",
            lengthMenu: [20, 35, 50, "All"],
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

    return {
        init: function (translations) {
            _initLogPane(translations);
        },
    };
}();