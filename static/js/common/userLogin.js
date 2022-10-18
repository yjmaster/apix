console.log("userLogin.js");

let media = '';
let login_url = '';
let main_url = '';
let apiUrl = '';
let os = Utils.getOS();
let pathName = window.location.pathname;

if(os === 'Windows'){
  apiUrl = 'http://localhost:5000';
}else{
  apiUrl = 'http://211.232.77.118:10001';
};

if(pathName.includes('kpf')){
    media = "kpf";
    login_url = `${apiUrl}/${media}/login`;
    main_url = `${apiUrl}/${media}`;
}else{
    media = "yjmedia";
    login_url = `${apiUrl}/login`;
    main_url = `${apiUrl}/`;
}

if(isLogin !== ''){
    alert(isLogin);
    window.location = login_url;
}

// if($.cookie('access_token')){    
//     window.location = main_url;
// }

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

    //console.log("login_url : ", login_url);
    let loginData = { user_login, password, media };

    $.ajax({
        url: login_url,
        contentType: 'application/json',
        method: 'POST',
        data: JSON.stringify(loginData)
    }).done(function(res){
        console.log(res)
        if(res.success){
            $.cookie('access_token', res.access_token);
            console.log("main_url", main_url)
            window.location = main_url;
        }else{
            alert(res['message']);
            return false;
        }
    });
}