
$(document).ready(function () {
    $(".resolve-entry").click(function () {
        var entryId = $(this).data("entry-id");
        $(`.confirm-resolve[data-entry-id=${entryId}]`).css("display", "inline");
        $(`.cancel-resolve[data-entry-id=${entryId}]`).css("display", "inline");
        $(this).css("display", "none");
    });
});

$(document).ready(function () {
    $(".cancel-resolve").click(function () {
        var entryId = $(this).data("entry-id");
        $(this).css("display", "none");
        $(`.confirm-resolve[data-entry-id=${entryId}]`).css("display", "none");
        $(`.resolve-entry[data-entry-id=${entryId}]`).css("display", "inline");

    });
});

$(document).ready(function () {
    $(".confirm-resolve").click(function (event) {
        event.preventDefault();
        var entryId = $(this).data("entry-id");
        var processId = $(this).data("process-id");
        var url = $(this).data("url");
        $.ajax({
            url: url,
            type: "GET",
            success: function (data) {
                $(`.harvest-entry[data-entry-id=${entryId}]`).remove()
                console.log(data)
                if (data.change_status) {
                    
                    $(`.process-status[data-process-id=${processId}] span`).removeClass('review-status')
                    $(`.process-status[data-process-id=${processId}] span`).addClass(data.status_css_class)
                    $(`.process-status[data-process-id=${processId}] span`).text(data.status_name)
                    $(`.harvest-entries[data-process-id=${processId}] div`).html(
                        `<span class="text-vs-dblue">No entries for review.</span>`
                    )
                }
                console.log(`harvest_entry=${entryId} resolved`);
            },
            error: function (xhr, status, error) {
                console.log("Failed to resolve harvest entry:", status, error);
            }
        });
    });
});

$(document).ready(function () {
    $(".confirm-delete").click(function (event) {
        event.preventDefault();
        var entryId = $(this).data("entry-id");
        var processId = $(this).data('process-id')
        var url = $(this).data("url");
        $.ajax({
            url: url,
            type: "GET",
            success: function (data) {
                $(`.harvest-entry[data-entry-id=${entryId}]`).remove()
                if (data.change_status) {
                    $(`.process-status[data-process-id=${processId}] span`).removeClass('review-status')
                    $(`.process-status[data-process-id=${processId}] span`).addClass(data.status_css_class)
                    $(`.process-status[data-process-id=${processId}] span`).text(data.status_name)
                    $(`.harvest-entries[data-process-id=${processId}] div`).html(
                        `<span class="text-vs-dblue">No entries for review.</span>`
                    )
                }
                console.log(`harvest_entry=${entryId} deleted`);
            },
            error: function (xhr, status, error) {
                console.log("Failed to delete harvest entry:", status, error);
            }
        });
    });
});