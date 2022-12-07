const escapeEmpty = function(value){if(value == null || value == undefined){return ""}else{ return value }}

let Utils = {
	call: function(method, url, data, callback){
		$.ajax({
			url: url,
			contentType: 'application/json',
			method: method,
			// dataType: "json",
			data: data,
			async: false,
			beforeSend: function(xhr){
				$.LoadingOverlay("show", {
					background: "rgba(0, 0, 0, 0.5)",
					spinnerIcon: 'ball-circus',
					imageColor: "#ffffffcc",
					maxSize: 30
				});
			},
			error: function(jqXHR, textStatus, errorThrown){
				callback(jqXHR.responseJSON);
				$.LoadingOverlay("hide");
			}
		}).done(function(res){
			callback(res);
			$.LoadingOverlay("hide");
		});
	},
	isEmpty: function(param){
		return Object.keys(param).length === 0;
	},
	noSpaceForm: function(obj){
		let str_space = /\s/;
    if(str_space.exec(obj.value)) {
        obj.focus();
        obj.value = obj.value.replace(/\s| /gi,'');
        return false;
		}
	},
	logout: function(){
		if($.cookie('access_token')){
				$.removeCookie('access_token');
				alert("You are logged out");
		}else{
				alert('token does not exist');
		}
		window.location = `/${Main.media}/login`;
	}
}