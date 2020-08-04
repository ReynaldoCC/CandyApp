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