var lat = '34.1273045', lon = '108.8269963';
function getWeather()
{
    if(!network_state)
        return getNetState();
    $("#weather_img").html('<span class="icon-spiner icon-spin" style="font-size: 5vw;"></span>');
    // var lat = getCookie('lat'), lon = getCookie('lon');
    if(lat == "" || lon == ""){
        $("#temp").text('99');
        $("#temp1").text('99');
        $("#temp2").text('99');
        $("#weather").text('青蛙雨');
        $("#city")
            .html('魔都 <span class="icon-map-marker"></span>')
            .attr('title', 'Magical City\nClick to Reload');
        $("#weather-main").attr('title', 'Update: yyyy-mm-dd HH:MM:SS\nClick to Reload');
        $("#weather_img").html('<span class="icon-refresh" style="font-size: 5vw;"></span>');
        return getLocation();
    }
    // 三天
    $.ajax({
        url: 'http://aliv2.data.moji.com/whapi/json/aliweather/briefforecast3days',
        type: "POST",
        data: {
            'lat': lat,
            'lon': lon
        },
        beforeSend: function(XHR){
            XHR.setRequestHeader("Authorization", "APPCODE a9dab280ccd341749f034d2bc338dcf9");
        },
        success: function(res){
            res = $.parseJSON(res);
            $("#temp1").text(res['data']['forecast'][0]['tempDay']);
            $("#temp2").text(res['data']['forecast'][0]['tempNight']);
        },
        error: function(){
            $("#temp1").text('99');
            $("#temp2").text('99');
        }
    });
    // 实时
    $.ajax({
        url: 'http://aliv2.data.moji.com/whapi/json/aliweather/briefcondition',
        type: "POST",
        data: {
            'lat': lat,
            'lon': lon
        },
        beforeSend: function(XHR){
            XHR.setRequestHeader("Authorization", "APPCODE a9dab280ccd341749f034d2bc338dcf9");
        },
        success: function(res){
            res = $.parseJSON(res);
            $("#temp").text(res['data']['condition']['temp']);
            $("#weather").text(res['data']['condition']['condition']);
            $("#city")
                .html(res['data']['city']['name']+' <span class="icon-map-marker"></span>')
                .attr('title', res['data']['city']['pname']+' '+res['data']['city']['name']+'\nClick to Reload');
            $("#weather-main").attr('title', 'Update: '+res['data']['condition']['updatetime']+'\nClick to Reload');
            $("#weather_img").html('<img src="./img/weather/'+res['data']['condition']['condition']+'.png" class="img-responsive">')
        },
        error: function(){
            $("#temp").text('99');
            $("#weather").text('青蛙雨');
            $("#city")
                .html('魔都 <span class="icon-map-marker"></span>')
                .attr('title', 'Magical City\nClick to Reload');
            $("#weather-main").attr('title', 'Update: yyyy-mm-dd HH:MM:SS\nClick to Reload');
            $("#weather_img").html('<span class="icon-refresh" style="font-size: 5vw;"></span>');
        }
    });
}
function getTime()
{
    var now = new Date();
    var month = now.getMonth();
    var date = now.getDate();
    var day = now.getDay();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();

    $("#hours").text(hours);
    if(minutes < 10)
        minutes = '0' + minutes;
    $("#minutes").text(minutes);
    if(seconds < 10)
        seconds = '0' + seconds;
    $("#seconds").text(seconds);
    if(day === 0)
        day = 'Sunday';
    else if(day === 1)
        day = 'Monday';
    else if(day === 2)
        day = 'Tuesday';
    else if(day === 3)
        day = 'Wednesday';
    else if(day === 4)
        day = 'Thursday';
    else if(day === 5)
        day = 'Friday';
    else if(day === 6)
        day = 'Saturday';
    $("#day").text(day);
    if(month === 0)
        month = 'Jan.';
    else if(month === 1)
        month = 'Feb.';
    else if(month === 2)
        month = 'Mar.';
    else if(month === 3)
        month = 'Apr.';
    else if(month === 4)
        month = 'May';
    else if(month === 5)
        month = 'June';
    else if(month === 6)
        month = 'July';
    else if(month === 7)
        month = 'Aug.';
    else if(month === 8)
        month = 'Sept.';
    else if(month === 9)
        month = 'Oct.';
    else if(month === 10)
        month = 'Nov.';
    else if(month === 11)
        month = 'Dec.';
    $("#month").text(month);
    $("#date").text(date);

    setTimeout('getTime()',100);
}

function getNetState()
{
    if(!network_state){
        $("#net-switch").attr('class', 'icon-off online');
        setTimeout(function(){
            $("#net-switch").attr('class', 'icon-off offline');
            setTimeout(function(){
                $("#net-switch").attr('class', 'icon-off online');
                setTimeout(function(){
                    $("#net-switch").attr('class', 'icon-off offline');
                    setTimeout(function(){
                        $("#net-switch").attr('class', 'icon-off online');
                        setTimeout(function(){
                            $("#net-switch").attr('class', 'icon-off offline');
                        }, 300)
                    }, 300)
                }, 300)
            }, 300)
        }, 300)
    }
    else{
        var netState_refresh =  $("#netState_refresh");
        netState_refresh.addClass('icon-spin');
        $("#net-switch").attr('class', 'icon-off offline');
        $("#ip_address").text('xxx.xxx.xxx.xxx');
        $("#net_state").text('Testing...');
        $.ajax({
            url: 'http://39.108.75.56/ip_address',
            success: function(data){
                $("#ip_address").text(data);
                $("#net_state").text('Internet Accessible');
                $("#net-switch").attr('class', 'icon-off online');

            },
            error: function () {
                $("#net-switch").attr('class', 'icon-off noInternet');
                $("#net_state").text('Offline');
            }
        });
        var gfw_try = $("#gfw_try");
        var gfw_state_show = $("#gfw_state");
        gfw_try.html('');
        gfw_state = 0;
        gfw_try.html('<img src="https://www.google.com.hk/images/branding/googlelogo/2x/googlelogo_color_120x44dp.png" onload="gfw_state = 1;">');
        setTimeout(function(){
            if(gfw_state){
                gfw_state_show.text('The real internet!');
            }
            else{
                gfw_state_show.text('The limited internet!');
            }
            netState_refresh.removeClass('icon-spin');
        }, 5000);
    }
}
function switch_net()
{
    if(!network_state){
        $("#net-switch").attr('class', 'icon-off online');
        network_state = 1;
        getNetState();
    }
    else{
        network_state = 0;
        $("#net-switch").attr('class', 'icon-off offline');
        $("#ip_address").text('xxx.xxx.xxx.xxx');
        $("#net_state").text('Offline');
    }
}
function getLocation()
{
    if(!network_state)
        return getNetState();
    var options = {
    enableHighAccuracy: true,
    maximumAge: 1000
    };
    if (navigator.geolocation)
    navigator.geolocation.getCurrentPosition(onSuccess,onError,options);
    else{}

    function onSuccess(position)
    {
        // setCookie('lat', position.coords.latitude, 15);
        // setCookie('lon', position.coords.longitude, 15);
        lat = String(position.coords.latitude);
        lon = String(position.coords.longitude);
        return getWeather();
    }
    function onError(error)
    {
        switch (error.code) {
        case 1:
            alert("位置服务被拒绝");
            break;
        case 2:
            alert("暂时获取不到位置信息");
            break;
        case 3:
            alert("获取信息超时");
            break;
        case 4:
            alert("未知错误");
            break;
        }
    }
}
