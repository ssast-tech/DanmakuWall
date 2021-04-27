var g_json; 

var auto = false;

var t;

function loadDoc() {
  console.log("in");
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
	  g_json = JSON.parse(this.responseText);
	  fillContent(g_json);
	  if(auto == false){
	  	t = setTimeout("loadDoc()", 1500);
	  }
	  else{
	  	resall();
	  }
    }
  };
  xhttp.open("GET", "/update", true);
  xhttp.send();
}

loadDoc();

function del(id){
	var json = {};
	json['num'] = 1;
	json['list'] = [id];
	$.ajax({  
		type: "POST",  
		url: "/delete",  
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify(json),
		complete:function(data) { 
			clearTimeout(t); 
			loadDoc();
		}
	});
}

function res(id){
	var json = {};
	json['num'] = 1;
	json['list'] = [id];
	$.ajax({  
		type: "POST",  
		url: "/reserve",  
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify(json),
		complete:function(data) {  
			clearTimeout(t);
			loadDoc();
		}
	});
}

function resall(){
	var json = {};
	json['num'] = g_json['list'].length;
	json['list'] = [];
	var i;
	for(i=0;i<json['num'];++i)
		json['list'][i] = g_json['list'][i]['id'];
	console.log(JSON.stringify(json));
	$.ajax({  
		type: "POST",  
		url: "/reserve",  
		contentType: "application/json", 
		dataType: "json",
		data: JSON.stringify(json),
		complete:function(data) {  
			clearTimeout(t);
			loadDoc();
		}
	});
}

function delall(){
	var json = {};
	json['num'] = g_json['list'].length;
	json['list'] = [];
	var i;
	for(i=0;i<json['num'];++i)
		json['list'][i] = g_json['list'][i]['id'];
	console.log(JSON.stringify(json));
	$.ajax({  
		type: "POST",  
		url: "/delete",   
		contentType: "application/json",  
		dataType: "json",
		data: JSON.stringify(json),
		complete:function(data) {  
			loadDoc();
		}
	});
}

function fillContent(json){
	console.log(json);
	
	var i;
	var remain = document.getElementById('remain');
	remain.innerHTML = "remain:" + json['remain'];
	
	var container = document.getElementById('container');
	container.innerHTML = "";
	for(i = 0; i < json['num']; ++i){
		container.innerHTML = container.innerHTML + "<div class='row'>"
						+ "<div class='content col-8'>" + json['list'][i]['content'] 
						+ "</div><div class='col-4'><button class='btn btn-primary' onclick='res(" + json['list'][i]['id'] + ")'>Reserve</button>"
						+ "&nbsp;&nbsp;<button class='btn btn-danger' onclick='del(" + json['list'][i]['id'] + ")'>Delete</button></div></div>";
	}
}

function AutoCensor(){
	if(auto == false){
		document.getElementById('auto').innerHTML = "关闭自动审核";
		clearTimeout(t);
		loadDoc();
		auto = true;
	}else{
		document.getElementById('auto').innerHTML = "开启自动审核";
		auto = false;
		//loadDoc();
	}
}