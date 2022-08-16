$(document).ready(function(){
    function ajax_login(){
        $.ajax({
            url: '/ajax-login',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(response) {
                console.log(response);
            }
        });
    }

    $('#loginForm').submit(function( event ) {
        event.preventDefault();
        ajax_login();
    });

});
