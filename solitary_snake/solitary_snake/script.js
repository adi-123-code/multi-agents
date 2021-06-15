function FreshQtableElement(row,cell,value)
{
	var th = q_table_table.rows[row + 1].cells[cell + 1];
	th.innerHTML = value;
}

function FreshQtable()
{
	q_table_table.innerHTML = '<tr><th class = "q_table_th">STA</th><th class = "q_table_th">UP</th><th class = "q_table_th">DOWN</th><th class = "q_table_th">LEFT</th><th class = "q_table_th">RIGHT</th></tr>';
	for(k = 0; k < 512; k++)
	{
		var add_html = '<td class = "score_table_th">' + k + '</td>';
		for(var m = 0; m < 4; m++)
			add_html += '<td class = "score_table_th">' + Q_table[k][m] + '</td>';
		q_table_table.innerHTML += '<tr>' + add_html + '</tr>';
	}
}

var canvas = document.getElementById("canvas");
var time_canvas = document.getElementById("time_canvas");
var score_table = document.getElementById("score_table");
var score_table_div = document.getElementById("score_table_div");
var q_table_table = document.getElementById("q_table");
var time_div = document.getElementById("time_left");
var best_score_input = document.getElementById("best");
var score_div = document.getElementById("score");
var time_ctx = time_canvas.getContext("2d");
var ctx = canvas.getContext("2d");


/*初始化Q_table*/
var Q_table = new Array(512);
for(var k = 0; k < 512; k++)
{
	Q_table[k] = new Array(4);
	Q_table[k][0] = 0;
	Q_table[k][1] = 0;
	Q_table[k][2] = 0;
	Q_table[k][3] = 0;
}
FreshQtable();

var tar_dir = 'U';
var snake_dir = 'U';
var snake_pos;
var snake_length = 0;
var esa_pos_x = 0;
var esa_pos_y = 0;
var new_head = new Array(2);
var esa_distance = 0;
var old_esa_distance = 0;

/*游戏控制*/
var time_id = 0;
var game_being = 0;
var left_time = 1000;
var score = 0;
var gen = 1;
var best_score = 0;

function InitSnakePos()
{
	snake_pos = new Array();
	snake_pos[0] = new Array(2);
	snake_pos[0][0] = 300;
	snake_pos[0][1] = 300;
	snake_pos[1] = new Array(2);
	snake_pos[1][0] = 300;
	snake_pos[1][1] = 320;
	snake_length = 2;
	esa_pos_x = 240;
	esa_pos_y = 80;
	tar_dir = 'U';
    snake_dir = 'U';
	left_time = 1000;
	score = 0;
	score_div.value = score;
}

function IsEsaInSnake(x,y,snake,index)
{
	for(var j = index; j < snake.length; j++)
	{
		if(snake[j][0] == x && snake[j][1] == y)
			return 1;
	}
	return 0;
}

/*线段是否相交*/
function IsBanana(ax,ay,bx,by,cx,cy,dx,dy)
{
	//线段ab的法线N1 
	 var nx1 = (by - ay), ny1 = (ax - bx); 
	  
	 //线段cd的法线N2 
	 var nx2 = (dy - cy), ny2 = (cx - dx); 
	  
	 //两条法线做叉乘, 如果结果为0, 说明线段ab和线段cd平行或共线,不相交 
	 var denominator = nx1*ny2 - ny1*nx2; 
	 if (denominator==0) { 
	 return false; 
	 } 
	  
	 //在法线N2上的投影 
	 var distC_N2=nx2 * cx + ny2 * cy; 
	 var distA_N2=nx2 * ax + ny2 * ay-distC_N2; 
	 var distB_N2=nx2 * bx + ny2 * by-distC_N2; 
	  
	 // 点a投影和点b投影在点c投影同侧 (对点在线段上的情况,本例当作不相交处理); 
	 if ( distA_N2*distB_N2>=0 ) { 
	 return false; 
	 } 
	  
	 // 
	 //判断点c点d 和线段ab的关系, 原理同上 
	 // 
	 //在法线N1上的投影 
	 var distA_N1=nx1 * ax + ny1 * ay; 
	 var distC_N1=nx1 * cx + ny1 * cy-distA_N1; 
	 var distD_N1=nx1 * dx + ny1 * dy-distA_N1; 
	 if ( distC_N1*distD_N1>=0 ) { 
	 return false; 
	 } 
	  
	 //计算交点坐标 
	 var fraction= distA_N2 / denominator; 
	 var dx= fraction * ny1, 
	 dy= -fraction * nx1; 
	 return true; 
}

function s_s()
{
	console.log("game_being : " + game_being);
	if(game_being)
	{
		clearInterval(time_id);
		game_being = 0;
		console.log("pause");
	}
	else
	{
		time_id = setInterval(Run,2);
		game_being = 1;
		console.log("resume");
	}
}

function Restart()
{
	if(score > best_score)
	{
		best_score = score;
		best_score_input.value = best_score;
	}
	var new_score = score_table.insertRow(1);
	new_score.innerHTML += '<tr><td class = "score_table_th">' + gen + '</td><td class = "score_table_th">' + score + '</td></tr>';
	score_div.value = "YOU DEAD";
	s_s();
	setTimeout(function(){
		InitSnakePos();
		s_s();
		gen++;
	},2);
}

function NextMoveByMe()
{
	snake_dir = tar_dir;
	console.log("HIT------------------------");
	var hit_body = IsAboutToHitBody(new_head);
	console.log("hit_body : " + hit_body);
	console.log("------------------------");
}

function IsAboutToHitBody(head)
{
	var temp_x = head[0];
	var temp_y = head[1];
	var hit_pos = 0;
	var a,b,c,d;
	a = IsEsaInSnake(temp_x-20,temp_y  ,snake_pos,2); //左
	b = IsEsaInSnake(temp_x  ,temp_y-20,snake_pos,2); //上
	c = IsEsaInSnake(temp_x  ,temp_y+20,snake_pos,2); //下
	d = IsEsaInSnake(temp_x+20,temp_y  ,snake_pos,2); //右
	var hit = [a,b,c,d];
	return hit;
}

function SelectIndex(w_arr,rand_val)
{
	/*if(rand_val > 1 - w_arr[0][0])	return w_arr[0][1];
	if(rand_val > 1 - w_arr[1][0])	return w_arr[1][1];
	if(rand_val > 1 - w_arr[2][0])	return w_arr[2][1];
	return w_arr[3][1];*/
	if(rand_val > 0 && rand_val <= w_arr[0][0])
		return w_arr[0][1];
	else if(rand_val > w_arr[0][0]&& rand_val <= w_arr[1][0])
		return w_arr[1][1];
	else if(rand_val > w_arr[1][0] && rand_val <= w_arr[2][0])
		return w_arr[2][1];
	else
		return w_arr[3][1];
}

/*Q相关函数*/
var max_index = 0;
var cur_q_arr = 0;
var sta_id = 0;
function NextMoveByQ()
{
	var new_sta = [0,0,0,0,0,0,0,0,0];
	
	/*判断头朝向*/
	if(snake_dir == 'U')
	{
		new_sta[0] = 0;
		new_sta[1] = 0;
	}
	else if(snake_dir == 'D')
	{
		new_sta[0] = 0;
		new_sta[1] = 1;
	}
	else if(snake_dir == 'L')
	{
		new_sta[0] = 1;
		new_sta[1] = 0;
	}
	else if(snake_dir == 'R')
	{
		new_sta[0] = 1;
		new_sta[1] = 1;
	}
	
	/*判断食物方向*/
	if(new_head[0] == esa_pos_x && new_head[1] >= esa_pos_y)//上
	{
		new_sta[2] = 0;
		new_sta[3] = 0;
		new_sta[4] = 0;
	}
	else if(new_head[0] == esa_pos_x && new_head[1] <= esa_pos_y)//下
	{
		new_sta[2] = 0;
		new_sta[3] = 0;
		new_sta[4] = 1;
	}
	if(new_head[1] == esa_pos_y && new_head[0] >= esa_pos_x)//左
	{
		new_sta[2] = 0;
		new_sta[3] = 1;
		new_sta[4] = 0;
	}
	else if(new_head[1] == esa_pos_y && new_head[0] <= esa_pos_x)//右
	{
		new_sta[2] = 0;
		new_sta[3] = 1;
		new_sta[4] = 1;
	}
	if(new_head[0] > esa_pos_x && new_head[1] > esa_pos_y)//上左
	{
		new_sta[2] = 1;
		new_sta[3] = 0;
		new_sta[4] = 0;
	}
	else if(new_head[0] > esa_pos_x && new_head[1] < esa_pos_y)//下左
	{
		new_sta[2] = 1;
		new_sta[3] = 0;
		new_sta[4] = 1;
	}
	if(new_head[1] > esa_pos_y && new_head[0] < esa_pos_x)//上右
	{
		new_sta[2] = 1;
		new_sta[3] = 1;
		new_sta[4] = 0;
	}
	else if(new_head[1] < esa_pos_y && new_head[0] < esa_pos_x)//下右
	{
		new_sta[2] = 1;
		new_sta[3] = 1;
		new_sta[4] = 1;
	}
	
	/*判断障碍位置*/
	var hit_body = IsAboutToHitBody(new_head);
	console.log("hit_body : " + hit_body);
	new_sta[5] = hit_body[0];
	new_sta[6] = hit_body[1];
	new_sta[7] = hit_body[2];
	new_sta[8] = hit_body[3];
	
	if(new_head[0] - 20 <= 0) //左
		new_sta[5] = 0;
	if(new_head[1] - 20 <= 0) //上
		new_sta[6] = 0;
	if(new_head[1] + 20 >= 580) //下
		new_sta[7] = 0;
	if(new_head[0] + 20 >= 580) //右
		new_sta[8] = 0;	
	
	
	sta_id = 0;
	for(var ii = 9-1; ii >= 0; ii--)
		sta_id += new_sta[ii] * Math.pow(2,ii);
	console.log("sta_id : " + sta_id);
	
	/*选择Q值*/
	cur_q_arr = Q_table[sta_id];
	max_index = 0;
	for(var jj = 0; jj < 4; jj++)
	{
		if(cur_q_arr[jj] > cur_q_arr[max_index])
			max_index = jj;
	}
	var cur_max_value = cur_q_arr[max_index];
	console.log("max : " + max_index + " : " + cur_max_value);
	
	if(cur_q_arr[0] == 0 && cur_q_arr[1] == 0 && cur_q_arr[2] == 0 && cur_q_arr[3] == 0)
	{
		max_index = parseInt(Math.random() * 20) % 4;
	}
	else
	{
		max_index = max_index;
	}
	
	/*计算权重*/
	//var temp_cur_q_arr = cur_q_arr;
	//cur_q_arr_w = [0,0,0,0];
	//var cur_q_arr_sum = 0;
	///*找最小值*/
	//var min_index = 0;
	//for(var jjj = 0; jjj < 4; jjj++)
	//{
	//	if(temp_cur_q_arr[jjj] < temp_cur_q_arr[min_index])
	//		min_index = jjj;
	//}
	//for(jjj = 0; jjj < 4; jjj++)
	//{
	//	temp_cur_q_arr[jjj] -= temp_cur_q_arr[min_index]
	//}
	//
	//for(jjj = 0; jjj < 4; jjj++)
	//{
	//	cur_q_arr_sum += temp_cur_q_arr[jjj];
	//}
	//cur_q_arr_w[0] = temp_cur_q_arr[0] / cur_q_arr_sum;
	//cur_q_arr_w[1] = temp_cur_q_arr[1] / cur_q_arr_sum;
	//cur_q_arr_w[2] = temp_cur_q_arr[2] / cur_q_arr_sum;
	//cur_q_arr_w[3] = temp_cur_q_arr[3] / cur_q_arr_sum;
	//
	///*重新划分权重*/
	//var w_redistribution = 0;
	//var max_w = 0.98;
	//for(jjj = 0; jjj < 4; jjj++)
	//{
	//	if(cur_q_arr_w[jjj] > cur_q_arr_w[max_index])
	//		max_index = jjj;
	//}
	//if(cur_q_arr_w[max_index] > max_w)
	//{
	//	w_redistribution = cur_q_arr_w[max_index] - max_w;
	//	cur_q_arr_w[max_index] = max_w;
	//	for(jjj = 0; jjj < 4; jjj++)
	//	{
	//		if(jjj != max_index)
	//			cur_q_arr_w[jjj] += w_redistribution / 3;
	//	}
	//}
	//console.log(cur_q_arr_w);
	//
	///*根据概率选择Q值*/
	//var rand = Math.random();
	//max_index = 0;
	//var new_cur_q_arr_w = [[cur_q_arr_w[0],0],[cur_q_arr_w[1],1],[cur_q_arr_w[2],2],[cur_q_arr_w[3],3]];
	//new_cur_q_arr_w.sort(function(a,b){
	//	return b[0] - a[0];
	//});
	//max_index = SelectIndex(new_cur_q_arr_w,rand);
	
	//console.log("rand : " + rand + " CHOSED---Q : [" + max_index + "] Q :" + cur_q_arr[max_index]);
	
	/*选择动作*/
	if(max_index == 0 && snake_dir != 'D')
		snake_dir = 'U';
	else if(max_index == 1 && snake_dir != 'U')
		snake_dir = 'D';
	else if(max_index == 2 && snake_dir != 'R')
		snake_dir = 'L';
	else if(max_index == 3 && snake_dir != 'L')
		snake_dir = 'R';
}

function Run()
{
	left_time -= 5;
	cur_q_arr[max_index] = cur_q_arr[max_index] + 1;
	FreshQtableElement(sta_id,max_index,cur_q_arr[max_index]);
	
	/*时间尽*/
	if(left_time <= 10)
	{
		console.log("!!!!SHIJIANMEILE!!!");
		cur_q_arr[max_index] = cur_q_arr[max_index] - 10;
		FreshQtableElement(sta_id,max_index,cur_q_arr[max_index]);
		Restart();
		return;
	}
	
	time_div.value = left_time;
	
	ctx.clearRect(0,0,600,600);
	
	/*人动作控制*/
	//NextMoveByMe();
	
	/*Q_table动作控制*/
	NextMoveByQ();
	
	new_head = new Array(2);
	new_head[0] = snake_pos[0][0];
	new_head[1] = snake_pos[0][1];

	for(var i = snake_length - 1; i > 0; i--)
	{
		snake_pos[i] = snake_pos[i - 1];
	}
	

	if(snake_dir == 'R')
		new_head[0] = new_head[0] + 20;
	else if(snake_dir == 'L')
		new_head[0] = new_head[0] - 20;
	else if(snake_dir == 'U')
		new_head[1] = new_head[1] - 20;
	else if(snake_dir == 'D')
		new_head[1] = new_head[1] + 20;
	snake_pos[0] = new_head;
	
	/*撞墙*/
	if(new_head[0] < 0 || new_head[0] > 580 || new_head[1] < 0 || new_head[1] > 580)
	{
		console.log("!!!!!ZHUANG QIANG!!!");
		cur_q_arr[max_index] = cur_q_arr[max_index] - 300;
		FreshQtableElement(sta_id,max_index,cur_q_arr[max_index]);
		Restart();
		return;
	}
	/*吃自己*/
	if(IsEsaInSnake(new_head[0],new_head[1],snake_pos,1))
	{
		console.log("!!!!!!CHIZIJI!!!");
		cur_q_arr[max_index] = cur_q_arr[max_index] - 200;
		FreshQtableElement(sta_id,max_index,cur_q_arr[max_index]);
		Restart();
		return;
	}
	
	/*进了一步*/
	esa_distance = Math.sqrt(Math.pow((new_head[0] - esa_pos_x),2) + Math.pow((new_head[1] - esa_pos_y),2));
	console.log("esa_distance : " + esa_distance);
	if(esa_distance < old_esa_distance)      //变近
	{
		cur_q_arr[max_index] = cur_q_arr[max_index] + 50;
		FreshQtableElement(sta_id,max_index,cur_q_arr[max_index]);
	}
	else if(esa_distance > old_esa_distance) //变远
	{
		cur_q_arr[max_index] = cur_q_arr[max_index] - 20;
		FreshQtableElement(sta_id,max_index,cur_q_arr[max_index]);
	}
	
	/*吃到*/
	if(snake_pos[0][0] == esa_pos_x && snake_pos[0][1] == esa_pos_y)
	{
		cur_q_arr[max_index] = cur_q_arr[max_index] + 200 + parseInt(left_time / 10);
		FreshQtableElement(sta_id,max_index,cur_q_arr[max_index]);
		left_time += 300;
		score += 50;
		score_div.value = score;
		
		if(left_time > 1000)
			left_time = 1000;
		console.log("TABETA!" + snake_length);
		snake_pos[snake_length] = new Array(2);
		snake_length++;
		for(var i = snake_length - 1; i > 0; i--)
		{
			snake_pos[i][0] = snake_pos[i - 1][0];
			snake_pos[i][1] = snake_pos[i - 1][1];
		}
		if(snake_dir == 'R')
			snake_pos[0][0] = esa_pos_x + 20;
		else if(snake_dir == 'L')
			snake_pos[0][0] = esa_pos_x - 20;
		else if(snake_dir == 'U')
			snake_pos[0][1] = esa_pos_y - 20;
		else if(snake_dir == 'D')
			snake_pos[0][1] = esa_pos_y + 20;
		
		var esa = new Array(2);
		do
		{
			esa_pos_x = parseInt(Math.random() * 560 / 20) * 20 + 20;
			esa_pos_y = parseInt(Math.random() * 560 / 20) * 20 + 20;
			esa[0] = esa_pos_x;
			esa[1] = esa_pos_y;
			//console.log("new eas : " + esa_pos_x + "," + esa_pos_y + " snake_pos.includes(esa) : " + snake_pos.includes(esa));
		}while(IsEsaInSnake(esa,snake_pos,0));
	}
	
	for(i = 0; i < snake_length; i++)
	{
		ctx.fillRect(snake_pos[i][0],snake_pos[i][1],20,20);
	}
	ctx.fillRect(esa_pos_x,esa_pos_y,20,20);
	
	time_ctx_width = left_time / 1000 * 600;
	time_ctx.clearRect(0,0,600,20);
	time_ctx.fillRect(0,0,time_ctx_width,20);
	
	old_esa_distance = esa_distance;
}

document.onkeydown = function(event){
	var e = event || window.event || arguments.callee.caller.arguments[0];
	console.log(e.keyCode);
	if(game_being)
	{
		if(e.keyCode == 37 && snake_dir != 'R')
			tar_dir = 'L';
		if(e.keyCode == 38 && snake_dir != 'D')
			tar_dir = 'U';
		if(e.keyCode == 39 && snake_dir != 'L')
			tar_dir = 'R';
		if(e.keyCode == 40 && snake_dir != 'U')
			tar_dir = 'D';
	}
	
	if(e.keyCode == 80)
		s_s();
		
	if(e.keyCode == 82)
		Restart();
}; 

InitSnakePos();
s_s();
