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

var NOmmenclatorList = function () {

        var _initNomenclators = function () {
                $(".dashwidget.overrided").on("click", function () {
                        let a = $(this).find("a.icon-container");
                        window.location.href = a[0].href;
                })
        }

        return {
                init: function () {
                        _initNomenclators();
                }
        }
}();
