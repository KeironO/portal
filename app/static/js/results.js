$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip()
    var get_url = window.location.href + "/get";


    // Populate results table, alpha.
    $.getJSON(get_url, function(data) {
        var predictions = data["_items"];
        chart(predictions);
        populateTable(predictions);
        resultsShow(500, true);

        $("input[type=radio][name=optionsRadios]").change(function() {
            resultsHide(100, false);
            var qcPredictions = limitPredictions(predictions, this.value);
            chart(qcPredictions);
            populateTable(qcPredictions);
            resultsShow(100, false);
        });
    });

    function resultsHide(timing, loading) {
      $("#generated-results").fadeOut(timing);
      if (loading == true) {
          $("#loading-screen").fadeIn(timing);
      }

    }

    function resultsShow(timing, loading) {
      if (loading == true) {
        $("#loading-screen").fadeOut(timing);
      }
      $("#generated-results").fadeIn(timing);

    }

    function limitPredictions(predictions, qcValue) {
        var limits = {
            "none": 0.0,
            "low": 0.5,
            "medium": 0.7,
            "high": 0.85,
            "ridiculous": 0.9
        }

        new_predictions = []

        predictions.forEach(function(result) {
            var qc_ed = []

            result["predictions"].forEach(function(pred) {

                if (pred[1] > limits[qcValue]) {
                    qc_ed.push(pred);
                } else {
                    return false; // End assignment.
                }

            });
            new_predictions.push({
                "seq_id": result["seq_id"],
                "predictions": qc_ed
            })
        });
        return new_predictions
    }


    function populateTable(predictions) {
        $("#results-table").DataTable({
            "destroy": true,
            "data": predictions,
            "pageLength": 10,
            "dom": 'Bfrtip',
            "buttons": [
              "copy", "csv", "excel", "pdf", "print"
            ],
            "columns": [{
                    "title": "Sequence ID",
                    "data": "seq_id",
                    "width": "20%"
                },
                {
                    "title": "Assignment",
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

    }

    function cleanPredictions(predictions) {
        var cleanPredictions = {}

        predictions.forEach(function(sequence) {
            var preds = sequence["predictions"];
            var cleanedPreds = []
            preds.forEach(function(p) {
                if (p[0] != "null") {
                    cleanedPreds.push(p[0]);
                }
            });
            cleanPredictions[sequence["seq_id"]] = cleanedPreds.join("; ");
        });

        return Object.values(cleanPredictions);

    }


    function chart(predictions) {
        var clearedPredictions = cleanPredictions(predictions);
        var counts = {};
        clearedPredictions.forEach(function(sequence) {
            if (sequence in counts) {
                counts[sequence] += 1
            } else {
                counts[sequence] = 1
            }
        });

        var data = [{
            type: "bar",
            y: Object.values(counts),
            x: Object.keys(counts),
            orientation: "v"
        }];

        var layout = {
            xaxis: {

                autotick: true,
                autorange: true,
                showticklabels: false
            }
        }

        Plotly.newPlot("results-plot", data, layout)
    }


});