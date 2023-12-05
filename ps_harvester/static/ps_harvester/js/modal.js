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

    $('.speech-entry-id').on('click', function(e){
        const entryNotes = $(`.speech-entry-notes[data-entry-id=${$(this).data("entry-id")}]`)
        const textArea = entryNotes.find(".modal-body textarea")
        getNotes(textArea)
    })


    $('.speech-entry-notes .edit-btn').on('click', function(e){
        const textArea = $(this).parents('.speech-entry-notes').find('.modal-body textarea')
        
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
    
});