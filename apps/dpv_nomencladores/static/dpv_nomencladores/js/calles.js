$(document).ready(function(){
    $("#filter_municipios").on("keyup", function() {
        var value = $(this).val().toLowerCase();
            $("#id_municipios span").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $("#check_all_municipios").on("click", function(){
        if ($("#check_all_municipios").prop('checked'))
            $("input[name='municipios']").attr('checked', true);
        else
            $("input[name='municipios']").attr('checked', false);
    });

});
