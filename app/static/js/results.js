$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip()
    var get_url = window.location.href + "/get";


    // Populate results table, alpha.
    $.getJSON(get_url, function(data) {
        var predictions = data["_items"];
        chart(predictions, 0);
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

    function cleanPredictions(predictions) {
        var cleanPredictions = { }

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
            }

            else {
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