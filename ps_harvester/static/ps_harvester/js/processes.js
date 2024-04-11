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

    function updateEntry(url, processID, entryID){

        const harvestEntry = $(`.harvest-entry[data-entry-id=${entryID}]`)
        const harvestEntries = $(`.harvest-entries[data-process-id=${processID}]`)
        const statusText = $(`.process-status[data-process-id=${processID}] span`)
        const reference = {"COMPLETE": "complete-status",
                           "INVALID": "invalid-status"}
        $.ajax({
            url: url,
            type: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                harvestEntry.remove()
        
                if (statusText.text() !== data.process_status) {
                    statusText.removeClass('review-status')
                    statusText.addClass(reference[data.process_status])
                    statusText.text(data.process_status)

                    harvestEntries.find('.accordion-body').append(
                        `<span class="text-vs-dblue">No entries for review.</span>`
                    )
                }
            },
            error: function (xhr, status, error) {
                console.log("Failed to update harvest entry");
            }
        });
    }

    $(".resolve-entry > button").click(function () {
        var parent = $(this).parent(".resolve-entry")
        $(parent).find(".icon-btn").css("display", "inline");
        $(this).css("display", "none");
    });

    $(".resolve-entry .confirm").click(function (e) {
        e.preventDefault();
        const url = $(this).data("url");
        const processID = $(this).data("process-id");
        const entryID = $(this).data("entry-id");
        updateEntry(url, processID, entryID)
    });

    $(".resolve-entry .cancel").click(function () {
        var parent = $(this).parents(".resolve-entry")
        $(parent).find(".icon-btn").css("display", "none")
        $(parent).find("button").css("display", "inline")
    });

    $(".delete-entry-modal .confirm").click(function (e) {
        e.preventDefault();
        const url = $(this).data("url");
        const processID = $(this).data("process-id");
        const entryID = $(this).data("entry-id");

        updateEntry(url, processID, entryID)
    });

});
