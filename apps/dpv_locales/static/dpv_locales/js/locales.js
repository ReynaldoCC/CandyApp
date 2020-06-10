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


const DPVLocal = function () {
    let local_form;
    let tmp;
    let validator_form;

    const _makeAlert = function(type, text, success, negate, title=null, accept=null, cancel=null, plus=null) {
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
                }
            } else {
                if (negate != null) {
                    negate(dataplus);
                }
            }
        });
    };
    const _initLocalPane = function (translations) {
        $('#local-table').DataTable({
            responsive: true,
            order: [ 0, 'desc' ],
            sScrollX: "100%",
            language: {
                "decimal": "",
                "emptyTable": translations.emptyTable,
                "info": translations.info_init + " _START_ a _END_ de _TOTAL_ " + translations.info_end,
                "infoEmpty": translations.infoEmpty,
                "infoFiltered": "(" + translations.infoFiltered_init + " _MAX_ " + translations.infoFiltered_end + ")",
                "infoPostFix": "",
                "thousands": ",",
                "lengthMenu": translations.lengthMenu_init + " _MENU_ " + translations.lengthMenu_end,
                "loadingRecords": translations.loadingRecords,
                "processing": translations.processing,
                "search":  translations.search,
                "zeroRecords": translations.zeroRecords,
                "paginate": {
                        "first": translations.first,
                        "last": translations.last,
                        "next": translations.next,
                        "previous": translations.previous,
                }
            },
        });
    };
    const _initLocalStatistics = function (translations, graph_data) {
        $('#stats-table').DataTable({
            responsive: true,
            order: [ 0, 'desc' ],
            sScrollX: "100%",
            lengthMenu: [[20, 50, -1], [20, 50, "Todos"]],
            language: {
                "decimal": "",
                "emptyTable": translations.emptyTable,
                "info": translations.info_init + " _START_ a _END_ de _TOTAL_ " + translations.info_end,
                "infoEmpty": translations.infoEmpty,
                "infoFiltered": "(" + translations.infoFiltered_init + " _MAX_ " + translations.infoFiltered_end + ")",
                "infoPostFix": "",
                "thousands": ",",
                "lengthMenu": translations.lengthMenu_init + " _MENU_ " + translations.lengthMenu_end,
                "loadingRecords": translations.loadingRecords,
                "processing": translations.processing,
                "search":  translations.search,
                "zeroRecords": translations.zeroRecords,
                "paginate": {
                        "first": translations.first,
                        "last": translations.last,
                        "next": translations.next,
                        "previous": translations.previous,
                }
            },
        });
        // console.log(graph_data);
        if (graph_data && graph_data.count > 0) {
            $(window).on('load', function () {
                var canvas = $('#Graph_result');
                new Chart(canvas, {
                    type: 'bar',
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            position: 'top',
                            text: 'Gráfico de Locales'
                        },
                        scales: {
                            yAxes: [{
                                id: 'left',
                                type: 'linear',
                                position: 'left',
                                ticks: {
                                    min: 0,
                                }
                            }, {
                                id: 'right',
                                type: 'linear',
                                position: 'right',
                                ticks: {
                                    min: 0,
                                }
                            }]
                        }
                    },
                    data: {
                        labels: graph_data.columns,
                        datasets: [{
                            label: 'Locales',
                            yAxisID: 'right',
                            data: graph_data.locales,
                            backgroundColor: "#007bff80",
                            borderColor: "#007bff",
                            borderWidth: 1,
                        }, {
                            label: 'Estatales',
                            yAxisID: 'right',
                            data: graph_data.estatales,
                            backgroundColor: "#28a74580",
                            borderColor: "#28a745",
                            borderWidth: 1,
                        }, {
                            label: 'Esfuerzo Propio',
                            yAxisID: 'right',
                            data: graph_data.propios,
                            backgroundColor: "#ffc10780",
                            borderColor: "#ffc107",
                            borderWidth: 1,
                        }, {
                            label: 'Viviendas',
                            yAxisID: 'right',
                            data: graph_data.vivtotal,
                            backgroundColor: "#dc354580",
                            borderColor: "#dc3545",
                            borderWidth: 1,
                        }, {
                            label: 'Viviendas Pendientes de Aprobación',
                            yAxisID: 'right',
                            data: graph_data.vivpend,
                            backgroundColor: "#753ede80",
                            borderColor: "#753ede",
                            borderWidth: 1,
                        }, {
                            label: 'Viviendas con Datos',
                            yAxisID: 'right',
                            data: graph_data.vivasoc,
                            backgroundColor: "#de933e80",
                            borderColor: "#de933e",
                            borderWidth: 1,
                        }, {
                            label: 'Total Personas',
                            yAxisID: 'left',
                            data: graph_data.personas,
                            type: 'line',
                            backgroundColor: "#007bff00",
                            borderColor: "#007bff",
                            borderWidth: 3,
                        }, {
                            label: 'Total Mujeres',
                            yAxisID: 'left',
                            data: graph_data.mujeres,
                            type: 'line',
                            backgroundColor: "#28a74500",
                            borderColor: "#28a745",
                            borderWidth: 3,
                        }, {
                            label: 'Total Menores de Edad',
                            yAxisID: 'left',
                            data: graph_data.menores,
                            type: 'line',
                            backgroundColor: "#ffc10700",
                            borderColor: "#ffc107",
                            borderWidth: 3,
                        }, {
                            label: 'Total de Discapacitados',
                            yAxisID: 'left',
                            data: graph_data.aclifim,
                            type: 'line',
                            backgroundColor: "#dc354500",
                            borderColor: "#dc3545",
                            borderWidth: 3,
                        }, {
                            label: 'Total Personas de 3ra Edad',
                            yAxisID: 'left',
                            data: graph_data.ancianos,
                            type: 'line',
                            backgroundColor: "#753ede00",
                            borderColor: "#753ede",
                            borderWidth: 3,
                        }]
                    },
                });
            });
        }
    };
    const _initLocalForm = function () {

        let $pj_municipio = $("#id_municipio").selectize({
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
        let $pj_cpopular = $("#id_consejo_popular").selectize({
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
        let $pj_direccion_calle = $("#id_direccion_calle").selectize({
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
        let $pj_direccion_entrecalle2 = $("#id_direccion_entre2").selectize({
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
        let $pj_direccion_entrecalle1 = $("#id_direccion_entre1").selectize({
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
        let $pj_piso = $("#id_piso").selectize({
            create: false,
            placeholder: "Selecione un piso",
            allowEmptyOption: false,
        });
        let $pj_organismo = $("#id_organismo").selectize({
            create: false,
            placeholder: "Selecione un organismo",
            allowEmptyOption: false,
        });

        const _fill_selectizes_with_values = function () {
            if ($("#id_municipio").val())
                $pj_municipio[0].selectize.setValue($("#id_municipio").val());
            if ($("#id_consejo_popular").val())
                $pj_cpopular[0].selectize.setValue($("#id_consejo_popular").val());
            if ($("#id_direccion_calle").val())
                $pj_direccion_calle[0].selectize.setValue($("#id_direccion_calle").val());
            if ($("#id_direccion_entre1").val())
                $pj_direccion_entrecalle1[0].selectize.setValue($("#id_direccion_entre1").val());
            if ($("#id_direccion_entre2").val())
                $pj_direccion_entrecalle2[0].selectize.setValue($("#id_direccion_entre2").val());
            if ($("#id_piso").val())
                $pj_piso[0].selectize.setValue($("#id_piso").val());
            if ($("#id_organismo").val())
                $pj_organismo[0].selectize.setValue($("#id_organismo").val());
        };
        $.validator.setDefaults({
            errorClass: 'text-danger',
            highlight: function(element) {
                $(element).addClass('is-invalid');
            },
            unhighlight: function(element) {
                $(element).removeClass('is-invalid');
            },

			ignore: ":hidden:not([class~=selectized]),:hidden > .selectized, .selectize-control .selectize-input input",

            errorPlacement: function(error, element) {
                if (element[0].attributes['type'].nodeValue === 'select-one' || element[0].attributes['type'].nodeValue === 'select-multiple')
                    error.insertBefore(element.parent());
                else
                    error.insertBefore(element);
            },

        });
        $.validator.addMethod('smalleThan', function( value, element, param ) {

			//console.log('distinctTo', param);
			var target = $( param );
			if ( this.settings.onfocusout && target.not( ".validate-smalleThan-blur" ).length ) {
				target.addClass( "validate-smalleThan-blur" ).on( "blur.validate-smalleThan", function() {
					$( element ).valid();
				} );
			}
			return parseInt(value) <= parseInt(target.val());
		}, 'El valor debe de este campo ser menor o igual que ');
        $.validator.addMethod('myNotEqualTo', function( value, element, param ) {

			// console.log('distinctTo', param);
			var target = $( param );
			// console.log('distinctTo', target);
			if ( this.settings.onfocusout && target.not( ".validate-notEqualTo-blur" ).length ) {
				target.addClass( "validate-notEqualTo-blur" ).on( "blur.validate-notEqualTo", function() {
					$( element ).valid();
				} );
			}
			return value !== target.val();
		}, 'Ese no puede ser el valor de este campo.');
        $.validator.addMethod('bigeThan', function( value, element, param ) {

			var target = $( param );
			if ( this.settings.onfocusout && target.not( ".validate-bigeThan-blur" ).length ) {
				target.addClass( "validate-bigeThan-blur" ).on( "blur.validate-bigeThan", function() {
					$( element ).valid();
				} );
			}
			return parseInt(value) >= parseInt(target.val());
		}, 'El valor debe de este campo ser mayor o igual que ');
        $.validator.addMethod('actaAcuerdo', function(value, element) {
            return this.optional(element) || /^[0-9]+[/]([0-9]{2}|[0-9]{4})$/i.test(value);
        }, 'El número de un acta o acuerdo debe tener esta nomenclatura xxxx/xx ó xxxx/xxxx');
        $.validator.addMethod('notFutureYear', function(value, element) {
            let isnotFuture = true;
            let year = value.split('/').pop();
            let today = new Date();
            console.log('anno', year);
            if (year.length === 2) {
                if (parseInt('20'.concat(year)) > today.getFullYear())
                    isnotFuture = false;
            } else if (year.length === 4){
                if (year > today.getFullYear())
                    isnotFuture = false;
            }
            return this.optional(element) || isnotFuture;
        }, 'El año del número  no puede estar en el futuro, solo pasado y presente');
        validator_form = local_form.validate({
			rules: {
				municipio: {
				    required: true,
                    remote: {
                        url: '/local/verify',
                        type: 'GET',
                        data: {
                            id: local_id,
                            direccion_calle: $("#id_direccion_calle").val(),
                            direccion_numero: $("#id_direccion_numero").val(),
                        },
                    },
				},
				direccion_numero: {
				    required: true,
                    remote: {
                        url: '/local/verify',
                        type: 'GET',
                        data: {
                            id: local_id,
                            direccion_calle: $("#id_direccion_calle").val(),
                            municipio: $("#id_municipio").val(),
                        },
                    },
				},
				consejo_popular: {
				    required: true,
				},
				direccion_entre1: {
				    required: true,
                    myNotEqualTo: "#id_direccion_entre2",
				},
				direccion_calle: {
				    required: true,
                    myNotEqualTo: "#id_direccion_entre1",
                    remote: {
                        url: '/local/verify',
                        type: 'GET',
                        data: {
                            id: local_id,
                            municipio: $("#id_municipio").val(),
                            direccion_numero: $("#id_direccion_numero").val(),
                        },
                    },
				},
				direccion_entre2: {
				    required: true,
                    myNotEqualTo: "#id_direccion_calle",
				},
				piso: {
				    required: true,
				},
				no_viviendas: {
				    min: 1,
                    digits: true,
				    required: true,
                    bigeThan: "#id_pendiente",
				},
				pendiente: {
				    required: true,
                    digits: true,
                    min: 0,
                    smalleThan: "#id_no_viviendas",
				},
				organismo: {
				    required: true,
				},
				acta: {
				    required: false,
                    actaAcuerdo: true,
                    notFutureYear: true,
                    require_from_group: [1, ".acta-group"],
				},
				acuerdoCAM: {
				    required: false,
                    actaAcuerdo: true,
                    notFutureYear: true,
                    require_from_group: [1, ".acta-group"],
                },
				acuerdoPEM: {
				    required: false,
                    actaAcuerdo: true,
                    notFutureYear: true,
                    require_from_group: [1, ".acta-group"],
                },
                acuerdoORG: {
				    required: false,
                    actaAcuerdo: true,
                    notFutureYear: true,
                    require_from_group: [1, ".acta-group"],
                },
                acuerdo_DPV: {
				    required: false,
                    actaAcuerdo: true,
                    notFutureYear: true,
                    require_from_group: [1, ".acta-group"],
                },
                observaciones: {
				    required: true,
                    maxlength: 600,
                },
                estatal: {
				    required: false,
                },
                aprobado: {
				    required: false,
                },
			},
			messages: {
				municipio: {
				    required: 'Tiene que seleccionar un municipio.',
                    remote: 'Ya existe otro local registrado con esa misma dercción(Municipio + Calle + Número).',
				},
				direccion_numero: {
				    required: 'El número de la dirección no puede quedar en blanco.',
                    remote: 'Ya existe otro local registrado con esa misma dercción(Municipio + Calle + Número).',
				},
				consejo_popular: {
				    required: 'Tiene que seleccionar un consejo popular.',
				},
				direccion_entre1: {
				    required: 'Tiene que seleccionar una primera entrecalle.',
                    distinctTo: 'la primera entrecalle no puede ser igual a la segunda entrecalle.',
				},
				direccion_calle: {
				    required: 'Tiene que seleccionar una calle.',
                    remote: 'Ya existe otro local registrado con esa misma dercción(Municipio + Calle + Número).',
                    distinctTo: 'la calle no puede ser igual a la primera entrecalle.',
				},
				direccion_entre2: {
				    required: 'Tiene que seleccionar una segunda entrecalle.',
                    distinctTo: 'La segunda entrecalle no puede ser igual a la calle.',
				},
				piso: {
				    required: 'Tiene que seleccionar un piso.',
				},
				no_viviendas: {
				    min: 'El número de viviendas no puede ser menor que 1.',
                    digits: 'El número de viviendas solo puede contener dígitos.',
				    required: 'El número de viviendas no puede quedar en blanco.',
                    bigeThan: "El número de viviendas no puede ser menor que  la cantidad de viviendas pendientes de aprobación",
				},
				pendiente: {
				    required: 'El número de viviendas pendientes de aprobación no puede quedar en blanco.',
                    digits: 'El número de viviendas pendientes de aprobación solo puede contener dígitos.',
                    min: 'El número de viviendas pendientes de aprobación no puede ser menor que 0.',
                    smalleThan: "El número de viviendas pendientes de aprobación no puede ser mayor que la cantidad de viviendas del local",
				},
				organismo: {
				    required: 'Tiene que seleccionar un organismo.',
				},
				acta: {
                    require_from_group: 'Tiene poner al menos un número de acta o acuerdo.',
				},
				acuerdoCAM: {
                    require_from_group:  'Tiene poner al menos un número de acta o acuerdo.',
                },
				acuerdoPEM: {
                    require_from_group: 'Tiene poner al menos un número de acta o acuerdo.',
                },
                acuerdoORG: {
                    require_from_group: 'Tiene poner al menos un número de acta o acuerdo.',
                },
                acuerdo_DPV: {
                    require_from_group: 'Tiene poner al menos un número de acta o acuerdo.',
                },
                observaciones: {
				    required: true,
                    maxlength: 600,
                },
                estatal: {
				    required: false,
                },
                aprobado: {
				    required: false,
                },
			},
		});

        _fill_selectizes_with_values();
    };

    return {
        init: function (translations) {
            _initLocalPane(translations);
        },
        initForm: function () {
            local_form = $("#local-form");
            _initLocalForm();
        },
        initStats: function (translations, graph_data) {
            _initLocalStatistics(translations, graph_data);
        },
    };
}();