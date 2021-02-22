function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        var name = $(this).attr('name')
        if(name) {
            name = name.replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('');
            $(this).removeClass("is-valid");
            $(this).removeClass("is-invalid");
        }
    });
    newElement.find('p').each(function() {
        var id = $(this).attr('id')
        if(id) {
            id = id.replace('-' + (total-1) + '-', '-' + total + '-');
            // var id = 'id_' + name;
            $(this).attr({'id': id}).val('');
            $(this).html("");
            $(this).addClass("hidden");
        }
    });
    // newElement.find('label').each(function() {
    //     var forValue = $(this).attr('for');
    //     if (forValue) {
    //       forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
    //       $(this).attr({'for': forValue});
    //     }
    // });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn.add-form-row').addClass('hidden');
    conditionRow.find('.btn.remove-form-row').removeClass('hidden');

    var conditionRow = $('.form-row:last');
    conditionRow.find('.btn.remove-form-row').removeClass('hidden');

    return false;
}
function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
            $(forms.get(i)).find('p').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    if(total == 2)
    {
        var conditionRow = $('.form-row:last');
        conditionRow.find('.btn.remove-form-row').addClass('hidden');
        conditionRow.find('.btn.add-form-row').removeClass('hidden');  
    }
    else
    {
        var conditionRow = $('.form-row:last');
        conditionRow.find('.btn.remove-form-row').removeClass('hidden');
        conditionRow.find('.btn.add-form-row').removeClass('hidden'); 
    }
    return false;
}
$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneMore('.form-row:last', 'form');
    document.getElementById("upload_button").scrollIntoView();
    return false;
});
$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});

$('#uploadForm').on('submit', function(event){
    event.preventDefault();
    var form = $(this);
    var formData = new FormData(this);
    $.ajax({
        url : "", // the endpoint
        type : 'POST', // http method
        data: formData,
        processData: false,
        contentType: false,
        dataType: 'json',
        // handle a successful response
        success : function(data) {
            if(data.form_is_valid)
            {
                console.log("success");
                window.location.href="frame_extract_download";
            }
            else
            {
                var invalid_frames = data.frames_not_found;
                var valid_frames = data.frames_found;
                for(invalid_frame of invalid_frames)
                {
                    $('#id_form-'+ invalid_frame +'-name').removeClass('is-valid'); 
                    $('#id_form-'+ invalid_frame +'-name').addClass('is-invalid'); 
                    $('#id_form-'+ invalid_frame +'-error').removeClass('hidden');
                    $('#id_form-'+ invalid_frame +'-error').html('No such frame in the uploaded file!');
                }

                for(valid_frame of valid_frames)
                {
                    $('#id_form-'+ valid_frame +'-name').removeClass('is-invalid'); 
                    $('#id_form-'+ valid_frame +'-name').addClass('is-valid'); 
                    $('#id_form-'+ valid_frame +'-error').addClass('hidden');
                    $('#id_form-'+ valid_frame +'-error').html('');
                }
            }
        },
    });
    return false;
});

$(document).on('input', '.verify-if-change', function(e){
    e.preventDefault();
    var id = e.target.id.match(/\d+/g)[0];
    $('#id_form-'+ id +'-name').removeClass('is-invalid'); 
    $('#id_form-'+ id +'-name').removeClass('is-valid'); 
    $('#id_form-'+ id +'-error').addClass('hidden');
    $('#id_form-'+ id +'-error').html('');
    return false;
});