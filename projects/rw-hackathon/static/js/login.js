layui.use('form', function(){
    var form = layui.form;
});

function login() {
    var email = $('#form-login-email').val();
    var password = $('#form-login-password').val();
    var data = {
        'email': email,
        'password': password
    };
    if (!email || !password)
        return 0;
    $.ajax({
        url: url_login,
        type: 'POST',
        data: data,
        xhrFields: {
            withCredentials: true
        },
        complete: function(xhr) {
            if (200 === xhr.status)
                window.location.href = './my_group.html';
            else if (400 === xhr.status)
                alert('信息不全，请核对后重试');
            else if (404 === xhr.status)
                alert('该邮箱未注册，请注册后重试');
            else if (403 === xhr.status)
                alert('帐号或密码错误，请确认后重试');
            else
                alert('未知错误，请稍后重试');
        }
    });
}