function dologin() {
var login = $('#username').val();
var pass = $('#password').val();

$.post("/login/", { 			
	'username':login,'password':pass
	 },function(data) {

		if (data==1 ){
			humane.log("Добро пожаловать!")
			location.reload(true);
		}else{	
			humane.log("Не верный логин или пароль!")
			return false;
		}
	   });
}

function doOut() {
$.post("/logout/", { 			
	 },function(data) {
        	humane.log("<b>Возвращайтесь снова!!</b>")
		location.reload(true);
	   });
}

