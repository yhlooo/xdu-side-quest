var web = 0, ios = 0, game = 0, acm = 0, android = 0, ha = 0;

function add_one(options, id)
{
    if(id != ''){
        var element = document.getElementById(id);
        if(element.classList.contains('btn-default')){  // 选择
            element.classList.add('btn-primary');
            element.classList.remove('btn-default');
            options.forEach(function(option){
                if(option[0]=='web')
                    web += option[1];
                else if(option[0]=='ios')
                    ios += option[1];
                else if(option[0]=='game')
                    game += option[1];
                else if(option[0]=='acm')
                    acm += option[1];
                else if(option[0]=='android')
                    android += option[1];
            });
            if(!options[0])
                ha += 1;
            point_update();
            if(ha >= 5){
                alert('233，这不是彩蛋！不过恭喜你，解锁隐藏成就“最佳魔法师”。');
                ha = 0;
                document.getElementById('ha-1.1').classList.remove('btn-primary');
                document.getElementById('ha-1.1').classList.add('btn-default');
                document.getElementById('ha-1.2').classList.remove('btn-primary');
                document.getElementById('ha-1.2').classList.add('btn-default');
                document.getElementById('ha-1.3').classList.remove('btn-primary');
                document.getElementById('ha-1.3').classList.add('btn-default');
                document.getElementById('ha-1.4').classList.remove('btn-primary');
                document.getElementById('ha-1.4').classList.add('btn-default');
                document.getElementById('ha-1.5').classList.remove('btn-primary');
                document.getElementById('ha-1.5').classList.add('btn-default');
            }

        }
        else{  // 取消选择
            element.classList.remove('btn-primary');
            element.classList.add('btn-default');
            options.forEach(function(option){
                if(option[0]=='web')
                    web -= option[1];
                else if(option[0]=='ios')
                    ios -= option[1];
                else if(option[0]=='game')
                    game -= option[1];
                else if(option[0]=='acm')
                    acm -= option[1];
                else if(option[0]=='android')
                    android -= option[1];
            });
            if(!options[0])
                ha -= 1;
            point_update();
        }
    }
}


function result_reset()
{
    web = ios = acm = game = android = 0;
    var node = document.getElementsByClassName('btn-primary');
    while(node.length){
        node.item(0).classList.add('btn-default');
        node.item(0).classList.remove('btn-primary');
    }
    point_update();
}

function point_update()
{
    var max_t = '学习';
    var max = 0;
    if(ios > max){
        max = ios;
        max_t = 'iOS组';
    }
    if(game > max){
        max = game;
        max_t = '独立游戏组';
    }
    if(acm > max){
        max = acm;
        max_t = 'ACM组';
    }
    if(android > max){
        max = android;
        max_t = 'Android组';
    }
    if(web > max){
        max = web;
        max_t = 'Web/Server组';
    }
    document.getElementById('result_text').innerHTML = '我们建议你滚去'+max_t;
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('radar'));
    // 指定图表的配置项和数据
    var option = {
        title: {
            text: '不信你可以看看这个拽炸天的雷达图'
        },
        tooltip: {},
        legend: {},
        radar: {
            // shape: 'circle',
            indicator: [
                { name: 'Web/Server', max: max+2},
                { name: 'Game', max: max+2},
                { name: 'iOS', max: max+2},
                { name: 'Android', max: max+2},
                { name: 'ACM', max: max+2}
            ]
        },
        series: [{
            name: '兴趣分布',
            type: 'radar',
            // areaStyle: {normal: {}},
            data : [
                {
                    value : [web, game, ios, android, acm],
                    name : ''
                }
            ]
        }]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


point_update();
