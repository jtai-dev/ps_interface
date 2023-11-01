$(document).ready(function () {
    $('#show-password').on('change', function () {
    var passwordInput = $('#password-input');

    if ($(this).is(':checked')) {
        passwordInput.attr('type', 'text');
    } else {
        passwordInput.attr('type', 'password');
    }
    });
});