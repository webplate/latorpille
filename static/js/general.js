function show_result(data) {
    //react to server data
    //hide spinner
    $('#spinner').fadeOut("fast");
    if (data.profile_found) {
        //hide error
        $('#bad_url').fadeOut("fast");
        
        // select most relevant profile match
        console.log(data.matches);
        var main_match = data.matches[0];
        
        //fill user id panel
        $('#tname').text(main_match.name);
        $('#tdomain').text(main_match.domain);
        $('#tphoto').attr('src', main_match.photo_url);
        
        //is the profile associated with a contact?
        if (data.contact_found) {
            $('#tcontact').text(main_match.contact_info)
            $('#tcontact_div').fadeIn("slow");
            $('#add_contact').fadeIn("slow");
        } else {
            $('#add_contact').fadeIn("slow");
            $('#tcontact_div').fadeOut("fast");
        }
        
        //show user id panel
        $('#information').fadeIn("slow");
    }
    else {
        //hide panel
        $('#information').fadeOut("fast");
        //show error
        $('#turl').text(data.target_url);
        $('#bad_url').fadeIn("slow");
    }
};

 function submit_target(e) {
    //show spinner
    $('#spinner').fadeIn("fast");
    //send form as json
    $.getJSON($SCRIPT_ROOT + '/_target', {
    target_url: $('input[name="target_url"]').val(),
    } , show_result);
    return false;
};

 function submit_contact(e) {
    //show spinner
    $('#spinner').fadeIn("fast");
    //send form as json
    $.getJSON($SCRIPT_ROOT + '/_target', {
    target_url: $('input[name="target_url"]').val(),
    contact_info: $('input[name="contact_info"]').val(),
    } , show_result);
    return false;
};

function myMain() {
    //bind form button to submit function (target url)
    $('#send_target_url').bind('click', submit_target);
    //bind enter key
    $('input[name=target_url]').bind('keydown', function(e) {
        if (e.keyCode == 13) {
            submit_target(e);
        }
    })
    //bind form button to submit function (contact info)
    $('#send_contact_info').bind('click', submit_contact);
    //bind enter key
    $('input[name=contact_info]').bind('keydown', function(e) {
        if (e.keyCode == 13) {
            submit_contact(e);
        }
    })

    //focus main input
    $('input[name=target_url]').focus();
}
