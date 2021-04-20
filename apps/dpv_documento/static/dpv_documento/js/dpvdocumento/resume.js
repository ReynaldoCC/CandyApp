( function ( $ ) {
    "use strict";

    var CHART_COLORS = {
        blue: 'rgb(54, 162, 235)',
        orange: 'rgb(255, 159, 64)',
        purple: 'rgb(153, 102, 255)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        red: 'rgb(255, 99, 132)',
        grey: 'rgb(201, 203, 207)',
    };

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url : "/docs/resumen/",
        type : "POST",
        headers:{
            "X-CSRFToken": csrftoken
        },
        success : function(response) {
            $('#id_resume_first_targets').html('');

            $.each(response.first_targets, function(key, val) {

                $('#id_resume_first_targets').append('\
                    <div class="col-sm-6 col-lg-3">\
                        <div class="card text-white bg-flat-color-' + val.color + '">\
                            <div class="card-body pb-0">\
                                <h4 class="mb-0">\
                                    <span class="count">' + val.total + '</span>\
                                </h4>\
                                <p class="text-light">' + val.title + '</p>\
                                <div class="chart-wrapper px-0" style="height:70px;" height="70">\
                                    <canvas id="widgetChart' + key + '"></canvas>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                ');

                // //WidgetChart
                var ctx = document.getElementById( "widgetChart" + key );
                ctx.height = 150;
                var myChart = new Chart( ctx, {
                    type: val.data.type,
                    data: {
                        labels: val.data.labels,
                        type: val.data.type,
                        datasets: [ {
                            data: val.data.datasets.data,
                            label: val.data.datasets.label,
                            backgroundColor: 'transparent',
                            borderColor: 'rgba(255,255,255,.55)',
                        }, ]
                    },
                    options: {

                        maintainAspectRatio: false,
                        legend: {
                            display: false
                        },
                        responsive: true,
                        tooltips: {
                            mode: 'index',
                            titleFontSize: 12,
                            titleFontColor: '#000',
                            bodyFontColor: '#000',
                            backgroundColor: '#fff',
                            titleFontFamily: 'Montserrat',
                            bodyFontFamily: 'Montserrat',
                            cornerRadius: 3,
                            intersect: false,
                        },
                        scales: {
                            xAxes: [ {
                                gridLines: {
                                    color: 'transparent',
                                    zeroLineColor: 'transparent'
                                },
                                ticks: {
                                    fontSize: 2,
                                    fontColor: 'transparent'
                                }
                            } ],
                            yAxes: [ {
                                display:false,
                                ticks: {
                                    display: false,
                                }
                            } ]
                        },
                        title: {
                            display: false,
                        },
                        elements: {
                            line: {
                                borderWidth: 1
                            },
                            point: {
                                radius: 4,
                                hitRadius: 10,
                                hoverRadius: 4
                            }
                        }
                    }
                } );

            });

            $('#id_resume_second_targets').html('');

            $.each(response.second_targets, function (key, val) {

                $('#id_resume_second_targets').append('\
                    <div class="col-xl-3 col-lg-6">\
                        <div class="card">\
                            <div class="card-body">\
                                <div class="stat-widget-one">\
                                    <div class="stat-icon dib"><i class="ti-' + val.icon + ' text-' + val.color + ' border-' + val.color + '"></i></div>\
                                    <div class="stat-content dib">\
                                        <div class="stat-text">' + val.title + '</div>\
                                        <div class="stat-digit">' + val.total + '</div>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                ');

            });

            var chartDocsClass = new Chart( document.getElementById( "chartDocsClass" ), {
                type: 'doughnut',
                data: {
                    labels: [],
                    datasets: [
                        {
                          label: 'Total',
                          data: [],
                          backgroundColor: Object.values(CHART_COLORS)
                      }
                  ]
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        fontSize: 18,
                        text: 'Documentos por clasificación'
                    }
                }
            } );

            $.each(response.chartDocsClass, function (key, val) {
                chartDocsClass.data.labels.push(val.title);
                chartDocsClass.data.datasets[0].data.push(val.value);
            });

            chartDocsClass.update();

            var chartDocsOrig = new Chart( document.getElementById( "chartDocsOrig" ), {
                type: 'horizontalBar',
                data: {
                    labels: [],
                    datasets: [
                        {
                          label: 'Total',
                          data: [],
                          backgroundColor: Object.values(CHART_COLORS)
                      }
                  ]
                },
                options: {
                    responsive: true,
                    legend: {
                        display: false
                    },
                    scales: {
                        xAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    },
                    title: {
                        display: true,
                        fontSize: 18,
                        text: 'Documentos por procedencias'
                    }
                }
            });

            $.each(response.chartDocsOrig, function (key, val) {
                chartDocsOrig.data.labels.push(val.title);
                chartDocsOrig.data.datasets[0].data.push(val.value);
            });

            chartDocsOrig.update();

            var chartDocsAnswers = new Chart( document.getElementById( "chartDocsAnswers" ), {
                type: 'horizontalBar',
                data: {
                    labels: [],
                    datasets: [
                        {
                          label: 'Total',
                          data: [],
                          backgroundColor: Object.values(CHART_COLORS)
                      }
                  ]
                },
                options: {
                    responsive: true,
                    legend: {
                        display: false
                    },
                    scales: {
                        xAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    },
                    title: {
                        display: true,
                        fontSize: 18,
                        text: 'Documentos con respuestas'
                    }
                }
            });

            $.each(response.chartDocsAnswers, function (key, val) {
                chartDocsAnswers.data.labels.push(val.title);
                chartDocsAnswers.data.datasets[0].data.push(val.value);
            });

            chartDocsAnswers.update();

            var chartDocsTime = new Chart( document.getElementById( "chartDocsTime" ), {
                type: 'pie',
                data: {
                    labels: [],
                    datasets: [
                        {
                          label: 'Total',
                          data: [],
                          backgroundColor: Object.values(CHART_COLORS)
                      }
                  ]
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        fontSize: 18,
                        text: 'Documentos en fecha termino'
                    }
                }
            });

            $.each(response.chartDocsTime, function (key, val) {
                chartDocsTime.data.labels.push(val.title);
                chartDocsTime.data.datasets[0].data.push(val.value);
            });

            chartDocsTime.update();
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });


} )( jQuery );