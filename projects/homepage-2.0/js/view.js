$(document).ready(function(){
    $("#left_menu_ctrl").click(function(){
        $("#left_menu").fadeToggle(500, function(){
            if($("#left_menu_ctrl").html() === '<img src="./img/left_menu_ctrl0.png">')
                $("#left_menu_ctrl").html('<img src="./img/right_menu_ctrl0.png">');
            else
                $("#left_menu_ctrl").html('<img src="./img/left_menu_ctrl0.png">');
        });
    });
    $("#search_text")
       .focus(function(){
           $("#search_sug").show();
       })
       .blur(function(){
           setTimeout(function(){$("#search_sug").hide();}, 500);
       });
    $("button.search_engine_logo").focus(function(){
        $(this).css('background-color', 'transparent').css('color', '#ffffff');
    });
    $("#navbar")
        .mouseover(function(){
            $("#navbar-bg").stop().fadeIn(200);
        })
        .mouseleave(function(){
            $("#navbar-bg").stop().fadeOut(200);
            navbar_state1 = '0';
            setTimeout(function(){
                if(navbar_state1 === '0')
                    navbar_change();
            }, 300);
        });

    $(".dropdown-ctrl")
        .mouseover(function(){
            var new_state = $(this).attr('id').substring(14);
            navbar_state1 = new_state;
            setTimeout(function(){
                if(navbar_state1 === new_state)
                    navbar_change();
            }, 300);
        })
        .mouseleave(function(){
            navbar_state1 = '0';
            setTimeout(function(){
                if(navbar_state1 === '0')
                    navbar_change();
            }, 300);
        });
    $(".dropdown-main")
        .mouseover(function(){
            var new_state = $(this).attr('id').substring(14);
            navbar_state1 = new_state;
            setTimeout(function(){
                if(navbar_state1 === new_state)
                    navbar_change();
            }, 300);
            // $(this).stop().show();
        })
        .mouseleave(function(){
            navbar_state1 = '0';
            setTimeout(function(){
                if(navbar_state1 === '0')
                    navbar_change();
            }, 300);
            // $(this).hide();
        });
    function navbar_change(comm)
    {
        var cur = $("#navbar-cur");
        var main, ctrl;
            if(navbar_state0 !== navbar_state1){
                if(navbar_state1 === '0'){  // 离开
                    main = $("#dropdown-main-"+navbar_state0);
                    cur.animate({'width': '0'}, 150);
                    main.slideUp(150);
                }
                else if(navbar_state0 === '0'){  // 第一次进入
                    main = $("#dropdown-main-"+navbar_state1);
                    ctrl = $("#dropdown-ctrl-"+navbar_state1);
                    cur.css('left', ctrl.offset().left);
                    cur.animate({'width': ctrl.css('width')}, 150, function(){
                        main.slideDown(150);
                    });
                }
                else{  // 切换
                    main = $("#dropdown-main-"+navbar_state0);
                    var main1 = $("#dropdown-main-"+navbar_state1);
                    ctrl = $("#dropdown-ctrl-"+navbar_state1);
                    cur.animate({'width': ctrl.css('width'), 'left': ctrl.offset().left}, 150, function(){
                        main.hide();
                        main1.show();
                    });
                }
            }
        navbar_state0 = navbar_state1;
    }
});







