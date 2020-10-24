function clear_whitelist() {
    $.when(clear_whitelist_ajax()).done(function(response){window.location.href="{{ url_for( 'setup_sentry' ) }}";})
    function clear_whitelist_ajax(){
        $.getJSON($SCRIPT_ROOT + '/_clear_whitelist',
            function(data){
            //this function is nothing
            console.log("Clearing WhiteList....")
        });
    }
}