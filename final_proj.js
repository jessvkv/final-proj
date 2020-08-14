// search by AJAX

//read in .csv file and parse 
function runSearch( ) {
    // hide and clear existing results
    $('#results').hide();
    $('tbody').empty();

    // make form parameters into string to send to server
    var frmStr = $('#gene_search').serialize();

    $("#file").xxx
        source: function(request, response){
            $.ajax({
                url: './final_proj.cgi',
                dataType: 'JSON',
                data: frmStr,
                method: 'GET',
                success: function( ) {
                    processJSON(data);
                },
                    //direct result to html
                    $('#form-result').html(data)
            });
        }
}       


// process JSON that has gene matches and adds to results table 
function processJSON( data ) { 
    
    // this will be used to keep track of row identifiers
    var next_row = 1;
    
    // iterate matches and add a row to the result table for each match
    $.each( data.matches, function(i, item) {
        var row_id = 'result_row_' + next_row++;
    
        // append new row to end of table
        $('<tr/>', { "id" : row_id } ).appendTo('tbody');

    });
    
    // show results section that was hidden
    $('#results').show();
}

//run js when page ready
$(document).ready( function() {
    //click submit --> search starts
    $('#submit').click( function() {
        runSearch();
        return false;
    });
});
