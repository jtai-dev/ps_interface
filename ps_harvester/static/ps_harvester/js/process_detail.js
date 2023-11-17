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

    function updateEntry(url, entryID){

        const harvestEntry = $(`.harvest-entry[data-entry-id=${entryID}]`)

        $.ajax({
            url: url,
            type: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                console.log(harvestEntry)
                harvestEntry.remove()
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

            success: function (data){
                if (data.redirect_url){
                    window.location.href = data.redirect_url;
                }
            },
            error: function(xhr){
                console.log("Failed to delete process")
            }
        })
    }

    $(".confirm-delete-process").click(function (e){
        e.preventDefault();
        deleteProcess($(this).data("url"))
    });

    $(".unresolve-entry").click(function () {
        var entryId = $(this).data("entry-id");
        $(`.confirm-unresolve-entry[data-entry-id=${entryId}]`).css("display", "inline");
        $(`.cancel-unresolve-entry[data-entry-id=${entryId}]`).css("display", "inline");
        $(this).css("display", "none");
    });

    $(".confirm-unresolve-entry").click(function (e) {
        e.preventDefault();
        const url = $(this).data("url");
        const entryID = $(this).data("entry-id");
        updateEntry(url, entryID)
    });

    $(".cancel-unresolve-entry").click(function () {
        var entryId = $(this).data("entry-id");
        $(this).css("display", "none");
        $(`.confirm-unresolve-entry[data-entry-id=${entryId}]`).css("display", "none");
        $(`.unresolve-entry[data-entry-id=${entryId}]`).css("display", "inline");

    });

    $(".confirm-delete-entry").click(function (e) {
        e.preventDefault(); 
        const url = $(this).data("url");
        const entryID = $(this).data("entry-id");

        updateEntry(url, entryID)
    });
});