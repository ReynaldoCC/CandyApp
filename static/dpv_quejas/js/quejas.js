'use strict';

function abrir_modal(url, id=null)
{
    $('#popup').load(url, function(id)
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

var DPVQuejas = function () {
    var queja_form;
    var asigne_form;
    var response_form;
    var personas;
    var persona;
    var tmp;


    var _makeAlert = function(type, text, success, negate, title=null, accept=null, cancel=null, plus=null) {
        let dataplus = plus || tmp;
        Swal.fire({
            title: title || "Error",
            html: text,
            icon: type,
            showCloseButton: true,
            showCancelButton: true,
            focusConfirm: false,
            confirmButtonText: accept || '<i class="fa fa-thumbs-up"></i> Si',
            confirmButtonAriaLabel: 'Correto',
            cancelButtonText: cancel || '<i class="fa fa-thumbs-down"></i> No',
            cancelButtonAriaLabel: 'Cancelar',
            showClass: {
                popup: 'animated fadeInDown faster',
            },
            hideClass: {
                popup: 'animated fadeOutUp faster',
            },
        }).then((result) => {
            if (result.value) {
                if (success != null) {
                    if (typeof(success) == 'function')
                        success(dataplus);
                };
            } else {
                if (negate != null) {
                    negate(dataplus);
                };
            };
        });
    };
    var _initQuejas = function () {

    };
    var _initTabWizard = function () {
        var prev_button = $('#previous_tab');
        var next_button = $('#next_tab');
        var submit_button = $('button[type="submit"].pull-right.btn.btn-primary');
        var tab_list = $('ul#myTab li.nav-item');
        var first_tab = $('ul#myTab li.nav-item:first');
        var last_tab = $('ul#myTab li.nav-item:last');
        var content_list = $('div#myTabContent.tab-content div.tab-pane');
        var sumary_container = $("#queja_sumary");
        var empty_sumary_msg = "No existe ninguna infomación agregada sobre la queja, Por favor vuelva a los pasos anteriores e ingrese la información necesaria.";
        var empty_procedence_msg = "No existe información sobre la procedencia de la queja. Para agregar dicha información dirijace a la primera pestaña o haga <a href='' class='back-link ref_procedence'>click aquí</a>.";
        var empty_quejoso_msg = "No existe información referente a quien se queja. Si la queja es de procedencia anónima configurelo así en la <a href='' class='back-link ref_procedence'>pestaña procedencia</a>, sino haga <a href='' class='back-link ref_quejoso'>click aqui</a> para rellenar los datos sobre quien realiza la queja."
        var empty_queja_msg = "No existe información sobre la queja como tal dirijace a la <a href='' class='back-link ref_queja'>pestaña Queja</a> para ingresar dichos datos o haga <a href='' class='back-link ref_queja'>click aquí</a>"

        $('#procedencia_tab').on('click', function (e) {
//            if (!queja_form.valid()) {
//                e.preventDefault();
//            };
            _disableOrEnablePNButton($(this));
        });
        $('#aquejado_tab').on('click', function (e) {
//            if (!queja_form.valid()) {
//                e.preventDefault();
//            };
            _disableOrEnablePNButton($(this));

        });
        $('#queja_tab').on('click', function (e) {
//            if (!queja_form.valid()) {
//                e.preventDefault();
//            };
            _disableOrEnablePNButton($(this));
        });
        $('#sumario_tab').on('click', function (e) {
//            if (!queja_form.valid()) {
//                e.preventDefault();
//            };
            _makeSumary();
            _disableOrEnablePNButton($(this));
        });
        $('#previous_tab').on('click', function (e) {
//            if (!queja_form.valid()) {
//                 return e.preventDefault();
//            };
            let current_tab = $('ul#myTab li.nav-item.active');
            current_tab.find('a.nav-link').removeClass('active show');
            let previous_tab = $('ul#myTab li.nav-item.active').prev("ul#myTab li.nav-item");
            //console.log(previous_tab.find('a.nav-link')[0].hash);
            //let conten_id = previous_tab.find('a.nav-link')[0].attributes['aria-controls'].value;
            let conten_selector = previous_tab.find('a.nav-link')[0].hash;
            previous_tab.find('a.nav-link').click();
            previous_tab.find('a.nav-link').addClass('active show');
            content_list.removeClass('active show in');
            $(conten_selector).addClass('active show in');
            if (previous_tab[0] === first_tab[0]) {
                prev_button.addClass('disabled');
            }
            if (next_button.hasClass('disabled')) {
                next_button.removeClass('disabled');
            }
        });
        $('#next_tab').on('click', function (e) {
            let current_tab = $('ul#myTab.nav.nav-tabs.row li.nav-item.active');
            current_tab.find('a.nav-link').removeClass('active show');
//            console.log('current', current_tab);
            let next_tab = $('ul#myTab li.nav-item.active').next("ul#myTab li.nav-item");
            next_tab.find('a.nav-link').click();
            next_tab.find('a.nav-link').addClass('active show');
            let conten_selector = next_tab.find('a.nav-link')[0].hash;
            content_list.removeClass('active show in');
            $(conten_selector).addClass('active show in');
            if (next_tab[0] == last_tab[0]) {
                next_button.addClass('disabled');
            }
            if (prev_button.hasClass('disabled')) {
                prev_button.removeClass('disabled');
            }
            //console.log(next_button);
        });
        $(".ref_procedence").on('click', function (e) {
            e.preventDefault();
            $('#procedencia_tab').trigger('click');
        });
        $(".ref_quejoso").on('click', function (e) {
            e.preventDefault();
            $('#aquejado_tab').trigger('click');
        });
        $(".ref_queja").on('click', function (e) {
            e.preventDefault();
            $('#queja_tab').trigger('click');
        });
        $("#id_queja-tipo_procedencia").on('change', function (e) {
            _toggleProcedenciaForms(true);
        });
        $("#id_queja-damnificado_not_indb").on('change', function (e) {
            $("#id_queja-same_address").click();
            if (this.checked) {
                $("#is_indb").addClass('no-show');
                $("#not_indb").removeClass('no-show');
                $q_cpopular[0].selectize.clear();
                $q_genero[0].selectize.clear();
                $q_direccion_calle[0].selectize.clear();
                $q_direccion_entrecalle1[0].selectize.clear();
                $q_direccion_entrecalle2[0].selectize.clear();
                $q_municipio[0].selectize.clear();
                $q_cpopular[0].selectize.clear();
                $("#id_person_queja-ci").val('');
                $("#id_person_queja-nombre").val('');
                $("#id_person_queja-apellidos").val('');
                $("#id_person_queja-email_address").val('');
                $("#id_person_queja-telefono").val('');
                $("#id_person_queja-movil").val('');
                $("#id_person_queja-direccion_numero").val('');
            } else {
                $("#is_indb").removeClass('no-show');
                $("#not_indb").addClass('no-show');
                $("#id_personas_list")[0].selectize.clear();
            };
        });
        $("#id_queja-same_address").on('change', function (e) {
            //alert(this.checked);
            if ($("#id_queja-damnificado_not_indb")[0].checked) {
                if (this.checked) {
                    $dir_calle[0].selectize.setValue($("#id_person_queja-direccion_calle").val(), false);
                    $dir_entrecalle1[0].selectize.setValue($("#id_person_queja-direccion_entrecalle1").val(), false);
                    $dir_entrecalle2[0].selectize.setValue($("#id_person_queja-direccion_entrecalle2").val(), false);
                    $dir_municipio[0].selectize.setValue($("#id_person_queja-municipio").val(), false);
                    $dir_cpopular[0].selectize.setValue($("#id_person_queja-cpopular").val(), false);
                    $("#id_queja-dir_num").val($("#id_person_queja-direccion_numero").val());
                } else {
                    $dir_calle[0].selectize.setValue('', false);
                    $dir_entrecalle1[0].selectize.setValue('', false);
                    $dir_entrecalle2[0].selectize.setValue('', false);
                    $dir_municipio[0].selectize.setValue('', false);
                    $dir_cpopular[0].selectize.setValue('', false);
                    $("#id_queja-dir_num").val('');
                }
            } else {
                if (this.checked) {
                    _setValuesAddressQueja();
                    //_getPersonData($('#id_personas_list').val());
                } else {
                    $dir_calle[0].selectize.setValue('', false);
                    $dir_entrecalle1[0].selectize.setValue('', false);
                    $dir_entrecalle2[0].selectize.setValue('', false);
                    $dir_municipio[0].selectize.setValue('', false);
                    $dir_cpopular[0].selectize.setValue('', false);
                    $("#id_queja-dir_num").val('');
                } ;
            }
        });
        $("#id_personas_list").on('change', function (e) {
            _loadPersonData(this.value);
        });

        var $pj_municipio = $("#id_empresa-municipio").selectize({
            create: false,
            placeholder: "Selecione un municipio",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $.ajax({
                    url: '/nomenclador/consejopopular/filter/' + value,
                    success: function(results) {
                        let current_value = $pj_cpopular[0].selectize.getValue();
                        let exist = false;
                        for (let i = 0; i < results.length; i++)
                            if (results[i].id == current_value) {
                                exist = true;
                            }
                        if (!exist)
                        $pj_cpopular[0].selectize.clear();
                        $pj_cpopular[0].selectize.clearOptions();
                        $pj_cpopular[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
                $.ajax({
                    url: '/nomenclador/calle/filter/' + value,
                    success: function(results) {
                        let current_value1 = $pj_direccion_calle[0].selectize.getValue();
                        let current_value2 = $pj_direccion_entrecalle1[0].selectize.getValue();
                        let current_value3 = $pj_direccion_entrecalle2[0].selectize.getValue();
                        let exist1, exist2, exist3 = false;
                        for (let i = 0; i < results.length; i++) {
                            if (results[i].id == current_value1) {
                                exist1 = true;
                            }
                            if (results[i].id == current_value2) {
                                exist2 = true;
                            }
                            if (results[i].id == current_value3) {
                                exist3 = true;
                            }
                        }
                        if (!exist1)
                        $pj_direccion_calle[0].selectize.clear();
                        $pj_direccion_calle[0].selectize.clearOptions();
                        $pj_direccion_calle[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist2)
                            $pj_direccion_entrecalle1[0].selectize.clear();
                        $pj_direccion_entrecalle1[0].selectize.clearOptions();
                        $pj_direccion_entrecalle1[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist3)
                            $pj_direccion_entrecalle2[0].selectize.clear();
                        $pj_direccion_entrecalle2[0].selectize.clearOptions();
                        $pj_direccion_entrecalle2[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
            },
        });
        var $pj_cpopular = $("#id_empresa-cpopular").selectize({
            placeholder: "Selecione un Consejo Popular",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pj_direccion_calle = $("#id_empresa-direccion_calle").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pj_direccion_entrecalle2 = $("#id_empresa-direccion_entrecalle2").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $pj_direccion_entrecalle1 = $("#id_empresa-direccion_entrecalle1").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $tipo_procedencia = $("#id_queja-tipo_procedencia").selectize({
            create: false,
            placeholder: "Selecione una tipo de procedencia",
            allowEmptyOption: false,
        });
        var $aq_genero = $("#id_person_procedence-genero").selectize({
            create: false,
            placeholder: "Selecione un género",
            allowEmptyOption: false,
        });
        var $aq_direccion_calle = $("#id_person_procedence-direccion_calle").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $aq_direccion_entrecalle1 = $("#id_person_procedence-direccion_entrecalle1").selectize({
            placeholder: "Selecione un ",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $aq_direccion_entrecalle2 = $("#id_person_procedence-direccion_entrecalle2").selectize({
            placeholder: "Selecione un ",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $aq_municipio = $("#id_person_procedence-municipio").selectize({
            create: false,
            placeholder: "Selecione un municipio",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $.ajax({
                    url: '/nomenclador/consejopopular/filter/' + value,
                    success: function(results) {
                        let current_value = $aq_cpopular[0].selectize.getValue();
                        let exist = false;
                        for (let i = 0; i < results.length; i++)
                            if (results[i].id == current_value) {
                                exist = true;
                            }
                        if (!exist)
                        $aq_cpopular[0].selectize.clear();
                        $aq_cpopular[0].selectize.clearOptions();
                        $aq_cpopular[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
                $.ajax({
                    url: '/nomenclador/calle/filter/' + value,
                    success: function(results) {
                        let current_value1 = $aq_direccion_calle[0].selectize.getValue();
                        let current_value2 = $aq_direccion_entrecalle1[0].selectize.getValue();
                        let current_value3 = $aq_direccion_entrecalle2[0].selectize.getValue();
                        let exist1, exist2, exist3 = false;
                        for (let i = 0; i < results.length; i++) {
                            if (results[i].id == current_value1) {
                                exist1 = true;
                            }
                            if (results[i].id == current_value2) {
                                exist2 = true;
                            }
                            if (results[i].id == current_value3) {
                                exist3 = true;
                            }
                        }
                        if (!exist1)
                            $aq_direccion_calle[0].selectize.clear();
                        $aq_direccion_calle[0].selectize.clearOptions();
                        $aq_direccion_calle[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist2)
                            $aq_direccion_entrecalle1[0].selectize.clear();
                        $aq_direccion_entrecalle1[0].selectize.clearOptions();
                        $aq_direccion_entrecalle1[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist3)
                            $aq_direccion_entrecalle2[0].selectize.clear();
                        $aq_direccion_entrecalle2[0].selectize.clearOptions();
                        $aq_direccion_entrecalle2[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
            },
        });
        var $aq_cpopular = $("#id_person_procedence-cpopular").selectize({
            placeholder: "Selecione un consejo popular",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $q_genero = $("#id_person_queja-genero").selectize({
            create: false,
            placeholder: "Selecione un género",
            allowEmptyOption: false,
        });
        var $q_direccion_calle = $("#id_person_queja-direccion_calle").selectize({
            placeholder: "Selecione una calle",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $q_direccion_entrecalle1 = $("#id_person_queja-direccion_entrecalle1").selectize({
            placeholder: "Selecione un ",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $q_direccion_entrecalle2 = $("#id_person_queja-direccion_entrecalle2").selectize({
            placeholder: "Selecione un ",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $q_municipio = $("#id_person_queja-municipio").selectize({
            create: false,
            placeholder: "Selecione un municipio",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $.ajax({
                    url: '/nomenclador/consejopopular/filter/' + value,
                    success: function(results) {
                        let current_value = $q_cpopular[0].selectize.getValue();
                        let exist = false;
                        for (let i = 0; i < results.length; i++)
                            if (results[i].id == current_value) {
                                exist = true;
                            }
                        if (!exist)
                            $q_cpopular[0].selectize.clear();
                        $q_cpopular[0].selectize.clearOptions();
                        $q_cpopular[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
                $.ajax({
                    url: '/nomenclador/calle/filter/' + value,
                    success: function(results) {
                        let current_value1 = $q_direccion_calle[0].selectize.getValue();
                        let current_value2 = $q_direccion_entrecalle1[0].selectize.getValue();
                        let current_value3 = $q_direccion_entrecalle2[0].selectize.getValue();
                        let exist1, exist2, exist3 = false;
                        for (let i = 0; i < results.length; i++) {
                            if (results[i].id == current_value1) {
                                exist1 = true;
                            }
                            if (results[i].id == current_value2) {
                                exist2 = true;
                            }
                            if (results[i].id == current_value3) {
                                exist3 = true;
                            }
                        }
                        if (!exist1)
                            $q_direccion_calle[0].selectize.clear();
                        $q_direccion_calle[0].selectize.clearOptions();
                        $q_direccion_calle[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist2)
                            $q_direccion_entrecalle1[0].selectize.clear();
                        $q_direccion_entrecalle1[0].selectize.clearOptions();
                        $q_direccion_entrecalle1[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist3)
                            $q_direccion_entrecalle2[0].selectize.clear();
                        $q_direccion_entrecalle2[0].selectize.clearOptions();
                        $q_direccion_entrecalle2[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
            },
        });
        var $q_cpopular = $("#id_person_queja-cpopular").selectize({
            placeholder: "Selecione un consejo popular",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $dir_calle = $("#id_queja-dir_calle").selectize({
            placeholder: "Selecione una calle",
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            allowEmptyOption: false,
            selectOnTab: true,
            createOnBlur: false,
            create: false,
        });
        var $dir_entrecalle1 = $("#id_queja-dir_entrecalle1").selectize({
            placeholder: "Selecione una calle ",
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            allowEmptyOption: false,
            selectOnTab: true,
            createOnBlur: true,
            create: false,
        });
        var $dir_entrecalle2 = $("#id_queja-dir_entrecalle2").selectize({
            required: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            placeholder: "Selecione una calle ",
            allowEmptyOption: false,
            selectOnTab: true,
            createOnBlur: false,
            create: false,
        });
        var $dir_municipio = $("#id_queja-dir_municipio").selectize({
            create: false,
            placeholder: "Selecione un municipio",
            allowEmptyOption: false,
            onChange: function(value) {
                if (!value.length) return;
                $.ajax({
                    url: '/nomenclador/consejopopular/filter/' + value,
                    success: function(results) {
                        let current_value = $q_cpopular[0].selectize.getValue();
                        let exist = false;
                        for (let i = 0; i < results.length; i++)
                            if (results[i].id == current_value) {
                                exist = true;
                            }
                        // console.log(exist, 'pop');
                        if (!exist)
                            $dir_cpopular[0].selectize.clear();
                        $dir_cpopular[0].selectize.clearOptions();
                        $dir_cpopular[0].selectize.load(function (callback) {
                            callback(results);
                        });

                    }
                });
                $.ajax({
                    url: '/nomenclador/calle/filter/' + value,
                    success: function(results) {
                        let current_value1 = $dir_calle[0].selectize.getValue();
                        let current_value2 = $dir_entrecalle1[0].selectize.getValue();
                        let current_value3 = $dir_entrecalle2[0].selectize.getValue();
                        let exist1 = false;
                        let exist2 = false;
                        let exist3 = false;
                        for (let i = 0; i < results.length; i++) {
                            if (results[i].id == current_value1) {
                                exist1 = true;
                            }
                            if (results[i].id == current_value2) {
                                exist2 = true;
                            }
                            if (results[i].id == current_value3) {
                                exist3 = true;
                            }
                        }
                        // console.log(exist1, 1, exist2, 2, exist3, 3);
                        if (!exist1)
                            $dir_calle[0].selectize.clear();
                        $dir_calle[0].selectize.clearOptions();
                        $dir_calle[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist2)
                            $dir_entrecalle1[0].selectize.clear();
                        $dir_entrecalle1[0].selectize.clearOptions();
                        $dir_entrecalle1[0].selectize.load(function (callback) {
                            callback(results);
                        });
                        if (!exist3)
                            $dir_entrecalle2[0].selectize.clear();
                        $dir_entrecalle2[0].selectize.clearOptions();
                        $dir_entrecalle2[0].selectize.load(function (callback) {
                            callback(results);
                        });
                    }
                });
            },
        });
        var $dir_cpopular = $("#id_queja-dir_cpopular").selectize({
            placeholder: "Selecione un consejo popular",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'nombre',
            searchField: 'nombre',
            sortField: 'nombre',
            selectOnTab: true,
            createOnBlur: false,
            create: false,
        });
        var $asunto = $("#id_queja-asunto").selectize({
            create: false,
            placeholder: "Selecione un asunto",
            allowEmptyOption: false,
        });
        var $respondera = $("#id_queja-responder_a").selectize({
            sortField: 'text',
            selectOnTab: true,
            createOnBlur: true,
            placeholder: "Selecione a quien referir respuesta",
            allowEmptyOption: false,
            create: function (input, callback){
                $.ajax({
                    url: '/nomenclador/responder/add/json',
                    type: 'POST',
                    data: {
                        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
                        nombre: input,
                    },
                    success: function (result) {
                        if (result) {
                            callback({ value: result.id, text: result.nombre });
                        }
                    }
                });
            }
        });
        var $tipo = $("#id_queja-tipo").selectize({
            create: false,
            placeholder: "Selecione un tipo",
            allowEmptyOption: false,
        });
        var $personas_list = $("#id_personas_list").selectize({
            create: false,
            maxItems: 1,
            placeholder: "Selecione una persona",
            allowEmptyOption: false,
            valueField: 'id',
            labelField: 'text',
            searchField: ['text', 'ci', 'nombre', 'apellidos', 'email_address', ],
            sortField: [
                {field: 'nombre', direction: 'asc'},
                {field: 'apellidos', direction: 'asc'}
            ],
            preload: true,
            load: function(query, callback) {
                $.ajax({
                    url: '/persona/natural/json',
                    type: 'GET',
                    dataType: 'JSON',
                    success: function(data) {
                        callback(data.personas);
                        if (person_list)
                            $personas_list[0].selectize.setValue(person_list);
                    },
                    error: function() {
                        callback();
                    }
                });
            },
        });

        var _disableOrEnablePNButton = function (element) {
            //console.log('element', element);
            // console.log(submit_button);
            let element_li;
            if (element[0].nodeName === "DIV") {
                element_li = element;

            } else {
                element_li = element.parent(".nav-item");
            };
            //console.log('elementLi', element_li);
            if (element_li[0] == last_tab[0]) {
                next_button.addClass('disabled');
                submit_button.removeClass('disabled');
            } else {
                if (next_button.hasClass('disabled'))
                    next_button.removeClass('disabled');
                if (!submit_button.hasClass('disabled'))
                    submit_button.addClass('disabled');
            };
            if (element_li[0] == first_tab[0]) {
                prev_button.addClass('disabled');
            } else {
                if (prev_button.hasClass('disabled'))
                    prev_button.removeClass('disabled');
            }
        };
        var _loadPersonData = function (id) {
            $.ajax({
                type: "GET",
                url: "/persona/natural/json/"+id,
                contentType: 'json',
                success: function (data) {
                    persona = data;
                    _asigne_person_queja(data);
                    console.log(persona);
                },
                error: function (data, error, status) {
                    console.log(data, error, status)
                },
            })
        };
        var _setValuesAddressQueja = function () {
            // console.log(persona.cpopular, "pop");
            // console.log(persona.direccion_entrecalle1, "1");
            // console.log(persona.direccion_entrecalle2, "2");
            $("#id_queja-dir_municipio")[0].selectize.setValue(persona.municipio, false);
            $("#id_queja-dir_cpopular")[0].selectize.setValue(persona.cpopular, false);
            $("#id_queja-dir_calle")[0].selectize.setValue(persona.direccion_calle, false);
            $("#id_queja-dir_entrecalle1")[0].selectize.setValue(persona.direccion_entrecalle1, false);
            $("#id_queja-dir_entrecalle2")[0].selectize.setValue(persona.direccion_entrecalle2, false);
            $("#id_queja-dir_num").val(persona.direccion_numero);
        };
        var _setValuesAddressPerson = function () {
            $q_municipio[0].selectize.setValue(persona.municipio, false);
            $q_cpopular[0].selectize.setValue(persona.cpopular, false);
            $q_direccion_calle[0].selectize.setValue(persona.direccion_calle, false);
            $q_direccion_entrecalle1[0].selectize.setValue(persona.direccion_entrecalle1, false);
            $q_direccion_entrecalle2[0].selectize.setValue(persona.direccion_entrecalle2, false);
            $("#id_person_queja-dir_num").val(persona.direccion_numero);
        };
        var _getPersonData = function (id) {
            $.ajax({
                url: '/persona/natural/json/'+id,
                type: 'GET',
                dataType: 'JSON',
                success: function(data) {
                    persona = data;
                    _setValuesAddressPerson();
                    // console.log(persona);
                },
                error: function() {
                    console.log(xhr, error, status);
                }
            })
        };
        const _clearEmpProcedence = function () {
                $pj_municipio[0].selectize.clear();
                $pj_cpopular[0].selectize.clear();
                $pj_direccion_calle[0].selectize.clear();
                $pj_direccion_entrecalle2[0].selectize.clear();
                $pj_direccion_entrecalle1[0].selectize.clear();
                $("#id_empresa-nombre").val("");
                $("#id_empresa-sigla").val("");
                $("#id_empresa-telefono").val("");
                $("#id_empresa-movil").val("");
                $("#id_empresa-nombre_contacto").val("");
                $("#id_empresa-codigo_nit").val("");
                $("#id_empresa-codigo_reuup").val("");
                $("#id_empresa-direccion_numero").val("");
        };
        const _clearPersonProcedence = function () {
                $aq_genero[0].selectize.clear();
                $aq_direccion_calle[0].selectize.clear();
                $aq_direccion_entrecalle1[0].selectize.clear();
                $aq_direccion_entrecalle2[0].selectize.clear();
                $aq_municipio[0].selectize.clear();
                $aq_cpopular[0].selectize.clear();
                $("#id_person_procedence-ci").val("");
                $("#id_person_procedence-direccion_numero").val("");
                $("#id_person_procedence-nombre").val("");
                $("#id_person_procedence-apellidos").val("");
                $("#id_person_procedence-movil").val("");
                $("#id_person_procedence-email_address").val("");
                $("#id_person_procedence-telefono").val("");
        };
        const _clearEmailProcedence = function () {
            $("#id_email-email").val("");
        };
        const _clearGobProcedence = function () {
            $("#id_gob-nombre").val("");
        };
        const _clearOrgProcedence = function () {
            $("#id_organiza-nombre").val("");
        };
        const _clearPrensaProcedence = function () {
            $("#id_pe-nombre").val("");
            $("#id_pe-siglas").val("");
        };
        const _clearPhoneProcedence = function () {
            $("#id_telefono-numero").val("");
        };
        const _clearAllProcedence = function () {
            _clearEmpProcedence();
            _clearPersonProcedence();
            _clearEmailProcedence();
            _clearGobProcedence();
            _clearOrgProcedence();
            _clearPrensaProcedence();
            _clearPhoneProcedence();
        };
        var _toggleProcedenciaForms = function () {

            if ($('#id_queja-tipo_procedencia').val() == '') {
                _clearAllProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').addClass('col-lg-12').removeClass('col-lg-6');
                $('.procedent').addClass('no-show');
            } else if ($('#id_queja-tipo_procedencia').val() == '1') {
                _clearAllProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#anon_block').removeClass('no-show');
            } else if ($('#id_queja-tipo_procedencia').val() == '2') {
                _clearEmpProcedence();
                _clearPersonProcedence();
                _clearEmailProcedence();
                _clearGobProcedence();
                _clearOrgProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#prensa_block').removeClass('no-show');
            } else if ($('#id_queja-tipo_procedencia').val() == '3') {
                _clearEmpProcedence();
                _clearEmailProcedence();
                _clearGobProcedence();
                _clearOrgProcedence();
                _clearPrensaProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#persona_block').removeClass('no-show');
            } else if ($('#id_queja-tipo_procedencia').val() == '4') {
                _clearEmpProcedence();
                _clearPersonProcedence();
                _clearEmailProcedence();
                _clearGobProcedence();
                _clearOrgProcedence();
                _clearPrensaProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#telefono_block').removeClass('no-show');
            } else if ($('#id_queja-tipo_procedencia').val() == '5') {
                _clearEmpProcedence();
                _clearPersonProcedence();
                _clearGobProcedence();
                _clearOrgProcedence();
                _clearPrensaProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#correo_block').removeClass('no-show');
            } else if ($('#id_queja-tipo_procedencia').val() == '6') {
                _clearPersonProcedence();
                _clearEmailProcedence();
                _clearGobProcedence();
                _clearOrgProcedence();
                _clearPrensaProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#empresa_block').removeClass('no-show');
            } else if ($('#id_queja-tipo_procedencia').val() == '7') {
                _clearEmpProcedence();
                _clearPersonProcedence();
                _clearEmailProcedence();
                _clearOrgProcedence();
                _clearPrensaProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#gob_block').removeClass('no-show');
            } else if ($('#id_queja-tipo_procedencia').val() == '8') {
                _clearEmpProcedence();
                _clearPersonProcedence();
                _clearEmailProcedence();
                _clearGobProcedence();
                _clearPrensaProcedence();
                _clearPhoneProcedence();
                $('#id_queja-tipo_procedencia').parent('.row.form-group.col-lg-6').removeClass('col-lg-12').addClass('col-lg-6');
                $('.procedent').addClass('no-show');
                $('#org_block').removeClass('no-show');
            }
        };
        var _getProcedence = function () {
            let type_procedence_value = $("#id_queja-tipo_procedencia")[0].selectize.getValue();
            let data = null;
            if (type_procedence_value == 2) {
                data = {
                    nombre: $('#id_pe-nombre').val(),
                    siglas: $('#id_pe-siglas').val(),
                };
            } else if (type_procedence_value == 3) {
                data = {
                    ci: $("#id_person_procedence-ci").val(),
                    nombre: $("#id_person_procedence-nombre").val(),
                    apellidos: $("#id_person_procedence-apellidos").val(),
                    movil: $("#id_person_procedence-movil").val(),
                    email_address: $("#id_person_procedence-email_address").val(),
                    telefono: $("#id_person_procedence-telefono").val(),
                    direccion_numero: $("#id_person_procedence-direccion_numero").val(),
                    genero: $("#id_person_procedence-genero")[0].selectize.getOption($("#id_person_procedence-genero")[0].selectize.getValue()).text(),
                    genero_value: $("#id_person_procedence-genero")[0].selectize.getValue(),
                    municipio: $("#id_person_procedence-municipio")[0].selectize.getOption($("#id_person_procedence-municipio")[0].selectize.getValue()).text(),
                    municipio_value: $("#id_person_procedence-municipio")[0].selectize.getValue(),
                    cpopular: $("#id_person_procedence-cpopular")[0].selectize.getOption($("#id_person_procedence-cpopular")[0].selectize.getValue()).text(),
                    cpopular_value: $("#id_person_procedence-cpopular")[0].selectize.getValue(),
                    direccion_calle: $("#id_person_procedence-direccion_calle")[0].selectize.getOption($("#id_person_procedence-direccion_calle")[0].selectize.getValue()).text(),
                    direccion_calle_value: $("#id_person_procedence-direccion_calle")[0].selectize.getValue(),
                    direccion_entrecalle1: $("#id_person_procedence-direccion_entrecalle1")[0].selectize.getOption($("#id_person_procedence-direccion_entrecalle1")[0].selectize.getValue()).text(),
                    direccion_entrecalle1_value: $("#id_person_procedence-direccion_entrecalle1")[0].selectize.getValue(),
                    direccion_entrecalle2: $("#id_person_procedence-direccion_entrecalle2")[0].selectize.getOption($("#id_person_procedence-direccion_entrecalle2")[0].selectize.getValue()).text(),
                    direccion_entrecalle2_value: $("#id_person_procedence-direccion_entrecalle2")[0].selectize.getValue(),
                };
            } else if (type_procedence_value == 4) {
                data = {
                    numero: $("#id_telefono-numero").val(),
                };
            } else if (type_procedence_value == 5) {
                data = {
                    email: $("#id_email-email").val(),
                };
            } else if (type_procedence_value == 6) {
                data = {
                    nombre: $("#id_empresa-nombre").val(),
                    sigla: $("#id_empresa-sigla").val(),
                    telefono: $("#id_empresa-telefono").val(),
                    movil: $("#id_empresa-movil").val(),
                    nombre_contacto: $("#id_empresa-nombre_contacto").val(),
                    email_address: $("#id_empresa-email_address").val(),
                    codigo_nit: $("#id_empresa-codigo_nit").val(),
                    codigo_reuup: $("#id_empresa-codigo_reuup").val(),
                    direccion_numero: $("#id_empresa-direccion_numero").val(),
                    municipio_value: $("#id_empresa-municipio")[0].selectize.getValue(),
                    municipio: $("#id_empresa-municipio")[0].selectize.getOption($("#id_empresa-municipio")[0].selectize.getValue()).text(),
                    cpopular_value: $("#id_empresa-cpopular")[0].selectize.getValue(),
                    cpopular: $("#id_empresa-cpopular")[0].selectize.getOption($("#id_empresa-cpopular")[0].selectize.getValue()).text(),
                    direccion_calle_value: $("#id_empresa-direccion_calle")[0].selectize.getValue(),
                    direccion_calle: $("#id_empresa-direccion_calle")[0].selectize.getOption($("#id_empresa-direccion_calle")[0].selectize.getValue()).text(),
                    direccion_entrecalle1_value: $("#id_empresa-direccion_entrecalle1")[0].selectize.getValue(),
                    direccion_entrecalle1: $("#id_empresa-direccion_entrecalle1")[0].selectize.getOption($("#id_empresa-direccion_entrecalle1")[0].selectize.getValue()).text(),
                    direccion_entrecalle2_value: $("#id_empresa-direccion_entrecalle2")[0].selectize.getValue(),
                    direccion_entrecalle2: $("#id_empresa-direccion_entrecalle2")[0].selectize.getOption($("#id_empresa-direccion_entrecalle2")[0].selectize.getValue()).text(),
                };
            } else if (type_procedence_value == 7) {
                data = {
                    nombre: $("#id_gob-nombre").val(),
                }
            } else if (type_procedence_value == 8) {
                data = {
                    nombre: $("#id_organiza-nombre").val(),
                };
            } else {
                data = {};
            }
            // console.log(data);
            return data;
        };
        var _makeSumary = function () {
            let type_procedence = $("#id_queja-tipo_procedencia")[0].selectize.getOption($("#id_queja-tipo_procedencia")[0].selectize.getValue()).text();
            let type_procedence_value = $("#id_queja-tipo_procedencia")[0].selectize.getValue();

            let procedence_data = _getProcedence();
            let quejoso_data = {
                not_db: $("#id_queja-damnificado_not_indb")[0].checked,
                persona: $("#id_personas_list")[0].selectize.getValue(),
                ci: $("#id_person_queja-ci").val(),
                nombre: $("#id_person_queja-nombre").val(),
                apellidos: $("#id_person_queja-apellidos").val(),
                movil: $("#id_person_queja-movil").val(),
                email_address: $("#id_person_queja-email_address").val(),
                telefono: $("#id_person_queja-telefono").val(),
                direccion_numero: $("#id_person_queja-direccion_numero").val(),
                genero_value: $("#id_person_queja-genero")[0].selectize.getValue(),
                genero: $("#id_person_queja-genero")[0].selectize.getOption($("#id_person_queja-genero")[0].selectize.getValue()).text(),
                municipio_value: $("#id_person_queja-municipio")[0].selectize.getValue(),
                municipio: $("#id_person_queja-municipio")[0].selectize.getOption($("#id_person_queja-municipio")[0].selectize.getValue()).text(),
                cpopular_value: $("#id_person_queja-cpopular")[0].selectize.getValue(),
                cpopular: $("#id_person_queja-cpopular")[0].selectize.getOption($("#id_person_queja-cpopular")[0].selectize.getValue()).text(),
                direccion_calle_value: $("#id_person_queja-direccion_calle")[0].selectize.getValue(),
                direccion_calle: $("#id_person_queja-direccion_calle")[0].selectize.getOption($("#id_person_queja-direccion_calle")[0].selectize.getValue()).text(),
                direccion_entrecalle1_value: $("#id_person_queja-direccion_entrecalle1")[0].selectize.getValue(),
                direccion_entrecalle1: $("#id_person_queja-direccion_entrecalle1")[0].selectize.getOption($("#id_person_queja-direccion_entrecalle1")[0].selectize.getValue()).text(),
                direccion_entrecalle2_value: $("#id_person_queja-direccion_entrecalle2")[0].selectize.getValue(),
                direccion_entrecalle2: $("#id_person_queja-direccion_entrecalle2")[0].selectize.getOption($("#id_person_queja-direccion_entrecalle2")[0].selectize.getValue()).text(),
            };
            let queja_data = {
                no_procendencia: $("#id_queja-no_procendencia").val(),
                no_radicacion: $("#id_queja-no_radicacion").val(),
                dir_num: $("#id_queja-dir_num").val(),
                referencia: $("#id_queja-referencia").val(),
                asunto_texto: $("#id_queja-asunto_texto").val(),
                texto: $("#id_queja-texto").val(),
                dir_calle_value: $("#id_queja-dir_calle")[0].selectize.getValue(),
                dir_calle: $("#id_queja-dir_calle")[0].selectize.getOption($("#id_queja-dir_calle")[0].selectize.getValue()).text(),
                dir_entrecalle1: $("#id_queja-dir_entrecalle1")[0].selectize.getOption($("#id_queja-dir_entrecalle1")[0].selectize.getValue()).text(),
                dir_entrecalle1_value: $("#id_queja-dir_entrecalle1")[0].selectize.getValue(),
                dir_entrecalle2: $("#id_queja-dir_entrecalle2")[0].selectize.getOption($("#id_queja-dir_entrecalle2")[0].selectize.getValue()).text(),
                dir_entrecalle2_value: $("#id_queja-dir_entrecalle2")[0].selectize.getValue(),
                dir_municipio: $("#id_queja-dir_municipio")[0].selectize.getOption($("#id_queja-dir_municipio")[0].selectize.getValue()).text(),
                dir_municipio_value: $("#id_queja-dir_municipio")[0].selectize.getValue(),
                dir_cpopular: $("#id_queja-dir_cpopular")[0].selectize.getOption($("#id_queja-dir_cpopular")[0].selectize.getValue()).text(),
                dir_cpopular_value: $("#id_queja-dir_cpopular")[0].selectize.getValue(),
                asunto: $("#id_queja-asunto")[0].selectize.getOption($("#id_queja-asunto")[0].selectize.getValue()).text(),
                asunto_value: $("#id_queja-asunto")[0].selectize.getValue(),
                tipo: $("#id_queja-tipo")[0].selectize.getOption($("#id_queja-tipo")[0].selectize.getValue()).text(),
                tipo_value: $("#id_queja-tipo")[0].selectize.getValue(),
            };
            quejoso_data.persona_data = {
                ci: "",
            };
            if (!quejoso_data.not_db) {
                if (persona != null)
                    quejoso_data.persona_data = persona;
            };
            // console.log(quejoso_data.persona_data);
            let data = {
                type_procedence: type_procedence,
                type_procedence_value: type_procedence_value,
                procedence_data: procedence_data,
                quejoso_data: quejoso_data,
                queja_data: queja_data,
                empty_sumary_msg: empty_sumary_msg,
                empty_procedence_msg: empty_procedence_msg,
                empty_quejoso_msg: empty_quejoso_msg,
                empty_queja_msg: empty_queja_msg,
            };
            // console.log(data);
            var contenido = `
                {{if ((type_procedence_value != "" && type_procedence != "" ) || (quejoso_data.ci != "" || quejoso_data.persona_data.ci != "") || (queja_data.texto != "" && queja_data.asunto_texto != "" ))}}
                <div class="col-md-12">
                    <div class="card border border-dark">
                        <div class="card-header border border-dark">
                            <strong class="card-title">Procedencia</strong>
                        </div>
                        <div class="card-body">
                        {{if (type_procedence_value != "" && type_procedence != "" )}}
                            <p class="card-text"><strong>Procedencia:</strong>{{:type_procedence}}</p>
                            {{if (type_procedence_value == "2")}}
                            <p class="card-text"><strong>Nombre: </strong>{{:procedence_data.nombre}}</p>
                            <p class="card-text"><strong>Siglas: </strong>{{:procedence_data.siglas}}</p>
                            {{else (type_procedence_value == "3")}}
                            <p class="card-text"><strong>Nombre: </strong>{{:procedence_data.nombre}} {{:procedence_data.apellidos}}</p>
                            <p class="card-text"><strong>CI: </strong>{{:procedence_data.ci}} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>Sexo:</strong>{{:procedence_data.genero}}</p>
                            <p class="card-text"><strong>Email: </strong>{{if (procedence_data.email_address != "")}}{{:procedence_data.email_address}}{{else}}No especificado{{/if}}</p>
                            <p class="card-text"><strong>Teléfono: </strong>{{if (procedence_data.telefono != "")}}{{:procedence_data.telefono}}{{else}}No especificado{{/if}}</p>
                            <p class="card-text"><strong>Movil: </strong>{{if (procedence_data.movil != "")}}{{:procedence_data.movil}}{{else}}No especificado{{/if}}</p>
                                {{if (procedence_data.direccion_calle != "")}}
                            <p class="card-text"><strong>Dirección: </strong>{{:procedence_data.direccion_calle}} #{{:procedence_data.direccion_numero}} entre {{:procedence_data.direccion_entrecalle1}} y {{:procedence_data.direccion_entrecalle2}}, en el{{if (procedence_data.cpopular != "")}} consejo popular {{:procedence_data.cpopular}} del{{/if}} municipio {{:procedence_data.municipio}}.</p>
                                {{else}}
                            <p class="card-text"><strong>Dirección: </strong>No especificada</p>
                                {{/if}}
                            {{else (type_procedence_value == "4")}}
                            <p class="card-text"><strong>Número: </strong>{{:procedence_data.numero}}</p>
                            {{else (type_procedence_value == "5")}}
                            <p class="card-text"><strong>Correo Electónico: </strong>{{:procedence_data.email}}</p>
                            {{else (type_procedence_value == "6")}}
                            <p class="card-text"><strong>Nombre: </strong>{{:procedence_data.nombre}} ({{:procedence_data.sigla}})</p>
                            <p class="card-text"><strong>Teléfono: </strong>{{if (procedence_data.telefono != "")}}{{:procedence_data.telefono}}{{else}}No especificado{{/if}}</p>
                            <p class="card-text"><strong>Movil: </strong>{{if (procedence_data.movil != "")}}{{:procedence_data.movil}}{{else}}No especificado{{/if}}</p>
                            <p class="card-text"><strong>Email: </strong>{{if (procedence_data.email_address != "")}}{{:procedence_data.email_address}}{{else}}No especificado{{/if}}</p>
                            <p class="card-text"><strong>Nombre Persona Contacto: </strong>{{if (procedence_data.nombre_contacto != "")}}{{:procedence_data.nombre_contacto}}{{else}}No especificado{{/if}}</p>
                            <p class="card-text"><strong>Código NiT: </strong>{{:procedence_data.codigo_nit}} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>Código ReUUP: </strong>{{:procedence_data.codigo_reuup}}</p>
                                {{if (procedence_data.direccion_calle != "")}}
                            <p class="card-text"><strong>Dirección: </strong>{{:procedence_data.direccion_calle}} #{{:procedence_data.direccion_numero}} entre {{:procedence_data.direccion_entrecalle1}} y {{:procedence_data.direccion_entrecalle2}} en el{{if (procedence_data.cpopular != "")}} consejo popular {{:procedence_data.cpopular}} del{{/if}} municipio de {{:procedence_data.municipio}}</p>
                                {{else}}
                            <p class="card-text"><strong>Dirección: </strong>No especificada</p>
                                {{/if}}
                            {{else (type_procedence_value == "7")}}
                            <p class="card-text"><strong>Nombre:</strong>{{:procedence_data.nombre}}</p>
                            {{else (type_procedence_value == "8")}}
                            <p class="card-text"><strong>Nombre:</strong>{{:procedence_data.nombre}}</p>
                            {{/if}}
                        {{else}}
                            <div class="alert alert-danger" role="alert">
                                <h4 class="alert-heading">Alerta</h4>
                                <hr>
                                <p class="mb-0">{{:empty_procedence_msg}}</p>
                            </div>
                        {{/if}}
                        </div>
                    </div>
                </div>
                <div class="col-md-12">
                    <div class="card border border-primary">
                        <div class="card-header border border-primary">
                            <strong class="card-title">Aquejado</strong>
                        </div>
                        <div class="card-body">
                        {{if (quejoso_data.ci == "" && quejoso_data.persona_data.ci == "")}}
                            <div class="alert alert-danger" role="alert">
                                <h4 class="alert-heading">Alerta</h4>
                                <hr>
                                <p class="mb-0">{{:empty_quejoso_msg}}</p>
                            </div>
                        {{else}}
                            {{if (quejoso_data.persona_data.ci == "")}}
                            <p class="card-text"><strong>Nombre: </strong>{{:quejoso_data.nombre}} {{:quejoso_data.apellidos}}</p>
                            <p class="card-text"><strong>CI: </strong>{{:quejoso_data.ci}} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>Sexo:</strong>{{:quejoso_data.genero}}</p>
                            <p class="card-text"><strong>Email: </strong>{{if (quejoso_data.email_address != "")}}{{:quejoso_data.email_address}}{{else}}No especificado{{/if}}</p>
                            <p class="card-text"><strong>Teléfono: </strong>{{if (quejoso_data.telefono != "")}}{{:quejoso_data.telefono}}{{else}}No especificado{{/if}}</p>
                            <p class="card-text"><strong>Movil: </strong>{{if (quejoso_data.movil != "")}}{{:quejoso_data.movil}}{{else}}No especificado{{/if}}</p>
                                {{if (quejoso_data.direccion_calle != "")}}
                            <p class="card-text"><strong>Dirección: </strong>{{:quejoso_data.direccion_calle}} #{{:quejoso_data.direccion_numero}} entre {{:quejoso_data.direccion_entrecalle1}} y {{:quejoso_data.direccion_entrecalle2}}, en el consejo popular {{:quejoso_data.cpopular}} del municipio {{:quejoso_data.municipio}}.</p>
                                {{else}}
                            <p class="card-text"><strong>Dirección: </strong>No especificada</p>
                                {{/if}}
                            {{else}}
                            <p class="card-text"><strong>Nombre: </strong>{{:quejoso_data.persona_data.nombre}} {{:quejoso_data.persona_data.apellidos}}</p>
                            <p class="card-text"><strong>CI: </strong>{{:quejoso_data.persona_data.ci}} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>Sexo:</strong>{{:quejoso_data.persona_data.genero_nombre}}</p>
                            <p class="card-text"><strong>Email: </strong>{{if (quejoso_data.persona_data.email_address != "")}}{{:quejoso_data.persona_data.email_address}}{{else}}No especificado{{/if}}</p>
                            <p class="card-text"><strong>Teléfono: </strong>{{if (quejoso_data.persona_data.telefono != "")}}{{:quejoso_data.persona_data.telefono}}{{else}}No especificado{{/if}}</p>
                            <p class="card-text"><strong>Movil: </strong>{{if (quejoso_data.persona_data.movil != "")}}{{:quejoso_data.persona_data.movil}}{{else}}No especificado{{/if}}</p>
                                {{if (quejoso_data.persona_data.direccion_calle_nombre != "")}}
                            <p class="card-text"><strong>Dirección: </strong>{{:quejoso_data.persona_data.direccion_calle_nombre}} #{{:quejoso_data.persona_data.direccion_numero}} entre {{:quejoso_data.persona_data.direccion_entrecalle1_nombre}} y {{:quejoso_data.persona_data.direccion_entrecalle2_nombre}}, en el consejo popular {{:quejoso_data.persona_data.cpopular_nombre}} del municipio {{:quejoso_data.persona_data.municipio_nombre}}.</p>
                                {{else}}
                            <p class="card-text"><strong>Dirección: </strong>No especificada</p>
                                {{/if}}
                            {{/if}}
                        {{/if}}
                        </div>
                    </div>
                </div>
                <div class="col-md-12">
                    <div class="card border border-info">
                        <div class="card-header border border-info">
                            <strong class="card-title">Queja</strong>
                        </div>
                        <div class="card-body">
                            {{if (queja_data.texto != "" && queja_data.asunto_texto != "" )}}
                            <p class="card-text"><strong>No. Procedencia: </strong>{{:queja_data.no_procendencia}}</p>
                            <p class="card-text"><strong>Referencia: </strong>{{:queja_data.referencia}}</p>
                                {{if (queja_data.dir_calle != "")}}
                            <p class="card-text"><strong>Dirección: </strong>{{:queja_data.dir_calle}} #{{:queja_data.dir_num}} entre {{:queja_data.dir_entrecalle1}} y {{:queja_data.dir_entrecalle2}}, en el consejo popular {{:queja_data.dir_cpopular}} del municipio {{:queja_data.dir_municipio}}.</p>
                                {{else}}
                            <p class="card-text"><strong>Dirección: </strong>No especificada</p>
                                {{/if}}
                            <p class="card-text"><strong>Tipo: </strong>{{:queja_data.tipo}}  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>Código Asunto: </strong>{{:queja_data.asunto}} </p>
                            <p class="card-text"><strong>Asunto: </strong>{{:queja_data.asunto_texto}}</p>
                            <p class="card-text"><strong>Cuerpo de la Queja: </strong>{{:queja_data.texto}}</p>
                            {{else}}
                            <div class="alert alert-danger" role="alert">
                                <h4 class="alert-heading">Alerta</h4>
                                <hr>
                                <p class="mb-0">{{:empty_queja_msg}}</p>
                            </div>
                            {{/if}}
                        </div>
                    </div>
                </div>
                {{else}}
                <div class="col-md-12">
                    <div class="card border border-danger">
                        <div class="card-header border border-danger">
                            <strong class="card-title">Sin Datos</strong>
                        </div>
                        <div class="card-body">
                            <div class="alert alert-danger" role="alert">
                                <h4 class="alert-heading">Alerta</h4>
                                <hr>
                                <p class="mb-0 text-danger">{{:empty_sumary_msg}}</p>
                            </div>
                        </div>
                    </div>
                </div>
                {{/if}}
            `;
            //console.log(quejoso_data);
            $.templates({contenido: contenido, });
            var html = $.render.contenido(data);
            sumary_container.html(html);
            $(".ref_procedence").on('click', function (e) {
                e.preventDefault();
                $('#procedencia_tab').trigger('click');
            });
            $(".ref_quejoso").on('click', function (e) {
                e.preventDefault();
                $('#aquejado_tab').trigger('click');
            });
            $(".ref_queja").on('click', function (e) {
                e.preventDefault();
                $('#queja_tab').trigger('click');
            });
        };
        var _asigne_person_queja = function(data) {
            $("#id_person_queja-ci").val(data.ci);
            $("#id_person_queja-nombre").val(data.nombre);
            $("#id_person_queja-apellidos").val(data.apellidos);
            $("#id_person_queja-movil").val(data.movil);
            $("#id_person_queja-email_address").val(data.email_address);
            $("#id_person_queja-telefono").val(data.telefono);
            $("#id_person_queja-direccion_numero").val(data.direccion_numero);
            $("#id_person_queja-genero")[0].selectize.setValue(data.genero);
            $("#id_person_queja-municipio")[0].selectize.setValue(data.municipio);
            $("#id_person_queja-cpopular")[0].selectize.setValue(data.cpopular);
            $("#id_person_queja-direccion_calle")[0].selectize.setValue(data.direccion_calle);
            $("#id_person_queja-direccion_entrecalle1")[0].selectize.setValue(data.direccion_entrecalle1);
            $("#id_person_queja-direccion_entrecalle2")[0].selectize.setValue(data.direccion_entrecalle2);
            //console.log($("#id_person_queja-direccion_entrecalle2").val(), 2, $("#id_person_queja-direccion_entrecalle1").val(), 1)
        };
        var _perform_show_person_queja = function () {
            // console.log("revisando", $("#id_queja-damnificado_not_indb"));
            if ($("#id_queja-damnificado_not_indb")[0].checked) {
                 $("#is_indb").addClass('no-show');
                 $("#not_indb").removeClass('no-show');
            }
        };
        var _fill_selectizes_with_values = function () {
            // console.log('tproce', $("#id_queja-tipo_procedencia").val());
            if ($("#id_queja-tipo_procedencia").val())
                $tipo_procedencia[0].selectize.setValue($("#id_queja-tipo_procedencia").val());
            // console.log('pjmun', $("#id_empresa-municipio").val());
            if ($("#id_empresa-municipio").val())
                $pj_municipio[0].selectize.setValue($("#id_empresa-municipio").val());
            // console.log('pjcp', $("#id_empresa-cpopular").val());
            if ($("#id_empresa-cpopular").val())
                $pj_cpopular[0].selectize.setValue($("#id_empresa-cpopular").val());
            // console.log('pjcalle', $("#id_empresa-direccion_calle").val());
            if ($("#id_empresa-direccion_calle").val())
                $pj_direccion_calle[0].selectize.setValue($("#id_empresa-direccion_calle").val());
            // console.log('pjecalle1', $("#id_empresa-direccion_entrecalle1").val());
            if ($("#id_empresa-direccion_entrecalle1").val())
                $pj_direccion_entrecalle1[0].selectize.setValue($("#id_empresa-direccion_entrecalle1").val());
            // console.log('pjecalle2', $("#id_empresa-direccion_entrecalle2").val());
            if ($("#id_empresa-direccion_entrecalle2").val())
                $pj_direccion_entrecalle2[0].selectize.setValue($("#id_empresa-direccion_entrecalle2").val());
            // console.log('aqgen', $("#id_person_procedence-genero").val());
            if ($("#id_person_procedence-genero").val())
                $aq_genero[0].selectize.setValue($("#id_person_procedence-genero").val());
            // console.log('aqmun', $("#id_person_procedence-municipio").val());
            if ($("#id_person_procedence-municipio").val())
                $aq_municipio[0].selectize.setValue($("#id_person_procedence-municipio").val());
            // console.log('aqcalle', $("#id_person_procedence-direccion_calle").val());
            if ($("#id_person_procedence-direccion_calle").val())
                $aq_direccion_calle[0].selectize.setValue($("#id_person_procedence-direccion_calle").val());
            // console.log('aqecalle1', $("#id_person_procedence-direccion_entrecalle1").val());
            if ($("#id_person_procedence-direccion_entrecalle1").val())
                $aq_direccion_entrecalle1[0].selectize.setValue($("#id_person_procedence-direccion_entrecalle1").val());
            // console.log('aqecalle2', $("#id_person_procedence-direccion_entrecalle2").val());
            if ($("#id_person_procedence-direccion_entrecalle2").val())
                $aq_direccion_entrecalle2[0].selectize.setValue($("#id_person_procedence-direccion_entrecalle2").val());
            // console.log('aqcp', $("#id_person_procedence-cpopular").val());
            if ($("#id_person_procedence-cpopular").val())
                $aq_cpopular[0].selectize.setValue($("#id_person_procedence-cpopular").val());
            // console.log('pqmun', $("#id_person_queja-municipio").val());
            if ($("#id_person_queja-municipio").val())
                $q_municipio[0].selectize.setValue($("#id_person_queja-municipio").val());
            // console.log('pqcp', $("#id_person_queja-cpopular").val());
            if ($("#id_person_queja-cpopular").val())
                $q_cpopular[0].selectize.setValue($("#id_person_queja-cpopular").val());
            // console.log('pqcalle', $("#id_person_queja-direccion_calle").val());
            if ($("#id_person_queja-direccion_calle").val())
                $q_direccion_calle[0].selectize.setValue($("#id_person_queja-direccion_calle").val());
            // console.log('pqecalle1', $("#id_person_queja-direccion_entrecalle1").val());
            if ($("#id_person_queja-direccion_entrecalle1").val())
                $q_direccion_entrecalle1[0].selectize.setValue($("#id_person_queja-direccion_entrecalle1").val());
            // console.log('pqecalle2', $("#id_person_queja-direccion_entrecalle2").val());
            if ($("#id_person_queja-direccion_entrecalle2").val())
                $q_direccion_entrecalle2[0].selectize.setValue($("#id_person_queja-direccion_entrecalle2").val());
            // console.log('qmun', $("#id_queja-dir_municipio").val());
            if ($("#id_queja-dir_municipio").val())
                $dir_municipio[0].selectize.setValue($("#id_queja-dir_municipio").val());
            // console.log('qcp', $("#id_queja-dir_cpopular").val());
            if ($("#id_queja-dir_cpopular").val())
                $dir_cpopular[0].selectize.setValue($("#id_queja-dir_cpopular").val());
            // console.log('qcalle', $("#id_queja-dir_calle").val());
            if ($("#id_queja-dir_calle").val())
                $dir_calle[0].selectize.setValue($("#id_queja-dir_calle").val());
            // console.log('qecalle1', $("#id_queja-dir_entrecalle1").val());
            if ($("#id_queja-dir_entrecalle1").val())
                $dir_entrecalle1[0].selectize.setValue($("#id_queja-dir_entrecalle1").val());
            // console.log('qecalle2', $("#id_queja-dir_entrecalle2").val());
            if ($("#id_queja-dir_entrecalle2").val())
                $dir_entrecalle2[0].selectize.setValue($("#id_queja-dir_entrecalle2").val());
            // console.log('qsubj', $("#id_queja-asunto").val());
            if ($("#id_queja-asunto").val())
                $asunto[0].selectize.setValue($("#id_queja-asunto").val());
            // console.log('qansw', $("#id_queja-responder_a").val());
            if ($("#id_queja-responder_a").val())
                $respondera[0].selectize.setValue($("#id_queja-responder_a").val());
            // console.log('qtipe', $("#id_queja-tipo").val());
            if ($("#id_queja-tipo").val())
                $tipo[0].selectize.setValue($("#id_queja-tipo").val());
            // console.log('perlist', $("#id_personas_list").val());
            if (person_list)
                _loadPersonData();
                $personas_list[0].selectize.setValue(person_list);
        };

        _toggleProcedenciaForms();
        _perform_show_person_queja();
        _fill_selectizes_with_values();
//         //console.log('algo', $('input[id$="-selectized"]'));
    };
    var _initQuejaForm = function () {
        const input1 = document.getElementById('id_pe-nombre');
        const input2 = document.getElementById('id_pe-siglas');
        const input3 = document.getElementById('id_person_procedence-ci');
        const input4 = document.getElementById('id_person_procedence-nombre');
        const input5 = document.getElementById('id_person_procedence-apellidos');
        const input6 = document.getElementById('id_telefono-numero');
        const input7 = document.getElementById('id_email-email');
        const input8 = document.getElementById('id_gob-nombre');
        const input9 = document.getElementById('id_organiza-nombre');
        const input10 = document.getElementById('id_empresa-nombre');
        const input11 = document.getElementById('id_empresa-sigla');
        const input12 = document.getElementById('id_empresa-codigo_nit');
        const input13 = document.getElementById('id_empresa-codigo_reuup');

        const awesomplete1 = new Awesomplete(input1);
        const awesomplete2 = new Awesomplete(input2);
        const awesomplete3 = new Awesomplete(input3);
        const awesomplete4 = new Awesomplete(input4);
        const awesomplete5 = new Awesomplete(input5);
        const awesomplete6 = new Awesomplete(input6);
        const awesomplete7 = new Awesomplete(input7);
        const awesomplete8 = new Awesomplete(input8);
        const awesomplete9 = new Awesomplete(input9);
        const awesomplete10 = new Awesomplete(input10);
        const awesomplete11 = new Awesomplete(input11);
        const awesomplete12 = new Awesomplete(input12);
        const awesomplete13 = new Awesomplete(input13);

        $.validator.setDefaults({
            errorClass: 'text-danger',
            highlight: function(element) {
                $(element).addClass('is-invalid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },
            // Validate only visible fields
			ignore: ":hidden",

            errorPlacement: function(error, element) {
                if (element[0].attributes['type'].nodeValue == 'select-one' || element[0].attributes['type'].nodeValue == 'select-multiple')
                    error.insertBefore(element.parent());
                else
                    error.insertBefore(element);
            },

        });
        let validator_form = queja_form.validate({
			rules: {
				'queja-tipo_procedencia': {
				    required: true,
				},
				'email-email': {
				    required: true,
				    email: true,
				},
				'pe-nombre': {
				    required: true,
                    maxlength: 30,
				},
				'pe-siglas': {
				    required: true,
                    maxlength: 10,
				},
				'person_procedence-ci': {
				    required: true,
				    digits: true,
                    maxlength: 11,
                    minlength: 11,
				},
				'person_procedence-nombre': {
				    required: true,
				    maxlength: 30,
				},
				'person_procedence-apellidos': {
				    required: true,
                    maxlength: 50,
				},
				'person_procedence-genero': {
				    required: true,
				},
				'person_procedence-email_address': {
				    email: true,
				},
				'person_procedence-movil': {
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                    remote: {
                        url: '/persona/natural/verify',
                        type: 'GET',
                    },
                },
				'person_procedence-telefono': {
				    required: true,
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
				},
				'person_procedence-direccion_calle': {
				    required: true,
				},
				'person_procedence-direccion_numero': {
				    required: true,
				},
				'person_procedence-direccion_entrecalle1': {
				    required: true,
				},
				'person_procedence-direccion_entrecalle2': {
				    required: true,
				},
				'person_procedence-municipio': {
				    required: true,
				},
				'person_procedence-cpopular': {
				    required: true,
				},
				'telefono-numero': {
				    required: true,
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
				},
				'empresa-nombre': {
				    required: true,
				    maxlength: 100,
				},
				'empresa-sigla': {
				    required: true,
                    maxlength: 10,
				},
				'empresa-telefono': {
				    required: true,
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
				},
				'empresa-movil': {
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                    remote: {
                        url: '/persona/natural/verify',
                        type: 'GET',
                    },
                },
				'empresa-nombre_contacto': {
				    required: true,
                    maxlength: 200,
				},
				'empresa-email_address': {
				    email: true,
				},
				'empresa-codigo_nit': {
				    required: true,
				},
				'empresa-codigo_reuup': {
				    required: true,
				},
				'empresa-municipio': {
				    required: true,
				},
				'empresa-cpopular': {
				    required: true,
				},
				'empresa-direccion_calle': {
				    required: true,
				},
				'empresa-direccion_numero': {
				    required: true,
				},
				'empresa-direccion_entrecalle1': {
				    required: true,
				},
				'empresa-direccion_entrecalle2': {
				    required: true,
				},
				'gob-nombre': {
				    required: true,
				    maxlength: 50,
				},
				'organiza-nombre': {
				    required: true,
				    maxlength: 50,
				},
				'personas_list': {
				    required: true,
				},
				'person_queja-ci': {
				    required: true,
				    digits: true,
                    maxlength: 11,
                    minlength: 11,
				},
				'person_queja-nombre': {
				    maxlength: 30,
				    required: true,
				},
				'person_queja-apellidos': {
				    required: true,
                    maxlength: 50,
				},
				'person_queja-genero': {
				    required: true,
				},
				'person_queja-email_address': {
				    email: true,
				},
				'person_queja-movil': {
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                    remote: {
                        url: '/persona/natural/verify',
                        type: 'GET',
                    },
                },
				'person_queja-telefono': {
				    required: true,
                    digits: true,
                    maxlength: 8,
                    minlength: 8,
                },
				'person_queja-direccion_calle': {
				    required: true,
				},
				'person_queja-direccion_numero': {
				    required: true,
				},
				'person_queja-direccion_entrecalle1': {
				    required: true,
				},
				'person_queja-direccion_entrecalle2': {
				    required: true,
				},
				'person_queja-cpopular': {
				    required: true,
				},
				'person_queja-municipio': {
				    required: true,
				},
				'queja-no_procendencia': {},
				'queja-no_radicacion': {},
				'queja-dir_calle': {
				    required: true,
				},
				'queja-dir_num': {
				    required: true,
				},
				'queja-dir_entrecalle1': {
				    required: true,
				},
				'queja-dir_entrecalle2': {
				    required: true,
				},
				'queja-dir_municipio': {
				    required: true,
				},
				'queja-dir_cpopular': {
				    required: true,
				},
				'queja-referencia': {},
				'queja-asunto': {
				    required: true,
				},
				'queja-tipo': {
				    required: true,
				},
				'queja-responder_a': {
				    required: true,
				},
				'queja-asunto_texto': {
				    required: true,
                    maxlength: 300,
				},
				'queja-texto': {
				    required: true,
                    maxlength: 3000,
                    minlength: 20,
				},
			},
			messages:{
				'queja-tipo_procedencia': {
				    required: "Tiene que seleccionar un tipo de procedencia.",
				},
				'queja-tipo_procedencia-selectized': {
				    required: "Tiene que seleccionar un tipo de procedencia.",
				},
				'email-email': {
				    required: "El email no puede quedar en blanco.",
				    email: "El email debe ser una dirección de correo electrónico válido.",
				},
				'pe-nombre': {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "El nombre no puede tener más de 30 caracteres.",
				},
				'pe-siglas': {
				    required: "Las siglas no pueden quedar en blanco.",
                    maxlength: "Las siglas no pueden más de 10 caracteres.",
				},
				'person_procedence-ci': {
				    required: "El CI no puede quedar en blanco.",
				    digits: "El CI solo puede tener dígitos.",
                    maxlength: "El CI no puede tener más de 11 dígitos.",
                    minlength: "El CI no puede tener menos de 11 dígitos.",
				},
				'person_procedence-nombre': {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "El nombre no puede tener más de 30 caracteres.",
				},
				'person_procedence-apellidos': {
				    required: "Los apellidos no pueden quedar en blanco.",
                    maxlength: "Los apellidos no pueden tener más de 50 caracteres.",
				},
				'person_procedence-genero': {
				    required: "Tiene que seleccionar un género.",
				},
				'person_procedence-genero-selectized': {
				    required: "Tiene que seleccionar un género.",
				},
				'person_procedence-email_address': {
				    email: "El email debe ser una dirección de correo electrónico válido.",
				},
				'person_procedence-movil': {
                    digits: "El movil solo puede tener dígitos.",
                    maxlength: "El movil no pueden tener más de 8 dígitos.",
                    minlength: "El movil no puede tener menos de 8 dígitos.",
                    remote: "Ya existe otra persona registrada con ese movil",
                },
				'person_procedence-telefono': {
				    required: "El teléfono no puede quedar en blanco.",
                    digits: "El teléfono solo puede tener dígitos.",
                    maxlength: "El teléfono no pueden tener más de 8 dígitos.",
                    minlength: "El teléfono no puede tener menos de 8 dígitos.",
				},
				'person_procedence-direccion_calle': {
				    required: "Tiene que seleccionar una calle.",
				},
				'person_procedence-direccion_calle-selectized': {
				    required: "Tiene que seleccionar una calle.",
				},
				'person_procedence-direccion_numero': {
				    required: "El número no puede quedar en blanco.",
				},
				'person_procedence-direccion_entrecalle1': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'person_procedence-direccion_entrecalle1-selectized': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'person_procedence-direccion_entrecalle2': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'person_procedence-direccion_entrecalle2-selectized': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'person_procedence-municipio': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'person_procedence-municipio-selectized': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'person_procedence-cpopular': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'person_procedence-cpopular-selectized': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'telefono-numero': {
				    required: "El núemro de teléfono no puede quedar en blanco.",
                    digits: "El núemro de teléfono solo puede tener dígitos.",
                    maxlength: "El núemro de teléfono no pueden tener más de 8 dígitos.",
                    minlength: "El núemro de teléfono no puede tener menos de 8 dígitos.",
				},
				'empresa-nombre': {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "El nombre no puede tener más de 100 caracteres.",
				},
				'empresa-sigla': {
				    required: "Las siglas no pueden quedar en blanco.",
                    maxlength: "Las siglas no pueden tener más de 10 caracteres.",
				},
				'empresa-telefono': {
				    required: "El teléfono no puede quedar en blanco.",
                    digits: "El teléfono solo puede tener dígitos.",
                    maxlength: "El teléfono no pueden tener más de 8 dígitos.",
                    minlength: "El teléfono no puede tener menos de 8 dígitos.",
				},
				'empresa-movil': {
                    digits: "El movil solo puede tener dígitos.",
                    maxlength: "El movil no pueden tener más de 8 dígitos.",
                    minlength: "El movil no puede tener menos de 8 dígitos.",
                },
				'empresa-nombre_contacto': {
				    required: "El nombre de contacto no puede quedar en blanco.",
				    maxlength: "El nombre de contacto no puede tener más de 200 caracteres.",
				},
				'empresa-email_address': {
				    email: "El email debe ser una dirección de correo electrónico válido.",
				},
				'empresa-codigo_nit': {
				    required: "El código NIT no puede quedar en blanco.",
				},
				'empresa-codigo_reuup': {
				    required: "El código REEUP no puede quedar en blanco.",
				},
				'empresa-municipio': {
				    required:  "Tiene que seleccionar un municipio.",
				},
				'empresa-cpopular': {
				    required:  "Tiene que seleccionar un consejo popular.",
				},
				'empresa-municipio-selectized': {
				    required:  "Tiene que seleccionar un municipio.",
				},
				'empresa-cpopular-selectized': {
				    required:  "Tiene que seleccionar un consejo popular.",
				},
				'empresa-direccion_calle': {
				    required: "Tiene que seleccionar una calle.",
				},
				'empresa-direccion_calle-selectized': {
				    required: "Tiene que seleccionar una calle.",
				},
				'empresa-direccion_numero': {
				    required: "El número no puede quedar en blanco.",
				},
				'empresa-direccion_entrecalle1': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'empresa-direccion_entrecalle1-selectized': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'empresa-direccion_entrecalle2': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'empresa-direccion_entrecalle2-selectized': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'gob-nombre': {
				    required: "El nombre no puede quedar en blanco.",
				    maxlength: "El nombre no puede tener más 50 caracteres.",
				},
				'organiza-nombre': {
				    required: "El nombre no puede quedar en blanco.",
				    maxlength: "El nombre no puede tener más 50 caracteres.",
				},
				'personas_list': {
				    required: "Tiene que seleccionar una persona de la lista.",
				},
				'personas_list-selectized': {
				    required: "Tiene que seleccionar una persona de la lista.",
				},
				'person_queja-ci': {
				    required: "El CI no puede quedar en blanco.",
				    digits: "El CI solo puede tener dígitos.",
                    maxlength: "El CI no puede tener más de 11 dígitos.",
                    minlength: "El CI no puede tener menos de 11 dígitos.",
				},
				'person_queja-nombre': {
				    required: "El nombre no puede quedar en blanco.",
                    maxlength: "Los apellidos no pueden tener más de 30 caracteres.",
				},
				'person_queja-apellidos': {
				    required: "Los apellidos no pueden quedar en blanco.",
                    maxlength: "Los apellidos no pueden tener más de 50 caracteres.",
				},
				'person_queja-genero': {
				    required: "Tiene que seleccionar un género.",
				},
				'person_queja-genero-selectized': {
				    required: "Tiene que seleccionar un género.",
				},
				'person_queja-email_address': {
				    email: "El email debe ser una dirección de correo electrónico válido.",
				},
				'person_queja-movil': {
                    digits: "El movil solo puede tener dígitos.",
                    maxlength: "El movil no pueden tener más de 8 dígitos.",
                    minlength: "El movil no puede tener menos de 8 dígitos.",
                    remote: "Ya existe otra persona registrada con ese movil",
                },
				'person_queja-telefono': {
				    required: "El teléfono no puede quedar en blanco.",
                    digits: "El teléfono solo puede tener dígitos.",
                    maxlength: "El teléfono no pueden tener más de 8 dígitos.",
                    minlength: "El teléfono no puede tener menos de 8 dígitos.",
                },
				'person_queja-direccion_calle': {
				    required: "Tiene que seleccionar una calle.",
				},
				'person_queja-direccion_calle-selectized': {
				    required: "Tiene que seleccionar una calle.",
				},
				'person_queja-direccion_numero': {
				    required: "El número no puede quedar en blanco.",
				},
				'person_queja-direccion_entrecalle1': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'person_queja-direccion_entrecalle1-selectized': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'person_queja-direccion_entrecalle2': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'person_queja-direccion_entrecalle2-selectized': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'person_queja-cpopular': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'person_queja-cpopular-selectized': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'person_queja-municipio': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'person_queja-municipio-selectized': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'queja-no_procendencia': {},
				'queja-no_radicacion': {},
				'queja-dir_calle': {
				    required: "Tiene que seleccionar una calle.",
				},
				'queja-dir_calle-selectized': {
				    required: "Tiene que seleccionar una calle.",
				},
				'queja-dir_num': {
				    required: "El número no puede quedar en blanco.",
				},
				'queja-dir_entrecalle1': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'queja-dir_entrecalle1-selectized': {
				    required: "Tiene que seleccionar una calle como primera entrecalle.",
				},
				'queja-dir_entrecalle2': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'queja-dir_entrecalle2-selectized': {
				    required: "Tiene que seleccionar una calle como segunda entrecalle.",
				},
				'queja-dir_municipio': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'queja-dir_municipio-selectized': {
				    required: "Tiene que seleccionar un municipio.",
				},
				'queja-dir_cpopular': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'queja-dir_cpopular-selectized': {
				    required: "Tiene que seleccionar un consejo popular.",
				},
				'queja-referencia': {},
				'queja-asunto': {
				    required: "Tiene que seleccionar un código de asunto.",
				},
				'queja-asunto-selectized': {
				    required: "Tiene que seleccionar un código de asunto.",
				},
				'queja-tipo': {
				    required: "Tiene que seleccionar un tipo de queja.",
				},
				'queja-tipo-selectized': {
				    required: "Tiene que seleccionar un tipo de queja.",
				},
				'queja-asunto_texto': {
				    required: "El texto del asunto no puede quedar en blanco.",
                    maxlength: "El texto del asunto no puede más de 300 caracteres.",
				},
				'queja-texto': {
				    required: "El cuerpo de la queja no puede quedar en blanco.",
                    maxlength: "El cuerpo de la queja no puede tener más de 3000 caracteres.",
                    minlength: "El cuerpo de la queja no puede tener menos de 20 caracteres.",
				},
				'queja-responder_a': {
				    required: "El responder a no puede quedar en blanco.",
				},
				'queja-responder_a-selectized': {
				    required: "El responder a no puede quedar en blanco.",
				},
			},
		});

		$('#id_pe-nombre').on('keypress', function (e) {
		    let params = {
		        name: 'nombre',
		        url: '/nomenclador/prensaescrita/autofill',
		        awesomplete: awesomplete1,
		    }
            _autofill_field(this, params);
		});
		$('#id_pe-siglas').on('keypress', function (e) {
		    let params = {
		        name: 'siglas',
		        url: '/nomenclador/prensaescrita/autofill',
		        awesomplete: awesomplete2,
		    }
            _autofill_field(this, params);
		});
		$('#id_person_procedence-ci').on('keypress', function (e) {
		    let params = {
		        name: 'ci',
		        url: '/persona/natural/autofill',
		        awesomplete: awesomplete3,
		    }
            _autofill_field(this, params);
		});
		$('#id_person_procedence-nombre').on('keypress', function (e) {
		    let params = {
		        name: 'nombre',
		        url: '/persona/natural/autofill',
		        awesomplete: awesomplete4,
		    }
            _autofill_field(this, params);
		});
		$('#id_person_procedence-apellidos').on('keypress', function (e) {
		    let params = {
		        name: 'apellidos',
		        url: '/persona/natural/autofill',
		        awesomplete: awesomplete5,
		    }
            _autofill_field(this, params);
		});
		$('#id_telefono-numero').on('keypress', function (e) {
		    let params = {
		        name: 'numero',
		        url: '/nomenclador/telefono/autofill',
		        awesomplete: awesomplete6,
		    }
            _autofill_field(this, params);
		});
		$('#id_email-email').on('keypress', function (e) {
		    let params = {
		        name: 'email',
		        url: '/nomenclador/email/autofill',
		        awesomplete: awesomplete7,
		    }
            _autofill_field(this, params);
		});
		$('#id_gob-nombre').on('keypress', function (e) {
		    let params = {
		        name: 'nombre',
		        url: '/nomenclador/gobierno/autofill',
		        awesomplete: awesomplete8,
		    }
            _autofill_field(this, params);
		});
		$('#id_organiza-nombre').on('keypress', function (e) {
		    let params = {
		        name: 'nombre',
		        url: '/nomenclador/organizacion/autofill',
		        awesomplete: awesomplete9,
		    }
            _autofill_field(this, params);
		});
		$('#id_empresa-nombre').on('keypress', function (e) {
		    let params = {
		        name: 'nombre',
		        url: '/persona/juridica/autofill',
		        awesomplete: awesomplete10,
		    }
            _autofill_field(this, params);
		});
		$('#id_empresa-sigla').on('keypress', function (e) {
		    let params = {
		        name: 'sigla',
		        url: '/persona/juridica/autofill',
		        awesomplete: awesomplete11,
		    }
            _autofill_field(this, params);
		});
		$('#id_empresa-codigo_nit').on('keypress', function (e) {
		    let params = {
		        name: 'codigo_nit',
		        url: '/persona/juridica/autofill',
		        awesomplete: awesomplete12,
		    }
            _autofill_field(this, params);
		});
		$('#id_empresa-codigo_reuup').on('keypress', function (e) {
		    let params = {
		        name: 'codigo_reuup',
		        url: '/persona/juridica/autofill',
		        awesomplete: awesomplete13,
		    }
            _autofill_field(this, params);
		});
		$('#id_person_procedence-ci').on('blur', function (e) {
		    let params = {
		        name: 'ci',
		        url: '/persona/natural/found',
		        object: 'person',
		        asigne: _asigne_person_procedence,
		    }
            _found_item(this, params);
		});
		$('#id_pe-nombre').on('blur', function (e) {
		    let params = {
		        name: 'nombre',
		        url: '/nomenclador/prensaescrita/found',
		        object: 'prensaescrita',
		        asigne: _asigne_pe,
		    }
            _found_item(this, params);

		});
		$('#id_empresa-codigo_nit').on('blur', function (e) {
		    let params = {
		        name: 'codigo_nit',
		        url: '/persona/juridica/found',
		        object: 'empresa',
		        asigne: _asigne_empresa,
		    }
            _found_item(this, params);

		});
		$('#id_empresa-codigo_reuup').on('blur', function (e) {
		    let params = {
		        name: 'codigo_reuup',
		        url: '/persona/juridica/found',
		        object: 'empresa',
		        asigne: _asigne_empresa,
		    }
            _found_item(this, params);

		});
		$('#id_empresa-nombre').on('blur', function (e) {
		    let params = {
		        name: 'nombre',
		        url: '/persona/juridica/found',
		        object: 'empresa',
		        asigne: _asigne_empresa,
		    }
            _found_item(this, params);

		});
		$('#id_empresa-sigla').on('blur', function (e) {
		    let params = {
		        name: 'sigla',
		        url: '/persona/juridica/found',
		        object: 'empresa',
		        asigne: _asigne_empresa,
		    }
            _found_item(this, params);

		});
		$('input[id$="-selectized"]').attr('name', function () {
            let name = this.id.slice(3);
            return name;
        });
        $('#id_same_quejoso').on('change', function (e) {
            if (this.checked) {
                $('#id_queja-damnificado_not_indb').click();
                $('#id_person_queja-ci').val($('#id_person_procedence-ci').val());
                $('#id_person_queja-nombre').val($('#id_person_procedence-nombre').val());
                $('#id_person_queja-apellidos').val($('#id_person_procedence-apellidos').val());
                $('#id_person_queja-email_address').val($('#id_person_procedence-email_address').val());
                $('#id_person_queja-telefono').val($('#id_person_procedence-telefono').val());
                $('#id_person_queja-direccion_numero').val($('#id_person_procedence-direccion_numero').val());
                $('#id_person_queja-movil').val($('#id_person_procedence-movil').val());
                //$('#id_person_queja-').val($('#id_person_procedence-').val());
                $('#id_person_queja-genero')[0].selectize.setValue($('#id_person_procedence-genero')[0].selectize.getValue() , false);
                $('#id_person_queja-direccion_calle')[0].selectize.setValue($('#id_person_procedence-direccion_calle')[0].selectize.getValue() , false);
                $('#id_person_queja-direccion_entrecalle1')[0].selectize.setValue($('#id_person_procedence-direccion_entrecalle1')[0].selectize.getValue() , false);
                $('#id_person_queja-direccion_entrecalle2')[0].selectize.setValue($('#id_person_procedence-direccion_entrecalle2')[0].selectize.getValue() , false);
                $('#id_person_queja-municipio')[0].selectize.setValue($('#id_person_procedence-municipio')[0].selectize.getValue() , false);
                $('#id_person_queja-cpopular')[0].selectize.setValue($('#id_person_procedence-cpopular')[0].selectize.getValue() , false);
                //$('#id_person_queja-')[0].selectize.setValue($('#id_person_procedence-')[0].selectize.getValue() , false);
            }
        });

		var _autofill_field = function (field, params) {
            let field_value = $(field).val();
            //console.log(field_value);
            if (field_value.length >= 3) {
                let data = new Object();
                data[params.name] = field_value;
                data['csrfmiddlewaretoken'] = $('[name="csrfmiddlewaretoken"]').val();
                $.ajax({
                    url: params.url,
                    type: 'POST',
                    dataType: 'json',
                    data: data,
                    success: function (json) {
                        // console.log(json)
                        _prepare_list(JSON.parse(JSON.stringify(json)), params.awesomplete);
                    },
                    error: function (xhr,errmsg,err) {
                        console.log(xhr,errmsg,err);
                    },
                });
            };
		};
        var _found_item = function (field, params) {
            let value_let = $(field).val();
            //console.log(value_let);
            if (value_let) {
                let data = new Object();
                data[params.name] = value_let;
                data['csrfmiddlewaretoken'] = $('[name="csrfmiddlewaretoken"]').val();
                $.ajax({
                    url: params.url,
                    type: 'POST',
                    dataType: 'json',
                    data: data,
                    success: function (json) {
                        // console.log(json);
                        let data = _prepare_data(json, params.object);
                        // console.log('data', data);
                        let accept="Usar estos datos";
                        let title="Aviso";
                        let plus=json;
                        tmp = json;
                        if (data) {
                            _makeAlert('info', data, params.asigne, null, title=title, accept=accept)
                        };
                    },
                    error: function (xhr,errmsg,err) {
                        console.log(xhr,errmsg,err);
                    },
                });
            };
        };
        var _prepare_data = function (json, item) {
            if (!json.exist) {
                return false;
            };
            let listilla = [];
            // console.log('prepare json', json);
            let model = json[item];
            // console.log('prepare_model', model);
            for(let key in model)
            {
                //console.log(key);
                if (key.search('direccion_') == -1  && key.search('municipio') == -1  && key.search('cpopular') == -1  &&  key.search('genero') == -1  )
                    listilla.push('<h6 class="text-left"><strong>'+key+': </strong>'+model[key]+'</h6>');
            }
            // console.log(listilla);
            return 'Coincidencia encontrada:<br>'.concat(listilla.join("")).concat('<br><p>Desea rellenar el formulario con estos datos si son correctos:</p>.');
        };

		var _prepare_list = function (list, awesomplete) {
		    // console.log(list);
            let c_list = [];
            //console.log(awesomplete);
            if (list.length > 0) {

                let field = awesomplete.input.name.split('-')[1]
                //console.log('field', field);
                list.forEach(item => {
                    c_list.push(item[field]);
                });
                awesomplete.list = c_list;
            }
        };
        var _asigne_person_procedence = function (data) {
            //console.log(data);
            $("#id_person_procedence-ci").val(data.person.ci);
            $("#id_person_procedence-nombre").val(data.person.nombre);
            $("#id_person_procedence-apellidos").val(data.person.apellidos);
            $("#id_person_procedence-email_address").val(data.person.email_address);
            $("#id_person_procedence-movil").val(data.person.movil);
            $("#id_person_procedence-telefono").val(data.person.telefono);
            $("#id_person_procedence-direccion_numero").val(data.person.direccion_numero);
            //$("#").val(data.person.);
            $("#id_person_procedence-genero")[0].selectize.setValue(data.person.genero, false);
            $("#id_person_procedence-direccion_calle")[0].selectize.setValue(data.person.direccion_calle, false);
            $("#id_person_procedence-direccion_entrecalle1")[0].selectize.setValue(data.person.direccion_entrecalle1, false);
            $("#id_person_procedence-direccion_entrecalle2")[0].selectize.setValue(data.person.direccion_entrecalle2, false);
            $("#id_person_procedence-municipio")[0].selectize.setValue(data.person.municipio, false);
            $("#id_person_procedence-cpopular")[0].selectize.setValue(data.person.cpopular, false);
            //$("#")[0].selectize.setValue(data.person., false);
            //$('.form-control').trigger('change');
            // console.log(data);
            tmp = null;
        };
        var _asigne_pe = function (data) {
            //alert(data);
            // console.log(data);
            $("#id_pe-nombre").val(data.prensaescrita.nombre);
            $("#id_pe-siglas").val(data.prensaescrita.siglas);
            tmp = null;
        };
        var _asigne_empresa = function (data) {
            //alert(data);
            //console.log(data);
            $("#id_empresa-nombre").val(data.empresa.nombre);
            $("#id_empresa-sigla").val(data.empresa.sigla);
            $("#id_empresa-codigo_nit").val(data.empresa.codigo_nit);
            $("#id_empresa-codigo_reuup").val(data.empresa.codigo_reuup);
            $("#id_empresa-direccion_numero").val(data.empresa.direccion_numero);
            $("#id_empresa-telefono").val(data.empresa.telefono);
            $("#id_empresa-movil").val(data.empresa.movil);
            $("#id_empresa-nombre_contacto").val(data.empresa.nombre_contacto);
            $("#id_empresa-email_address").val(data.empresa.email_address);
            //$("#").val();
            $("#id_empresa-municipio")[0].selectize.setValue(data.empresa.municipio, false);
            $("#id_empresa-cpopular")[0].selectize.setValue(data.empresa.cpopular, false);
            $("#id_empresa-direccion_calle")[0].selectize.setValue(data.empresa.direccion_calle, false);
            $("#id_empresa-direccion_entrecalle2")[0].selectize.setValue(data.empresa.direccion_entrecalle2, false);
            $("#id_empresa-direccion_entrecalle1")[0].selectize.setValue(data.empresa.direccion_entrecalle1, false);
            tmp = null;
        };

		// validator_form.resetForm();
    };
    var _initQuejaAsignaForm = function () {
        var $personas_list = $('#id_tecnico').selectize({
            create: false,
            maxItems: 1,
            placeholder: "Selecione un técnico",
            allowEmptyOption: false,
        });

        $.validator.setDefaults({
            errorClass: 'text-danger',
            highlight: function(element) {
                $(element).addClass('is-invalid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },
            // Validate only visible fields
			ignore: ":hidden",

            errorPlacement: function(error, element) {
                if (element[0].attributes['type']) {
                    if (element[0].attributes['type'].nodeValue == 'select-one' || element[0].attributes['type'].nodeValue == 'select-multiple')
                        error.insertBefore(element.parent());
                    else
                        error.insertBefore(element);
                } else {
                    error.insertBefore(element);
                }
            },

        });
        let validator_form = asigne_form.validate({
			rules: {
				tecnico: {
				    required: true,
				},
				observaciones: {
                    maxlength: 500,
				},
			},
			messages:{
				tecnico: {
				    required: "Tiene que seleccionar un técnico.",
				},
				observaciones: {
                    maxlength: "las observaciones no puede tener más de 500 caracteres.",
				},
            },
		});
    };
    var _initResponse = function () {
        $("#show_form").on("click", function (e) {
            $("#show_detail").removeClass("my-hidden");

            $("#show_form").addClass("my-hidden");
            $("#show_form_div").removeClass("my-hidden");
            $("#show_detail_div").addClass("my-hidden");
            if ($('button[type="submit"]').hasClass("disabled")) $('button[type="submit"]').removeClass("disabled");
        });
        $("#show_detail").on("click", function (e) {
            $("#show_detail").addClass("my-hidden");
            $("#show_form").removeClass("my-hidden");
            $("#show_form_div").addClass("my-hidden");
            $("#show_detail_div").removeClass("my-hidden");
            $('button[type="submit"]').addClass("disabled");
        });
    };
    var _initResponseForm = function () {
        $.validator.setDefaults({
            errorClass: 'text-danger',
            highlight: function(element) {
                $(element).addClass('is-invalid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },
            // Validate only visible fields
			ignore: ":hidden",

            errorPlacement: function(error, element) {
                error.insertBefore(element);
            },

        });
        let validator_form = response_form.validate({
			rules: {
				'gestion': {
				    required: true,
                    maxlength: 3000,
                    minlength: 20,
				},
				'texto': {
				    required: true,
                    maxlength: 3000,
                    minlength: 20,
				},
			},
			messages:{
				'gestion': {
				    required: "No puede dejar texto de la gestion en blanco.",
                    maxlength: "El texto de la gestion no puede tener mas de 3000 caracteres.",
                    minlength: "El texto de la gestion no puede tener menos de 20 caracteres.",
				},
				'texto': {
				    required: "No puede dejar el texto de la respuesta en blanco.",
                    maxlength: "El texto de la respuesta no puede tener mas de 3000 caracteres.",
                    minlength: "El texto de la respuesta no puede tener menos de 20 caracteres.",
				},
			},
		});
    };

    return {
        init: function () {
            _initQuejas();
        },
        initForm: function () {
            queja_form = $("#queja_form");
            _initTabWizard();
            _initQuejaForm();
        },
        initAsigneTech: function () {
            asigne_form = $("#form_asig_tecnico");
            _initQuejaAsignaForm();
        },
        initResponse: function () {
            response_form = $("#response_form");
            _initResponse();
            _initResponseForm();
        },
    };
}();

jQuery(document).ready(function() {
    DPVQuejas.init();
});