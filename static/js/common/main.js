let Main = {
  init: function(){
    console.log("Main init()");

    let pathName = window.location.pathname;
    // let apiUrl = 'http://localhost:5000';
    let apiUrl = 'http://211.232.77.118:10001';

    this.userList = [];
    this.latestOpned = null;

    if(pathName.includes('kpf')){
      this.media = "kpf";
      this.apiUrl = apiUrl;
    }
    this.eventBind();
    this.getUserList({}, 'list');
  },
  eventBind: function(){
    $('#search').click(function(e){
      Main.searchOption();
    });

    $(".search-input").keydown(function(key){
      if(key.keyCode == 13){
        Main.searchOption();
        return false;
      }
    });

    $(".user-list").on("click", e => {
      const inputForm = $('.needs-validation')[0];
      $(inputForm).removeClass('was-validated');

      let clickedTarget = $(e.target);
      let activeStatus = clickedTarget.closest("li");
      
      let targetTag = clickedTarget.get(0);
      if(targetTag.tagName === 'BUTTON'){
        this.eventBtn(clickedTarget);
      }else{
        if(activeStatus.hasClass("disabled")){
          return false;
        }
        this.eventRow(clickedTarget);
      }
    });

    $('#reset-btn').click(function(){
      Main.getUserList({}, 'list');
      $('.search-input').val('');
      $('#option_user').val('user_login');
    });

    $('#register').click(function(e){
      let btnType = $(e.target).attr("mode");
      let inputForm = $('.needs-validation')[0];
      let pwdValid = (btnType === 'register' ? true : false);

      $('.needs-validation input[type="password"]')
        .attr('required', pwdValid);

      if(inputForm.checkValidity()){
        let password = $('#user_pwd1').val();
        let re_password = $('#user_pwd2').val();

        if(password !== re_password){
          alert("비밀번호가 맞지 않습니다.");
          return false;
        }

        let user_login = $('#user_login').val();
        let user_name = $('#user_name').val();
        let media = $('#media').val();
        let role = 'C';

        let registerData = {
          user_login, user_name, media, role };
        
        if(password){
          registerData['password'] = password
        }

        Main.setUser(registerData, btnType);
      }else{
        $(inputForm).addClass('was-validated');
      }
    });
  },
  eventBtn: function(clickedTarget){
    let targetRow = clickedTarget.closest("li");
    let clickedBtn = clickedTarget.closest("button").text();

    if(clickedBtn === 'token'){
      let rowIdx = targetRow.index();
      let access_token = this.userList[rowIdx].access_token;

      let textArea = document.createElement("textarea");
      textArea.value = access_token;
      textArea.style.position = "fixed";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();

      try{
        let successful = document.execCommand('copy');
        let msg = successful ? 'token copied' : 'token copy failed';
        alert(msg);
      }catch(err){
        console.error('Was not possible to copy te text: ', err);
      };

      document.body.removeChild(textArea);
      return;
      // window.navigator.clipboard.writeText(access_token).then(() => {
      //   alert("token copied");
      // });
    }else{
      let useYn = (clickedBtn === 'disabled' ? 'N' : 'Y');
      let user_login = $(targetRow).find('#user_login_list').text();
      let media = $(targetRow).find('#user_media_list').text();
      let regExp = /\(([^)]+)\)/;
      let matches = regExp.exec(media);
      media = matches[1];
      this.setUserYn({user_login, media, useYn});
    }
  },
  eventRow: function(clickedTarget){
    let targetRow = clickedTarget.closest("li");
    if (this.latestOpned?.get(0) === targetRow?.get(0)) {
      this.latestOpned = targetRow;
      return;
    }
    this.latestOpned?.removeClass("bg-light");

    targetRow.addClass("bg-light");
    this.latestOpned = targetRow;

    let user_login =  targetRow.find('#user_login_list').text();
    let media =  targetRow.find('#user_media_list').text();
    
    let regExp = /\(([^)]+)\)/;
    let matches = regExp.exec(media);
    media = matches[1];

    let userData = { user_login, media };
    this.getUserList(userData, 'form');
  },
  searchOption: function(){
    let option_user = $("#option_user option:selected").val();
    let searchText = $(".search-input").val().trim();
    if(searchText === ""){
      $('#option_user').val('user_login');
      this.getUserList({}, 'list');
      return false;
    }
    let userData = {};
    userData[option_user] = searchText;
    this.getUserList(userData, 'list');
  },
  getUserList: function(userData, type){
    let url = `${this.apiUrl}/auth/user`;
    Utils.call('GET', url, userData, function(res){
      if(res.success){
        if(type === 'list'){
          Main.setUserList(res);
        }else if(type === 'form'){
          Main.setUserForm(res);
        }
      }else{
        alert(res.message);
      }
    })
  },
  setUser: function(userData, type){
    let url = `${this.apiUrl}/auth/${type}`;
    let userId = userData['user_login'];
    userData = JSON.stringify(userData);

    let methodType = (type === 'register' ? 'POST' : 'PUT');
    Utils.call(methodType, url, userData, function(res){
      alert(res.message);
      if(res.success){
        if(type === 'register'){
          $('#reset-btn').click();
        }else{
          $(`#user_login_list[login='${userId}']`).click();
        }
      }
    })
  },
  setUserYn: function(userData){
    let url = `${this.apiUrl}/auth/yn`;
    userData = JSON.stringify(userData);
    Utils.call('PUT', url, userData, function(res){
      if(res.success){
        $('#reset-btn').click();
      }
      alert(res.message);
    });
  },
  setUserList: function(res){
    this.setUserForm({});
    this.userList = res.result;

    let cnt = (this.userList).length;
    $('#userCnt').text(cnt);

    let user_html = '';
    for(let [idx, user] of (this.userList).entries()){
      let isDisabled = (user.useYn == 'Y' ? '': 'disabled');
      let btnType = (user.useYn == 'Y' ?
        '<button type="button" class="btn btn-danger btn-sm">disabled</button>':
        '<button type="button" class="btn btn-success btn-sm">activate</button>');
  
      user_html += `
        <li class="list-group-item list-group-item-action ${isDisabled} d-flex justify-content-between lh-sm">\n
          <div>\n
            <h6 class="my-0">
              <span id='user_login_list' login='${user.user_login}'>${user.user_login}</span>
              <span id='user_media_list'>(${user.media})</span>
            </h6>\n
            <small class="text-muted">${user.register_date}</small>\n
            <small class="text-muted">| ${user.update_date}</small>\n
          </div>\n
          <span class="text-muted">\n
            <button type="button" class="btn btn-primary btn-sm" ${isDisabled}>token</button>\n
            ${btnType}\n
          </span>\n
        </li>\n`;
      $('.user-list').html(user_html);
    }
  },
  setUserForm: function(res){
    let titleTxt = '';
    let btnTxt = '';
    let modeAttr = '';
    let idValid = true;
    $('.needs-validation input').val('');
    
    if(!Utils.isEmpty(res)){
      titleTxt = 'User Update';
      btnTxt = '수정하기';
      modeAttr = 'update'

      let user = res.result[0];
      
      $('#user_login').val(user.user_login);
      $('#user_name').val(user.user_name);
      $('#media').val(user.media);
    }else{
      idValid = false;
      titleTxt = 'User Register';
      btnTxt = '등록하기';
      modeAttr = 'register'
    }

    $('#user_login').attr('disabled',idValid);
    $('#form_type').text(titleTxt);
    $('#register').text(btnTxt);
    $('#register').attr('mode',modeAttr);
  }
}