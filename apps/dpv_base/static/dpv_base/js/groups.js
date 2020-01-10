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
