$(document).ready(function () {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $("#speech-form").submit(function (event) {
        event.preventDefault();

        var formData = $(this).serialize();
        var formURL = $(this).data("url");
        var successBanner = $("#status-banner-success");
        var failBanner = $("#status-banner-failed");

        $.ajax({
            url: formURL,
            type: "POST",
            data: formData,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (response) {
                console.log("SUCCESS")
                successBanner.prop('hidden', false).hide()
                successBanner.text(response.msg)

                successBanner.slideToggle(300, function () {
                    setTimeout(function () {
                        successBanner.slideToggle(500, function () {
                            successBanner.prop('hidden', true)
                        });
                    }, 2000);
                });

            },
            error: function (xhr, status, error) {
                console.log("SOME ERROR")
                failBanner.prop('hidden', false).hide()
                failBanner.text(JSON.parse(xhr.responseText).msg)

                failBanner.slideToggle(300, function () {
                    setTimeout(function () {
                        failBanner.slideToggle(500, function () {
                            failBanner.prop('hidden', true)
                        });
                    }, 2000);
                });
            }
        })
    });
});