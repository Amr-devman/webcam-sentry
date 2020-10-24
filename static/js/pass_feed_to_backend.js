var timer = setInterval(pass_feed_to_backend, 2000)

function pass_feed_to_backend(){
    // actually snap photo (from preview freeze).
    Webcam.snap( function(data_uri) {
        $.getJSON($SCRIPT_ROOT + '/_motion_detection', {
            photo_cap: data_uri,
        },function(data){
            var response = data.response;
        })

    });
}