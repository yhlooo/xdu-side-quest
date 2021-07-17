function search_suggest()
{
    if(!network_state)
        return;
    if(search_engine === 'google')
        return 0;
    var search_text = $("#search_text").val();
    var url1 = "http://39.108.75.56/search_suggest?&search_text=" + search_text;
    $("#search_sug").load(url1, function(){
        $('li.sa_sg').mouseover(function(){
            $(this).css('background-color', '#F5F5F5');
        }).mouseleave(function(){
            $(this).css('background-color', '#ffffff');
        }).click(function(){
            $('#search_text').val($(this).attr('query'));
            go_search();
        });
    });
}
function go_search()
{
    var search_text = $("#search_text").val();
    var search_url = '';
    if(search_engine === 'bing'){
        search_url = 'http://cn.bing.com/search?q=' + search_text + '&go=搜索&qs=bs&form=QBRE&scope=web';
    }
    else{
        search_url = 'https://www.google.com/search?q=' + search_text + '&oq=' + search_text;
    }
    window.open(search_url);
    search_reset();
}
function search_reset()
{
    $("#search_text").val("");
    $("#search_sug").html("");
}
function search_engine_switch(engin)
{
    search_engine = engin;
    if(engin === 'bing')
        $("#engin_title").html('<img src="./img/bing_logo.png" height="40" width="118">　<span class="caret"></span>');
    else if(engin === 'google')
        $("#engin_title").html('<img src="./img/google_logo.png" height="40" width="118">　<span class="caret"></span>');
}
