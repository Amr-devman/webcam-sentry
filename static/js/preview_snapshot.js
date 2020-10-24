function preview_snapshot() {
    // actually snap photo (from preview freeze).
    Webcam.snap( function(data_uri) {
        // display results in page
        sentry_email = document.getElementById('sentry-email').value
        whitelisted_name = document.getElementById('sentry-whitelisted-person').value

        $.when(add_to_whitelist_ajax()).done(function(response){window.location.href="{{ url_for( 'setup_sentry' ) }}";})

        function add_to_whitelist_ajax(){
            $.getJSON($SCRIPT_ROOT + '/_photo_cap', {
                photo_cap: data_uri,
                sentry_email: sentry_email,
                whitelisted_name: whitelisted_name
            },function(data){
                var response = data.response;
            })
        }
    });
}
