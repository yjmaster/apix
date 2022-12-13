let pathName = window.location.pathname;

$("#password").keydown(function (key){
    if(key.keyCode == 13){
        userLogin();
    }
});

function userLogin(){
    let user_login = $('#user_login').val();
    let password = $('#user_pwd').val();

    if(user_login === ""){
        alert("아이디를 입력해주세요.");
        return false;
    }
    if(password === ""){
        alert("비밀번호를 입력해주세요.");
        return false;
    }

    let loginData = { user_login, password };

    $.ajax({
        url: '/login',
        contentType: 'application/json',
        method: 'POST',
        data: JSON.stringify(loginData)
    }).done(function(res){
        if(res.success){
            let date = new Date();
            var minutes = 120; 
            date.setTime(date.getTime() + (minutes * 60 * 1000));
            $.cookie("access_token", res.id_client, { expires: date });
            window.location = '/demo';
        }else{
            alert(res['message']);
            return false;
        }
    });
}