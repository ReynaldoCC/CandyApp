function abrir_modal(url)
{
        jQuery('#popup').load(url, function()
        {
            jQuery(this).modal('show');
        });
        return false;
}

function cerrar_modal()
{
        jQuery('#popup').modal('hide');
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


