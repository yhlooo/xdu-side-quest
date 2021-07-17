layui.use('form', function(){
    var form = layui.form;
});

var form_register = new Vue({
    el: '#form_register',
    data: {
        group_name_tip: '请填写',
        is_error: false,
        is_ok: false,
        form_tip: ''
    }
});


function form_check_registered(name, value) {
    var res = false;
    $.ajax({
        url: url_check_registered,
        data: {
            'name': name,
            'value': value
        },
        async: false,
        xhrFields: {
            withCredentials: true
        },
        complete: function(xhr) {
            res = (404 !== xhr.status);
        }
    });
    return res;
}

function form_check_group_name() {
    var data = form_register.$data;
    data.group_name_tip = '请填写';
    data.is_error = false;
    data.is_ok = false;
    var group_name = $('#form-register-group_name').val();
    if (!group_name)
        return false;
    if (form_check_registered('group_name', group_name)) {
        data.group_name_tip = '该组名已被使用';
        data.is_error = true;
        return false;
    }
    else {
        data.group_name_tip = '该组名可用';
        data.is_ok = true;
        return true;
    }
}

function form_check() {
    var group_name = $('#form-register-group_name').val();
    var email = $('#form-register-email').val();
    var pass = $('#form-register-password').val();
    var re_pass = $('#form-register-reenter_password').val();
    var data = form_register.$data;
    data.form_tip = '';
    if (!group_name || !email || !pass || !re_pass)
        data.form_tip = '表单信息不全，请补充完整后提交';
    else if (form_check_registered('group_name', group_name))
        data.form_tip = '该组名已被使用，请更换后重试，或直接登录';
    else if (form_check_registered('email', email))
        data.form_tip = '该邮箱已被使用，请更换后重试，或直接登录';
    else if (pass !== re_pass)
        data.form_tip = '两次输入的密码不一样，请确认后重新提交';
    else
        return true;
    return false;
}

function register() {
    if (!form_check())
        return false;
    var group_name = $('#form-register-group_name').val();
    var email = $('#form-register-email').val();
    var grade = 1;
    if ($('#form_register-grade2').is(':checked'))
        grade = 2;
    else if ($('#form_register-grade3').is(':checked'))
        grade = 3;
    else
        grade = 1;
    var data = {
        'group_name': group_name,
        'email': email,
        'password': $('#form-register-password').val(),
        'grade': grade
    };
    $.ajax({
        url: url_register,
        type: 'POST',
        data: data,
        xhrFields: {
            withCredentials: true
        },
        complete: function(xhr) {
            if (200 === xhr.status)
                window.location.href = './register_success.html?group_name=' + group_name + '&email=' + email;
            else if (400 === xhr.status)
                alert('提交信息不全');
            else if (403 === xhr.status)
                alert('帐号已注册');
            else
                alert('未知错误，请稍后重试');
        }
    });
}