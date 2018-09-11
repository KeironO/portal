$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip()
    var get_url = window.location.href + "/get";


    // Populate results table, alpha.
    $.getJSON(get_url, function(data) {
        var predictions = data["_items"];
        chart(predictions);
        populateTable(predictions, "none");
        renderTree("none");
        resultsShow(500, true);


        $("input[type=radio][name=optionsRadios]").change(function() {
            resultsHide(100, false);
            var qcPredictions = limitPredictions(predictions, this.value);
            chart(qcPredictions);
            populateTable(qcPredictions, this.value);
            renderTree(this.value);
            resultsShow(100, false);

        });
    });

    function renderTree(qcValue) {
        var limits = {
            "none": 0.0,
            "low": 0.5,
            "medium": 0.7,
            "high": 0.85,
            "ridiculous": 0.97
        }

        var limit_value = limits[qcValue];

        var tree_url = window.location.href + "/tree/" + limit_value.toString();

        var m = [20, 120, 20, 120]
        var w = 800 - m[-1] - m[3]
        var h = 500 - m[0] - m[2]
        var i = 0;
        var root;

        var tree = d3.layout.tree().size([h, w])

        var diagonal = d3.svg.diagonal()
            .projection(function(d) {
                return [d.y, d.x];
            });

        d3.select("#tree svg").remove();
        var vis = d3.select("#tree").append("svg:svg")
            .attr("width", w + m[1] + m[3])
            .attr("height", h + m[0] + m[2])
            .append("svg:g")
            .attr("transform", "translate(" + m[3] + "," + m[0] + ")");
        console.log(window.location.href.replace("testtree", "tree"));
        d3.json(tree_url, function(json) {
            root = json;
            root.x0 = h / 2;
            root.y0 = 0;

            function toggleAll(d) {
                if (d.children) {
                    d.children.forEach(toggleAll);
                    toggle(d);
                }
            }
            // Initialize the display to show a few nodes.
            root.children.forEach(toggleAll);
            update(root);
        });

        function update(source) {
            var duration = d3.event && d3.event.altKey ? 5000 : 500;
            // Compute the new tree layout.
            var nodes = tree.nodes(root).reverse();
            // Normalize for fixed-depth.
            nodes.forEach(function(d) {
                d.y = d.depth * 180;
            });
            // Update the nodes…
            var node = vis.selectAll("g.node")
                .data(nodes, function(d) {
                    return d.id || (d.id = ++i);
                });
            // Enter any new nodes at the parent's previous position.
            var nodeEnter = node.enter().append("svg:g")
                .attr("class", "node")
                .attr("transform", function(d) {
                    return "translate(" + source.y0 + "," + source.x0 + ")";
                })
                .on("click", function(d) {
                    toggle(d);
                    update(d);
                });
            nodeEnter.append("svg:circle")
                .attr("r", 1e-6)
                .style("fill", function(d) {
                    return d._children ? "lightsteelblue" : "#fff";
                });
            nodeEnter.append("svg:text")
                .attr("x", function(d) {
                    return d.children || d._children ? -10 : 10;
                })
                .attr("dy", ".35em")
                .attr("text-anchor", function(d) {
                    return d.children || d._children ? "end" : "start";
                })
                .text(function(d) {
                    return d.name;
                })
                .style("fill-opacity", 1e-6);
            // Transition nodes to their new position.
            var nodeUpdate = node.transition()
                .duration(duration)
                .attr("transform", function(d) {
                    return "translate(" + d.y + "," + d.x + ")";
                });
            nodeUpdate.select("circle")
                .attr("r", 4.5)
                .style("fill", function(d) {
                    return d._children ? "lightsteelblue" : "#fff";
                });
            nodeUpdate.select("text")
                .style("fill-opacity", 1);
            // Transition exiting nodes to the parent's new position.
            var nodeExit = node.exit().transition()
                .duration(duration)
                .attr("transform", function(d) {
                    return "translate(" + source.y + "," + source.x + ")";
                })
                .remove();
            nodeExit.select("circle")
                .attr("r", 1e-6);
            nodeExit.select("text")
                .style("fill-opacity", 1e-6);
            // Update the links…
            var link = vis.selectAll("path.link")
                .data(tree.links(nodes), function(d) {
                    return d.target.id;
                });
            // Enter any new links at the parent's previous position.
            link.enter().insert("svg:path", "g")
                .attr("class", "link")
                .attr("d", function(d) {
                    var o = {
                        x: source.x0,
                        y: source.y0
                    };
                    return diagonal({
                        source: o,
                        target: o
                    });
                })
                .transition()
                .duration(duration)
                .attr("d", diagonal);
            // Transition links to their new position.
            link.transition()
                .duration(duration)
                .attr("d", diagonal);
            // Transition exiting nodes to the parent's new position.
            link.exit().transition()
                .duration(duration)
                .attr("d", function(d) {
                    var o = {
                        x: source.x,
                        y: source.y
                    };
                    return diagonal({
                        source: o,
                        target: o
                    });
                })
                .remove();
            // Stash the old positions for transition.
            nodes.forEach(function(d) {
                d.x0 = d.x;
                d.y0 = d.y;
            });
        }
        // Toggle children.
        function toggle(d) {
            if (d.children) {
                d._children = d.children;
                d.children = null;
            } else {
                d.children = d._children;
                d._children = null;
            }
        }

    }

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
            "ridiculous": 0.97
        }

        new_predictions = []


    for (var result of predictions) {
        var predictions = result["predictions"];
        var binary = [];
        for (var p of predictions) {
          if (p[0] != "null") {
            if (p[1] >= limits[qcValue]) {
              binary.push(true);
            }
            else {
              binary.push(false);
            }
          }
          else {
            binary.push(false)
          }

        }

        var cutoff_indx = binary.lastIndexOf(true);

        var predictions_infer = predictions.slice(0, cutoff_indx+1);

        new_predictions.push({
          "seq_id": result["seq_id"],
          "predictions": predictions_infer
        });
    }


        return new_predictions
    }


    function populateTable(predictions, qcValue) {


    var limits = {
            "none": 0.0,
            "low": 0.5,
            "medium": 0.7,
            "high": 0.85,
            "ridiculous": 0.97
        }

        var pred_lim = limits[qcValue];

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
                                if (prediction[1] <= pred_lim) {
                                final_str += '<span data-toggle="tooltip" data-placement="top" class="text-danger" title="Confidence Value: ' + prediction[1] * 100 + '%">' + prediction[0] + '; </span>'
                                }

                                else{
                                final_str += '<span data-toggle="tooltip" data-placement="top" title="Confidence Value: ' + prediction[1] * 100 + '%">' + prediction[0] + '; </span>'
                                }

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