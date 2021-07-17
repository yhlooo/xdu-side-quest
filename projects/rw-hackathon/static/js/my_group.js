layui.use('form', function(){
    var form = layui.form;
});
var group_info = new Vue({
    el: '#group_info',
    data: {
        group_id: '',
        group_name: '',
        email: '',
        grade: '',
        members: '',
        work_name: '',
        work_description: ''
    }
});

function detail() {
    $.ajax({
        url: url_detail,
        type: 'POST',
        data: {
            'members': $('#form-detail-members').val(),
            'work_name': $('#form-detail-work_name').val(),
            'work_description': $('#form-detail-work_description').val()
        },
        xhrFields: {
            withCredentials: true
        },
        async: false,
        complete: function(xhr) {
            if (200 === xhr.status) {
                window.location.href = './my_group.html';
            }
            else if (403 === xhr.status)
                window.location.href = './login.html';
            else if (404 === xhr.status)
                alert('该用户还未注册，请尝试注册后再操作');
            else
                alert('未知错误，请稍后重试');
        }
    });
}

$.ajax({
    url: url_group_info,
    xhrFields: {
        withCredentials: true
    },
    complete: function(xhr) {
        if (200 === xhr.status) {
            var data = eval('(' + xhr.responseText + ')');
            group_info.$data.group_id = data[0];
            group_info.$data.group_name = data[1];
            group_info.$data.email = data[2];
            group_info.$data.grade = data[3];
            group_info.$data.members = data[4];
            group_info.$data.work_name = data[5];
            group_info.$data.work_description = data[6];
        }
        else if (403 === xhr.status)
            window.location.href = './login.html';
        else
            alert('未知错误，请稍后重试');
    }
});