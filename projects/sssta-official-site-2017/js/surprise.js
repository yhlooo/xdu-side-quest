function submit_check(type)
{
    var name = document.getElementById('name').value;
    var key = document.getElementById('key').value;
    var value = document.getElementById('value').value;
    if(type == 'oninput')
        document.getElementById('submit').disabled = !((key == '0' || key == '1' || key == '2.0' || key == '2.1' || key == '2.2') && name != '' && value != '');
    else if(type == 'onfocus')
        document.getElementById('key_unsigned').classList.add('hidden');
    else{  // 'onblur'
        if(key != '0' &&　key != '1' &&　key != '2.0' &&　key != '2.1' &&　key != '2.2'){
            document.getElementById('key_unsigned').classList.remove('hidden');
            document.getElementById('submit').disabled = true;
        }
    }
}
