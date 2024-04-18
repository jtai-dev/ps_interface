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

    function updateEntry(url, processID, entryID) {

        processRow = $(`.process-row[data-process-id=${processID}]`)
        entryRow = $(`.entry-row[data-entry-id=${entryID}]`)

        currentStatus = processRow.find("span[class$='-status']")
        entryContainer = processRow.find(".entry-container")
        reference = {
            "COMPLETE": "complete-status",
            "INCOMPLETE": "incomplete-status",
            "PENDING REVIEW": "review-status",
            "ERROR": "error-status"
            }

        $.ajax({
            url: url,
            type: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                entryRow.remove()

                currentStatus.removeClass()
                currentStatus.addClass(reference[data.process_status])
                currentStatus.text(data.process_status)
                
                entryRows = entryContainer.find("table tbody tr")
                reviewCounter = currentStatus.next("span")

                if (entryRows.length < 1){
                    entryContainer.find('table').remove()
                    reviewCounter.remove()
                    entryContainer.append(
                        `<span class="ps-2">No entries for review.</span>`
                    )
                }
                else{
                    reviewCounter.text(`(${entryRows.length})`)
                }
                console.log('Successfully update harvest entry.')
            },
            error: function (xhr, status, error) {
                console.log("Failed to update harvest entry");
            }
        });
    }

    $(".resolve-entry > button").click(function () {
        parent = $(this).parent(".resolve-entry")
        $(parent).find(".icon-btn").css("display", "inline");
        $(this).css("display", "none");
    });

    $(".resolve-entry .confirm").click(function (e) {
        e.preventDefault();
        url = $(this).data("url");
        processID = $(this).parents(".process-row").data("process-id");
        entryID = $(this).parents(".entry-row").data("entry-id");
        updateEntry(url, processID, entryID)
    });

    $(".resolve-entry .cancel").click(function () {
        parent = $(this).parents(".resolve-entry")
        $(parent).find(".icon-btn").css("display", "none")
        $(parent).find("button").css("display", "inline")
    });

    $(".delete-entry-modal .confirm").click(function (e) {
        e.preventDefault();
        url = $(this).data("url");
        deleteEntryModal = $(this).parents('.delete-entry-modal')
        processID = deleteEntryModal.data("process-id");
        entryID = deleteEntryModal.data("entry-id");
        updateEntry(url, processID, entryID)
    });

});
