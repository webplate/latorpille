function show_result(data) {
    //react to server data
    //hide spinner
    $('#spinner').fadeOut("fast");
    if (data.profile_found) {
        //fill user id panel
        $('#tname').text(data.name);
        $('#tdomain').text(data.domain);
        $('#tphoto').attr('src', data.photo_url);
        
        //is the profile associated with a contact?
        if (data.contact_found) {
            $('#tcontact').text(data.contact_info)
        } else {
            $('#add_contact').fadeIn("slow");
        }
        //hide error
        $('#bad_url').fadeOut("fast");
        //show user id panel
        $('#information').fadeIn("slow");
    }
    else {
        //hide panel
        $('#information').fadeOut("fast");
        //show error
        console.info(data);
        $('#turl').text(data.target_url);
        $('#bad_url').fadeIn("slow");
    }
};

 function submit_form(e) {
    //show spinner
    $('#spinner').fadeIn("fast");
    //send form as json
    $.getJSON($SCRIPT_ROOT + '/_target', {
    target_url: $('input[name="target_url"]').val(),
    } , show_result);
    return false;
};

