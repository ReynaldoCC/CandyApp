$(document).ready(function(){
    $("#filter_municipios").on("keyup", function() {
        var value = $(this).val().toLowerCase();
            $("#id_municipios span").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $("#check_all_municipios").on("click", function(){
        $("span:not([style='display: none;']) input[name='municipios']").prop('checked', this.checked);
    });

});
