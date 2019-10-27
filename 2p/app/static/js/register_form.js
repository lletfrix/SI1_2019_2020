$(document).ready( function() {

    const name_is_valid = (name) => {
        var regex = /[0-9A-Za-z].{5,}/;
        var is_valid = regex.test(name);
        return is_valid;
    };


    const pass_is_valid = (pass) => {
        var regex = /.{6,}/;
        var is_valid = regex.test(pass);
        return is_valid;
    };


    const ccard_is_valid = (ccard) => {
        var regex = /[0-9]{12,}/;
        var is_valid = regex.test(ccard);
        return is_valid;
    };


    $('#nickname_register').on('input', function (){
        var nickname = $(this);
        is_valid = name_is_valid(nickname.val());
        if (is_valid) {
            nickname.removeClass("error").addClass("ok");
        }else{
            nickname.removeClass("ok").addClass("error");
        }
    });


    $('#password_register').on('input', function (){
        var pass = $(this);
        var progress_bar = $('#progress_bar');
        var strength = 0;
        var caps = /[A-Z]/;
        var number = /[0-9]/;

        if (pass.val().match(caps)) {
            strength += 1;
        }
        if (pass.val().match(number)) {
            strength += 1;
        }

        if(strength === 0 || !pass_is_valid(pass.val())){
            progress_bar.removeClass('mid_strength').removeClass('high_strength').addClass('low_strength');
        }
        else if(strength === 1){
            progress_bar.removeClass('low_strength').removeClass('high_strength').addClass('mid_strength');
        }
        else if(strength >= 2){
            progress_bar.removeClass('low_strength').removeClass('mid_strength').addClass('high_strength');
        }
    });


    $('#ccard_register').on('input', function () {
        var ccard = $(this);
        is_valid = ccard_is_valid(ccard.val());
        if (is_valid) {
            ccard.removeClass("error").addClass("ok");
        }else{
            ccard.removeClass("ok").addClass("error");
        }
    });


    $('#register_form').on('submit', function (e) {
        var form_data = $('#register_form').serializeArray();
        var name = form_data[0]['value'];
        var password = form_data[1]['value'];
        var ccard = form_data[4]['value'];
        if (!(name_is_valid(name) && pass_is_valid(password) && ccard_is_valid(ccard))){
            e.preventDefault();
        }
    });
});
