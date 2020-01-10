$(document).ready(function(){
    $("#filter_groups").on("keyup", function() {
        var value = $(this).val().toLowerCase();
            $("#id_groups span").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $("#filter_user_permissions").on("keyup", function() {
        var value = $(this).val().toLowerCase();
            $("#id_user_permissions span").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $("#check_all_groups").on("click", function(){
        if ($("#check_all_groups").prop('checked'))
            $("input[name='groups']").attr('checked', true);
        else
            $("input[name='groups']").attr('checked', false);
    });
    $("#check_all_user_permissions").on("click", function(){
       if ($("#check_all_user_permissions").prop('checked')) {
            $("input[name='user_permissions']").attr('checked', true);
        }else
            $("input[name='user_permissions']").attr('checked', false);
    });
});

function create_calle()
{
    console.log("creating calle");
}

function abrir_modal(url, id=null)
{
    $('#add_calle').load(url, function(id)
    {
        $(this).modal('show');
    });
    return false;
}

function cerrar_modal()
{
    $('#add_calle').modal('hide');
    return false;
}