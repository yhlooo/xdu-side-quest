/**
 * Created by Keyboard on 2017/4/28.
 */
var ii = 0, jj = 0, status = 0;
var cell1 = [], cell2 = [];
var livePro = [0, 0, 1, 1, 0, 0, 0, 0, 0], bornPro = [0, 0, 0, 1, 0, 0, 0, 0, 0];
for(ii = 0;ii < 52;ii++){
    cell1[ii] = [];
    cell2[ii] = [];
    for(jj = 0;jj < 52;jj++){
        cell1[ii][jj] = 0;
        cell2[ii][jj] = 0;
    }
}

function run()
{
    var id;
    if(status==0)
        return 0;
    id = "on"+mytoString(ii+1)+mytoString(jj+1);
    document.getElementById(id).className = "off";
    if(jj+1<50)
        jj++;
    else if(ii+1<50){
        jj=0;
        ii++;
    }
    else{
        jj=0;
        ii=0;
    }
    id = "on"+mytoString(ii+1)+mytoString(jj+1);
    document.getElementById(id).className = "on";
    setTimeout("run()", 100);
}

function arun() {
    var i, j, id;
    if (status == 0)
        return 0;

    for (i = 1; i < 51; i++) {
        for (j = 1; j < 51; j++) {
            id = "on" + mytoString(i) + mytoString(j);
            if (document.getElementById(id).className == "on")
                cell1[i][j] = 1;
            else
                cell1[i][j] = 0;
        }
    }
    switchStatus();
    for(i = 1;i < 51;i++){
        for(j = 1;j < 51;j++) {
            id = "on" + mytoString(i) + mytoString(j);
            if (cell1[i][j] == 1)
                document.getElementById(id).className = "on";
            else
                document.getElementById(id).className = "off";
        }
    }
    setTimeout("arun()", 100);
}

function switchOn(){  // 游戏开始
    status = 1;
    arun();
}
function suspend(){  // 游戏暂停
    status = 0;
}
function switchOff(){  // 游戏停止
    var i, j, id;
    status = 0;
    for(i = 0;i < 50;i++){
        for(j = 0;j < 50;j++){
            id = "on"+mytoString(i+1)+mytoString(j+1);
            document.getElementById(id).className = "off";
        }
    }

}
function reload()
{
    var i, j, id;
    status = 0;
    livePro = [0, 0, 1, 1, 0, 0, 0, 0, 0];
    bornPro = [0, 0, 0, 1, 0, 0, 0, 0, 0];
    for(i = 0;i < 9;i++){
        if(livePro[i])
            document.getElementById("live"+i.toString()).className = "checkbox on";
        else
            document.getElementById("live"+i.toString()).className = "checkbox off";
        if(bornPro[i])
            document.getElementById("born"+i.toString()).className = "checkbox on";
        else
            document.getElementById("born"+i.toString()).className = "checkbox off";
    }
    for(i = 0;i < 50;i++){
        for(j = 0;j < 50;j++){
            id = "on"+mytoString(i+1)+mytoString(j+1);
            document.getElementById(id).className = "off";
        }
    }
    document.getElementById("on0826").className = "on";
    document.getElementById("on0924").className = "on";
    document.getElementById("on0926").className = "on";
    document.getElementById("on1014").className = "on";
    document.getElementById("on1015").className = "on";
    document.getElementById("on1022").className = "on";
    document.getElementById("on1023").className = "on";
    document.getElementById("on1113").className = "on";
    document.getElementById("on1117").className = "on";
    document.getElementById("on1122").className = "on";
    document.getElementById("on1123").className = "on";
    document.getElementById("on1136").className = "on";
    document.getElementById("on1137").className = "on";
    document.getElementById("on1212").className = "on";
    document.getElementById("on1218").className = "on";
    document.getElementById("on1222").className = "on";
    document.getElementById("on1223").className = "on";
    document.getElementById("on1236").className = "on";
    document.getElementById("on1237").className = "on";
    document.getElementById("on1302").className = "on";
    document.getElementById("on1303").className = "on";
    document.getElementById("on1312").className = "on";
    document.getElementById("on1316").className = "on";
    document.getElementById("on1318").className = "on";
    document.getElementById("on1319").className = "on";
    document.getElementById("on1324").className = "on";
    document.getElementById("on1326").className = "on";
    document.getElementById("on1402").className = "on";
    document.getElementById("on1403").className = "on";
    document.getElementById("on1412").className = "on";
    document.getElementById("on1418").className = "on";
    document.getElementById("on1426").className = "on";
    document.getElementById("on1513").className = "on";
    document.getElementById("on1517").className = "on";
    document.getElementById("on1614").className = "on";
    document.getElementById("on1615").className = "on";
}
function hover(list, line, n)
{
    if(n==1){
        document.getElementById(list).className = "localon";
        document.getElementById(line).className = "localon";
    }
    else{
        document.getElementById(list).className = "localoff";
        document.getElementById(line).className = "localoff";
    }
}

function turn(id) {  // 转换cell的状态
    if(document.getElementById(id).className == "on")
        document.getElementById(id).className = "off";
    else
        document.getElementById(id).className = "on";
}
function mytoString(n)
{
    if(n < 10 && n >= 0)
        return "0"+n.toString();
    else
        return n.toString();
}

function switchStatus()
{
    var n, i, j;
    for(i=1;i<51;i++){
        for(j=1;j<51;j++){
            n = cell1[i-1][j-1]+cell1[i-1][j]+cell1[i-1][j+1];
            n += cell1[i][j-1]+cell1[i][j+1];
            n += cell1[i+1][j-1]+cell1[i+1][j]+cell1[i+1][j+1];
            if(cell1[i][j]==1){
                if(livePro[n])
                    cell2[i][j] = 1;
                else
                    cell2[i][j] = 0;

            }
            else{
                if(bornPro[n]){
                    cell2[i][j] = 1;
                }
                else{
                    cell2[i][j] = 0;
                }
            }
        }
    }
    for(i=1;i<51;i++){
        for(j=1;j<51;j++){
            cell1[i][j]=cell2[i][j];
        }
    }
}

function live(n)
{
    var id;
    id = "live"+n.toString();
    if(document.getElementById(id).className == "checkbox off") {
        document.getElementById(id).className = "checkbox on";
        livePro[n] = 1;
    }
    else {
        document.getElementById(id).className = "checkbox off";
        livePro[n] = 0;
    }
}
function born(n)
{
    var id;
    id = "born"+n.toString();
    if(document.getElementById(id).className == "checkbox off") {
        document.getElementById(id).className = "checkbox on";
        bornPro[n] = 1;
    }
    else {
        document.getElementById(id).className = "checkbox off";
        bornPro[n] = 0;
    }
}
