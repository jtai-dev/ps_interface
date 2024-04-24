$(document).ready(function () {
    $(".auth-form").submit(function (event) {
        event.preventDefault();
        console.log("AJAX")
        formData = $(this).serialize();
        
        $("input.form-control").removeClass('is-invalid')
        $(".invalid-feedback").empty()
        $(".auth-error").empty()

        $.ajax({
            type: "POST",
            url: window.location.href,
            data: formData,
            success: function (response) {
                if (response.redirect){
                    window.location.href = response.redirect_url
                }
                else{
                    authCard = $(response).find('.auth-card')
                    $('.auth-card').html(authCard.html())
                }
            },
            error: function (xhr, status, error) {
                formErrors = JSON.parse(xhr.responseText)
                
                $.each(formErrors.field_errors, function (field, errors) {
                    inputControl = $(`.auth-form input.form-control[name="${field}"]`)
                    inputControl.addClass("is-invalid")
                    errorContainer = $(inputControl.siblings(".invalid-feedback"))
                    wrappedErrors = errors.map(e =>`<p class="text-start text-vs-red">${e}</p>`)
                    errorContainer.html(wrappedErrors.join("\n"))

                })
                nonFieldErrors = formErrors.non_field_errors
                wrappedErrors = nonFieldErrors.map(e =>`<p class="text-start text-vs-red">${e}</p>`)
                firstAuthItem = $(".auth-item").first().html(wrappedErrors.join("\n"))
            }
        })
    });

    $('.reveal-pass input').on('change', function () {
        authItem = $(this).parents(".auth-item")
        passInput = authItem.find(".form-control")
        if ($(this).is(':checked')) {
            passInput.attr('type', 'text');
        } else {
            passInput.attr('type', 'password');
        }
    });
}); 