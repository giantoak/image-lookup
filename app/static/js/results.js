$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/gallery');
    console.log(socket);
    $('#loading-placeholder').text('Loading...');
    $('th').hide();

    socket.on('result', function (msg) {
        /* format the returned data and put it up for display
         *
         * given: msg, a json string that contains
         *          - query ==> the best query determined by Google
         *          - results ==> a list of links that were exact matches
         *          - url ==> original url of reverse image query
         *          - image ==> url of original image
         *          - filename ==> filename of image at upload time
         */
        $('#loading-placeholder').text('');
        $('th').show();

        jmsg = JSON.parse(msg);
    
        // handle the "Best query"
        var row = $('<tr class="result">');

        // Create two columns: one for image used in query....
        
        var image_cell = $('<td class="input-holder">')
            .html('<img class="input-image" src="' + jmsg['img'] + '">')
            .append($('<div class="actual-name">')
                    .text(jmsg['filename']));

        //              ... and one for returned data
        var data_cell = $('<td class="data">');
        if (jmsg['query'] != 'None') {
            best_query_msg = 'Best query: ' + jmsg['query'];
            best_query = $('<div class="best-query">')
                        .text(jmsg['query']);

            data_cell.append(best_query)
        }
        
        var exact_matches_li = $('<ul>');
        jmsg['results'].forEach(function (r) {
            var elem = $('<li>')
                        .html('<a href="' + r + '">' + r + '</a>');
            exact_matches_li.append(elem);
        });

        if (jmsg['results'].length == 0) {
            var last_elem = $('<div class="orig-query">').html('No exact matches found. <a href="' + jmsg['url'] + '">Original query</a>');
        }
        else {
            var last_elem = $('<div class="orig-query">').html('<a href="' + jmsg['url'] + '">Original query</a>');
        }


        data_cell.append(exact_matches_li)
            .append(last_elem);

        row.append(image_cell)
            .append(data_cell);

        $('#results-container').append(row);
    });
});
