var http = require('http');
var mysql = require('mysql');
var url = require('url');
var fs = require('fs');
var path = require('path');

var http = require('http');
var fs = require('fs');

var dir = 'public/';

var con = mysql.createConnection({
	host: "39.107.76.131",
	user: "wewall2018",
	password: "!Ima#gine@2018$sTuFes",
	database: "wewall2018"
});

con.connect(function(err){
	if(err){
		console.log('connection error!');
		throw err;
	}
	console.log("Connected!");
});

function getUserName(userID){
	sql = "select username from wewall_username where id = '" + userID + "'"; 
	con.query(sql, function(err, result){
		if(err){
			console.log(err);
			return "Undefined";
		}
		if(result.length == 0){
			return "Undefined";
		}
		return result[0].username;
	});
}

function getMsg(){
	sql = "select * from wewall_msg where checked = 1 and wall = 0 limit 1;";
	var dic = new Array();
	con.query(sql, function(err, result){
		if(err) {
			console.log("query error!");
			throw err;
		}
		if(result.length == 0)
			dic['new'] = 0;
		else{
			dic['new'] = 1;
			dic['userid'] = result[0].userID;
			dic['content'] = result[0].content;
			dic['content'] = getUserName(result[0].userID);
		}
	});
	return dic;
}

function handle_request(req, res) {

  var pathname = url.parse(req.url).pathname;
  console.log(pathname);
  if(pathname == '/update'){
		res.writeHead(200, {"Content-Type": "application/json"});
		
		sql = "select * from wewall_msg where checked = 1 and wall = 0 limit 1;";
		var dic = {};
		con.query(sql, function(err, result){
			if(err) {
				console.log("query error!");
				//throw err;
				return ;
			}
			if(result.length == 0){
				dic['new'] = 0;
				res.end(JSON.stringify(dic));
				return ;
			}
			else{
				dic['new'] = 1;
				dic['userid'] = result[0].userID;
				dic['content'] = result[0].content;
				//dic['content'] = getUserName(result[0].userID);
				//console.log(result[0].id);
				sql = "update wewall_msg set wall = 1 where id = " + result[0].id;
					con.query(sql, function(err, result){
						if(err){
							console.log(err);
						}
						console.log("succeed");
					});
			}
			//console.log(dic);
			sql = "select username from wewall_username where id = '" + result[0].userID + "'"; 
			con.query(sql, function(err, result){
				if(err){
					console.log(err);
					dic['username'] = "Undefined";
					//throw err;
					return ;
				}
				if(result.length == 0){
					dic['username'] = "Undefined";
					//res.end(JSON.stringify(post_data));
				}else{
					dic['username'] = result[0].username;
				}
				//console.log(dic);
				console.log(JSON.stringify(dic));
				
				res.end(JSON.stringify(dic));
			});
		});

		con.query("select count(*) from wewall_msg where checked = 1 and wall = 0;", function(err, result){
			if(err){
				console.log("query remaining number error!");
				return;
			}
			console.log("remaining:" + result[0]['count(*)']);
		});
  }else if(pathname == '/'){
		res.writeHead(200, {"Content-Type": "text/html"});
		fs.readFile('public/index.html', function(err, data){
			if(err){
				console.log(err);
				//throw err;
				res.end();
			}
			res.end(data);
		});
  }else{
	  fs.readFile(dir + pathname.substr(1), function(err, data){
			if(err){
				//console.log(err);
				//throw err;
				res.writeHead(404, {'Content-Type': 'text/html'});
				res.end();
			}else{
				switch(path.extname(pathname)){
                    case ".js":
                        res.writeHead(200, {"Content-Type": "text/javascript"});
                        break;
                    case ".css":
                        res.writeHead(200, {"Content-Type": "text/css"});
                        break;
                    case ".gif":
                        res.writeHead(200, {"Content-Type": "image/gif"});
                        break;
                    case ".jpg":
                        res.writeHead(200, {"Content-Type": "image/jpeg"});
                        break;
                    case ".png":
                        res.writeHead(200, {"Content-Type": "image/png"});
                        break;
                    default:
                        res.writeHead(200, {"Content-Type": "text/html"});
                }
                res.end(data);
			}
	  });
  }
}

function get_file_content(filepath) {
  return fs.readFileSync(filepath);
}

var server = http.createServer(handle_request);
server.listen(8080);



console.log('Listen on 8080.');


