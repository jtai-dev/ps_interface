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

    $(".resolve-entry").click(function () {
        var entryId = $(this).data("entry-id");
        $(`.confirm-resolve-entry[data-entry-id=${entryId}]`).css("display", "inline");
        $(`.cancel-resolve-entry[data-entry-id=${entryId}]`).css("display", "inline");
        $(this).css("display", "none");
    });

    $(".confirm-resolve-entry").click(function (e) {
        e.preventDefault();
        const url = $(this).data("url");
        const processID = $(this).data("process-id");
        const entryID = $(this).data("entry-id");
        updateEntry(url, processID, entryID)
    });

    $(".cancel-resolve-entry").click(function () {
        var entryId = $(this).data("entry-id");
        $(this).css("display", "none");
        $(`.confirm-resolve-entry[data-entry-id=${entryId}]`).css("display", "none");
        $(`.resolve-entry[data-entry-id=${entryId}]`).css("display", "inline");
    });

    $(".confirm-delete-entry").click(function (e) {
        e.preventDefault();
        const url = $(this).data("url");
        const processID = $(this).data("process-id");
        const entryID = $(this).data("entry-id");

        updateEntry(url, processID, entryID)
    });

    // $('.error-status').on('click', function (e) {
    //     const accordionTarget = $(this).closest('.accordion-button').data('bs-target');
    //     setTimeout(function(){
    //         $(accordionTarget).collapse('hide')
    //     }, 400)
    // });

});
