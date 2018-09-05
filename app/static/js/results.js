$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip()
    var get_url = window.location.href + "/get";


    // Populate results table, alpha.
    $.getJSON(get_url, function(data) {
        var predictions = data["_items"];
        chart(predictions, 3);
        $("#results-table").DataTable({
            "data": predictions,
            "pageLength": 10,
            "columns": [{
                    "title": "Sequence ID",
                    "data": "seq_id"
                },
                {
                    "title": "Results",
                    "data": "predictions",
                    "render": function(data, type, row) {
                        var final_str = ""
                        for (i in data) {
                            var prediction = data[i];
                            if (prediction[0] != "null") {
                                final_str += '<span data-toggle="tooltip" data-placement="top" title="Confidence Value: ' + prediction[1] * 100 + '%">' + prediction[0] + '; </span>'
                            }
                        }
                        return final_str
                    }
                }
            ]
        });
    });


    function chart(predictions, index) {
        var counts = {};
        predictions.forEach(function(sequence) {
            var pred = sequence["predictions"][index];
            if (pred[0] in counts) {
                counts[pred[0]] += 1
            } else {
                counts[pred[0]] = 1
            }
        });
        var bcs = palette('tol', Object.keys(counts).length).map(function(hex) {
              return '#' + hex;
            });

        console.log(bcs, typeof bcs, Object.values(bcs));

        var ctx = document.getElementById("myChart");
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(counts),
                datasets: [{
                    label: '# of Annotations',
                    data: Object.values(counts),
                    backgroundColor: Object.values(bcs)
                }],

            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }

});