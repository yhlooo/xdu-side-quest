// Coin
function toss_coin()
{
    var rand = Math.random();
    var coin = $("#coin");
    if (rand >= 0.5)
        coin.text('1');
    else
        coin.text('0');
    coin_spin(16);
}

function coin_spin(n)
{
    if (n > 0) {
        var coin = $("#coin");
        if (coin.text() === '0')
            coin.text('1');
        else
            coin.text('0');
        setTimeout('coin_spin(' + String(n-1) + ')', 50);
    }
}

// Lunch
function select_lunch(sign)
{
    var restaurant = $("#restaurant");
    var floor = $("#floor");
    var rand = Math.random() * 6;
    if (sign === 1) {
        restaurant = restaurant.text();
        if (restaurant === '竹园餐厅' || restaurant === '海棠餐厅') {
            if (rand >= 3)
                floor.text('二楼');
            else
                floor.text('一楼');
        }
        else if (restaurant === '综合楼') {
            if (rand >= 3)
                floor.text('老综');
            else
                floor.text('新综');
        }
        else if (restaurant === '丁香餐厅') {
            if (rand >= 4)
                floor.text('三楼');
            else if (rand >= 2)
                floor.text('二楼');
            else
                floor.text('一楼');
        }
        else {
            select_lunch(2);
            return;
        }
        floor_spin(18);
    }
    else {
        if (rand >= 4.5)
            restaurant.text('竹园餐厅');
        else if (rand >= 3.)
            restaurant.text('海棠餐厅');
        else if (rand >= 1.5)
            restaurant.text('丁香餐厅');
        else
            restaurant.text('综合楼');
        restaurant_spin(16);
        setTimeout('$("#lunch_tip2").slideDown(500);', 50 * 34 + 500)
    }
}
function restaurant_spin(n)
{
    if (n > 0) {
        var restaurant = $("#restaurant");
        var text = restaurant.text();
        if (text === '竹园餐厅')
            restaurant.text('海棠餐厅');
        else if (text === '海棠餐厅')
            restaurant.text('丁香餐厅');
        else if (text === '丁香餐厅')
            restaurant.text('综合楼');
        else if (text === '综合楼')
            restaurant.text('竹园餐厅');
        setTimeout('restaurant_spin(' + String(n-1) + ')', 50);
    }
    else {
        setTimeout('select_lunch(1)')
    }
}
function floor_spin(n)
{
    if (n > 0) {
        var restaurant = $("#restaurant").text();
        var floor = $("#floor");
        var text = floor.text();
        if (restaurant === '竹园餐厅') {
            if (text === '一楼')
                floor.text('二楼');
            else if (text === '二楼')
                floor.text('一楼');
        }
        else if (restaurant === '海棠餐厅') {
            if (text === '一楼')
                floor.text('二楼');
            else if (text === '二楼')
                floor.text('一楼');
        }
        else if (restaurant === '丁香餐厅') {
            if (text === '一楼')
                floor.text('二楼');
            else if (text === '二楼')
                floor.text('三楼');
            else if (text === '三楼')
                floor.text('一楼');
        }
        else if (restaurant === '综合楼') {
            if (text === '新综')
                floor.text('老综');
            else if (text === '老综')
                floor.text('新综');
        }
        setTimeout('floor_spin(' + String(n-1) + ')', 50);
    }
}

// Seat
function size_change(id, point)
{
    var something = $(id);
    something.val(parseInt(something.val()) + point);
}
function select_seat(sign, n)
{
    if (n > 0) {
        var rand = Math.random();
        if (sign === 1) {
            var res_row = $("#res_row");
            if (res_row.text() === '天选之位') {
                res_row.text('第1行');
                select_seat(1, 20);
                setTimeout('select_seat(2, 20)', 50 * 20 + 200);
                return;
            }
            var rows = parseInt($("#rows").val());
            res_row.text('第' + parseInt(rand * rows + 1) + '行');
        }
        else {
            var res_col = $("#res_col");
            var cols = parseInt($("#cols").val());
            var res = parseInt(cols * rand + 1);
            if (res >= cols / 2 + 1)
                res_col.text('，右第' + (cols - res + 1) + '列');
            else
                res_col.text('，左第' + res + '列');
        }
        setTimeout('select_seat(' + sign + ', ' + String(n - 1) + ')', 50);
    }
}
