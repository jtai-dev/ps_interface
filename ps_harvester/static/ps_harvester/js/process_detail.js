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

    function updateEntry(url, entryID) {

        entryRow = $(`.entry-row[data-entry-id=${entryID}]`)

        $.ajax({
            url: url,
            type: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                entryRow.remove()
                console.log('Successfully update harvest entry.')
            },
            error: function (xhr, status, error) {
                console.log("Failed to update harvest entry");
            }
        });
    }

    function deleteProcess(url) {

        $.ajax({
            url: url,
            type: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            },

            success: function (data) {
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                }
            },
            error: function (xhr) {
                console.log("Failed to delete process")
            }
        })
    }


    $(".unresolve-entry > button").click(function () {
        parent = $(this).parent(".unresolve-entry")
        $(parent).find(".icon-btn").css("display", "inline");
        $(this).css("display", "none");
    });


    $(".unresolve-entry .confirm").click(function (e) {
        e.preventDefault();
        url = $(this).data("url");
        entryID = $(this).parents(".entry-row").data("entry-id");
        updateEntry(url, entryID)
    });

    $(".unresolve-entry .cancel").click(function () {
        parent = $(this).parents(".unresolve-entry")
        $(parent).find(".icon-btn").css("display", "none")
        $(parent).find("button").css("display", "inline")
    });

    $(".delete-entry-modal .confirm").click(function (e) {
        e.preventDefault();
        url = $(this).data("url");
        entryID = $(this).parents('.delete-entry-modal').data("entry-id");
        updateEntry(url, entryID)
    });

    $(".delete-process-modal .confirm").click(function (e) {
        e.preventDefault();
        deleteProcess($(this).data("url"))
    });

});