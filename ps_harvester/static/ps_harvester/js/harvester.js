
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

    $(".resolve-entry").click(function () {
        var entryId = $(this).data("entry-id");
        $(`.confirm-resolve[data-entry-id=${entryId}]`).css("display", "inline");
        $(`.cancel-resolve[data-entry-id=${entryId}]`).css("display", "inline");
        $(this).css("display", "none");
    });

    $(".cancel-resolve").click(function () {
        var entryId = $(this).data("entry-id");
        $(this).css("display", "none");
        $(`.confirm-resolve[data-entry-id=${entryId}]`).css("display", "none");
        $(`.resolve-entry[data-entry-id=${entryId}]`).css("display", "inline");

    });


    function getNotes(textArea){
        $.ajax({
            url: textArea.data('url'),
            type: "GET",
            success: function(data){
                textArea.val(data.notes)
            }
        })
    }

    function updateNotes(textArea){
        const modalBody = textArea.parents('.modal-body')
        $.ajax({
            url: textArea.data('url'),
            type: "POST",
            data: {notes: textArea.val()},
            headers: {
                'X-CSRFToken': csrftoken,
            },
            success: function(response){
                console.log(response.msg)
            },
            error: function(response){
                modalBody.append(`<div class='ms-1 text-vs-red'><span>Error saving: ${response.msg}</span></div>`);
            }
        })
    }

    $('.process-id').on('click', function(e){
        const processNotes = $(`.process-notes[data-process-id=${$(this).data("process-id")}]`)
        const textArea = processNotes.find(".modal-body textarea")
        getNotes(textArea)
    })

    $('.process-notes .edit-btn').on('click', function(e){
        const textArea = $(this).parents('.process-notes').find('.modal-body textarea');

        $(this).text(function(i, text){
            return text === "Edit" ? "Save" : "Edit"
        })

        if ($(this).text() === 'Save'){
            textArea.removeAttr('disabled');   
        }
        else{
            updateNotes(textArea)
            textArea.prop('disabled', true);
        }
    });

    $('.speech-id').on('click', function(e){
        const entryNotes = $(`.entry-notes[data-entry-id=${$(this).data("entry-id")}]`)
        const textArea = entryNotes.find(".modal-body textarea")
        getNotes(textArea)
    })


    $('.entry-notes .edit-btn').on('click', function(e){
        const textArea = $(this).parents('.entry-notes').find('.modal-body textarea')
        
        $(this).text(function(i, text){
            return text === "Edit" ? "Save" : "Edit"
        })

        if ($(this).text() === 'Save'){
            textArea.removeAttr('disabled');
        }
        else{
            updateNotes(textArea)
            textArea.prop('disabled', true);
        }
    })

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
                console.log("Failed to update harvest entry:", status, error);
            }
        });
    }

    $(".confirm-resolve").click(function (e) {
        e.preventDefault();
        const url = $(this).data("url");
        const processID = $(this).data("process-id");
        const entryID = $(this).data("entry-id");
        
        updateEntry(url, processID, entryID)

    });

    $(".confirm-delete").click(function (e) {
        e.preventDefault();
        const url = $(this).data("url");
        const processID = $(this).data("process-id");
        const entryID = $(this).data("entry-id");

        updateEntry(url, processID, entryID)
    });

    $('.error-status').on('click', function (e) {
        const accordionTarget = $(this).closest('.accordion-button').data('bs-target');
        setTimeout(function(){
            $(accordionTarget).collapse('hide')
        }, 400)
    });

});



