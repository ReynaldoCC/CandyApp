"use strict";


var AgreeCalle = function () {

    var _initialize = function () {

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

        $('#form_calle').on('submit', function(event){
            event.preventDefault();
            //console.log("form submitted!")  // sanity check
            if (!$('#form_calle').valid())
                return;
            create_post();
        });

        function create_post() {

            let form_data = $("#form_calle").serialize();
            $.ajax({
                url : "/nomenclador/new_calle/", // the endpoint
                type : "POST", // http method
                data : form_data,
                success : function(json) {
                    console.log(json);
                    $('#id_nombre').val(''); // remove the value from the input
                    let id_select_element = $("#selected[type='hidden']").val();
                    let mun_select = $(':not(#form_calle) select[id$=municipio]');
                    mun_select[0].selectize.setValue(mun_select[0].selectize.getValue());
                    $("#"+id_select_element)[0].selectize.on('load', function() {
                        $("#"+id_select_element)[0].selectize.setValue(json.id);
                    });
                    $('#close_md').click();
                },
                error : function(xhr,errmsg,err) {
                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! Hemos encontrado un error: "+errmsg+
                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                      console.log(xhr);
                    toastr.error(xhr.responseJSON.errmsg.nombre[0], '<h3>Error</h3>');
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });

        }
    };

    return {
        init: function () {

            _initialize();

        }
    }
}();
