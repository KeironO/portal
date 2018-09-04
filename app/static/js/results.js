$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip()
    var get_url = window.location.href + "/get";
    $("#example").DataTable({
        "ajax": {
            "url" : get_url,
            "dataSrc" : "_items"
        },
        "pageLength" : 50,
        "columns" : [
            {
                "title": "Sequence ID",
                "data" : "seq_id"
            },
            {
                "title": "Results",
                "data" : "predictions",
                "render" : function(data, type, row) {
                    var final_str = ""
                    for (i in data) {
                        var prediction = data[i];
                        if (prediction[0] != "null") {
                            final_str += '<span data-toggle="tooltip" data-placement="top" title="Confidence Value: ' + prediction[1]*100 + '%">' + prediction[0] + '; </span>'
                        } 
                    }
                    return final_str
                }
            }
        ]
    });
} );