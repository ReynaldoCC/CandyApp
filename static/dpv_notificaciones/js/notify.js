"use strict";


const Notifies = function () {
    let notify_item;
    let alert_notify = false;
    let alert_error_notifies = false;

    let _make_alert = function (type, text) {
        Swal.fire({
            position: 'top-end',
            icon: type || 'success',
            title: text || 'Your work has been saved',
            showConfirmButton: false,
            timer: 2500
        })
    }
    let _init = function (url) {
        notify_item = jQuery(".notify-nav-icon");

        let _success_notifies = function (json) {
            if (json.news > 0){
                notify_item.removeClass("hide");
                if (!alert_notify) {
                    alert_notify = true;
                    _make_alert("success", "Tiene nuevas notificaciones sin ver");
                }
            } else {
                notify_item.addClass("hide");
                alert_notify = false;
            }
        };
        let _error_notifies = function (xhr,errmsg,err) {
            console.log("Ocurrio error al intentar obtener las notificaciones", xhr,errmsg,err);
            if (!alert_error_notifies){
                alert_error_notifies = true;
                _make_alert("error", "No se pudieron obetner al notificaciones por un error");
            }
            notify_item.addClass("hide");
        };
        let _have_news = function () {
            jQuery.ajax({
                url: url,
                type: "get",
                success: _success_notifies,
                error: _error_notifies,
            });
            return true;
        }
        if (notify_item && url) {
            setInterval(function () {_have_news()}, 30000);
        }
    };
    let _initList = function (translations) {

    }
    return {
        init: function (url) {
            _init(url);
        },
        initList: function (translations) {
            _initList();
        }
    }
}();