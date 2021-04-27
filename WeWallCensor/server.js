var http = require('http');
var mysql = require('mysql');
var url = require('url');
var fs = require('fs');
var path = require('path');
var express = require('express');
var bodyParser = require('body-parser');

var http = require('http');
var fs = require('fs');

var dir = 'public/';

var size = 15;

var con = mysql.createConnection({
	host: "39.107.76.131",
	user: "wewall2018",
	password: "!Ima#gine@2018$sTuFes",
	database: "wewall2018"
});

function reserve(id){
	sql = "update wewall_msg set checked = 1 where id = " + id + ";";
	con.query(sql, function(err, result){
		if(err) {
			console.log("query error!");
		}
	});
}

function del(id){
	sql = "update wewall_msg set checked = 2 where id = " + id + ";";
	con.query(sql, function(err, result){
		if(err) {
			console.log("query error!");
		}
	});
}

con.connect(function(err){
	if(err){
		console.log('connection error!');
		throw err;
	}
	console.log("Connected!");
});

var server = express();
server.use(bodyParser.json());
server.use(express.static('public'));

server.get('/', function(req, res){
	fs.readFile('public/index.html', function(err, data){
			if(err){
				console.log(err);
				//throw err;
				res.send();
			}
			res.send(data);
		});
});

server.post('/reserve', function(req, res){
	var dic = req.body;
	var i;
	for(i=0;i<dic['num'];++i)
		reserve(dic['list'][i]);
	res.send("succeed!");
});

server.post('/delete', function(req, res){
	var dic = req.body;
	console.log(dic);
	var i;
	for(i=0;i<dic['num'];++i)
		del(dic['list'][i]);
	res.send("succeed!");
});

server.get('/update', function(req, res){
	sql = "select id, content from wewall_msg where checked = 0 limit " + size + ";";
	var dic = {};
	con.query(sql, function(err, result){
		if(err) {
			console.log("query error!");
			//throw err;
			return ;
		}
		dic['num'] = result.length;
		dic['list'] = result;
		sql = "select count(*) from wewall_msg where checked = 0;"; 
		con.query(sql, function(err, result){
			if(err){
				console.log(err);
				dic['username'] = "Undefined";
				//throw err;
				return ;
			}
			dic['remain'] = result[0]['count(*)'];
			console.log(JSON.stringify(dic));
			
			res.send(JSON.stringify(dic));
		});
	});
});


server.listen(7070);
console.log('Listen on 7070.');
