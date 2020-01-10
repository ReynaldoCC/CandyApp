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

function desmarcar_otros(id)
{
    if (document.getElementById(id).checked == true) {
        if (id == 'none-radio') {
            document.getElementById('id_use_tls').checked = false;
            document.getElementById('id_use_ssl').checked = false;
        }
        if (id == 'id_use_tls') {
            document.getElementById('none-radio').checked = false;
            document.getElementById('id_use_ssl').checked = false;
        }
        if (id == 'id_use_ssl') {
            document.getElementById('none-radio').checked = false;
            document.getElementById('id_use_tls').checked = false;
        }
    }
}

