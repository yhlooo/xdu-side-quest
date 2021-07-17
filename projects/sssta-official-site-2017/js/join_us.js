function turn_to(command)
{
    if(command=='sign_up'){
        document.getElementById('sign_up-li').classList.add('active');
        document.getElementById('sign_in-li').classList.remove('active');
        document.getElementById('profile-li').classList.remove('active');
        document.getElementById('sign_up-div').classList.remove('hidden');
        document.getElementById('sign_in-div').classList.add('hidden');
        document.getElementById('profile-div').classList.add('hidden');
    }
    else if(command=='sign_in'){
        document.getElementById('sign_up-li').classList.remove('active');
        document.getElementById('sign_in-li').classList.add('active');
        document.getElementById('profile-li').classList.remove('active');
        document.getElementById('sign_up-div').classList.add('hidden');
        document.getElementById('sign_in-div').classList.remove('hidden');
        document.getElementById('profile-div').classList.add('hidden');

    }
    else if(command=='profile'){
        document.getElementById('sign_up-li').classList.remove('active');
        document.getElementById('sign_in-li').classList.remove('active');
        document.getElementById('profile-li').classList.add('active');
        document.getElementById('sign_up-div').classList.add('hidden');
        document.getElementById('sign_in-div').classList.add('hidden');
        document.getElementById('profile-div').classList.remove('hidden');
    }
}

function pass_again(command)
{
    var pass = document.getElementById('pass-input1').value;
    var pass_again = document.getElementById('pass_again-input1').value;
    if(pass==''){
        document.getElementById('pass_again-div1').className = 'form-group';
        document.getElementById('pass_again-span1').className = '';
    }
    else if(command=='onfocus'){
        if(pass!=pass_again){  // 默认的
            document.getElementById('pass_again-div1').className = 'form-group';
            document.getElementById('pass_again-span1').className = '';
        }
        else{  // 对的
            document.getElementById('pass_again-div1').className = 'form-group has-success has-feedback';
            document.getElementById('pass_again-span1').className = 'glyphicon glyphicon-ok form-control-feedback';
        }
    }
    else if(command=='onchange'){
        if(pass!=pass_again){  // 默认的
            document.getElementById('pass_again-div1').className = 'form-group';
            document.getElementById('pass_again-span1').className = '';
        }
        else{  // 对的
            document.getElementById('pass_again-div1').className = 'form-group has-success has-feedback';
            document.getElementById('pass_again-span1').className = 'glyphicon glyphicon-ok form-control-feedback';
        }
    }
    else if(command=='onblur'){
        if(pass_again==''){  // 默认的
            document.getElementById('pass_again-div1').className = 'form-group';
            document.getElementById('pass_again-span1').className = '';
        }
        else if(pass!=pass_again){  // 错的
            document.getElementById('pass_again-div1').className = 'form-group has-error has-feedback';
            document.getElementById('pass_again-span1').className = 'glyphicon glyphicon-remove form-control-feedback';
        }
        else{  // 对的
            document.getElementById('pass_again-div1').className = 'form-group has-success has-feedback';
            document.getElementById('pass_again-span1').className = 'glyphicon glyphicon-ok form-control-feedback';
        }
    }
}

function submit_check(formID)
{
    if(formID=='form1'){
        var name1 = document.getElementById('name-input1').value;
        var sex1 = document.getElementById('sex-input1').value;
        var account1 = document.getElementById('account-input1').value;
        var pass1 = document.getElementById('pass-input1').value;
        var pass_again1 = document.getElementById('pass_again-input1').value;
        var email1 = document.getElementById('email-input1').value;
        document.getElementById('had_signed').classList.add('hidden');
        if(name1 != '' && sex1 != 'undefined' && email1 != '' && account1 != '' && pass1 != '' && pass1 == pass_again1){  // 启用提交按钮
            document.getElementById('submit1').classList.remove('disabled');
            document.getElementById('submit1').setAttribute('onclick', "sign_up()");
        }
        else{  // 禁用提交按钮
            document.getElementById('submit1').classList.add('disabled');
            document.getElementById('submit1').removeAttribute('onclick');
        }
    }
    else if(formID=='form2'){
        var account2 = document.getElementById('account-input2').value;
        var pass2 = document.getElementById('pass-input2').value;
        if(account2 != '' && pass2 != ''){  // 启用提交按钮
            document.getElementById('submit2').classList.remove('disabled');
            document.getElementById('submit2').setAttribute('onclick', "sign_in()");
        }
        else{  // 禁用提交按钮
            document.getElementById('submit2').classList.add('disabled');
            document.getElementById('submit2').removeAttribute('onclick');
        }
    }
    else if(formID=='form3'){

    }
}

function switch_group()
{
    var group = document.getElementById('direction-input3').value;
    var web_option = document.getElementById('web-option');
    var game_option = document.getElementById('game-option');
    var acm_option = document.getElementById('acm-option');
    web_option.classList.add('hidden');
    game_option.classList.add('hidden');
    acm_option.classList.add('hidden');
    document.getElementById(group+'-option').classList.remove('hidden');
}