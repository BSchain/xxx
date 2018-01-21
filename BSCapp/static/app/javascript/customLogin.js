/*function validateSignUp() {
  $("#formRegister").validate({
    submitHandler: function() {
      Func_signUp();
    },
    rules: {
      inputEmail: {
        required: true,
	      email: true
      },
      inputUsername: {
        required: true,
	      minlength: 2
	    },
	    inputPassword: {
	      required: true,
	      minlength: 5
	    },
      inputVerify: {
        required: true,
	      minlength: 5,
	      equalTo: "#inputPassword"
      }
    },
    messages: {
      inputEmail: "请输入正确的邮箱地址",
      inputUsername: {
        required: "请输入用户名",
        minlength: "用户名长度不能小于2个字符"
      },
      inputPassword: {
        required: "请输入密码",
        minlength: "密码长度不能小于5个字符"
      },
      inputVerify: {
        required: "请再次输入密码",
        minlength: "密码长度不能小于5个字符",
        equalTo: "密码输入不一致"
      }
    }
  })
}

function validateSignIn() {
  $("#formLogin").validate({
    submitHandler: function() {
      Func_signIn();
    },
    rules: {
      username: {
        required: true,
	      minlength: 2
	    },
	    password: {
	      required: true,
	      minlength: 5
	    }
    },
    messages: {
      username: {
        required: "请输入用户名",
        minlength: "用户名必需由两个字符组成"
      },
      password: {
        required: "请输入密码",
        minlength: "密码长度不能小于 5 个字符"
      }
    }
  })
}

function Func_signUp() {
  pwd = $("#inputPassword").val()
  $.ajax("/signUp/", {
    dataType: 'json',
    type: 'POST',
    data: {
      "username": $("#inputUsername").val(),
      "mail": $("#inputEmail").val(),
      "password": pwd,
    }
  }).done(function(data) {
    if (data.statCode != 0) {
      alert(data.errormessage)
    } else {
      location.reload();
      $("#menuLogin").hide()
      $("#menuUser").show()
      $("#navUser").text(data.username)
      $.cookie('username', data.username, {path: '/'})
      $.cookie('password', md5(pwd), {path: '/'})
    }
  })
}
*/
function Func_validate() {
  pwd = $("#password").val()
  $.ajax({
    url: '/signin/',
    dataType: 'json',
    type: 'POST',
    data: {
      "username": $("#username").val(),
      "password": pwd,
    }
  }).done(function(data) {
    if(data.statCode != 0) {
      alert(data.errormessage)
      return(false)
    } else {
     $.cookie('username', data.username, {path: '/'})
     $.cookie('password', md5(pwd), {path: '/'})
     indexURL = "/customInfo/"
     window.location.replace(indexURL);
     return(true)
     /*
      $("#navLogin").hide()
      $("#navUser").show()
      $("#navUser").text(data.username)*/
    }
  })
}

/*
function Func_signOut() {
  $("#navUser").hide()
  $("#navLogin").show()
  $.removeCookie('username', {path: '/'})
  $.removeCookie('password', {path: '/'})
  location.reload()
}

function Func_gotoMyPage() {
  myPageURL = "/user/" + $("#navUser").text()
  window.location.replace(myPageURL);
}

function setCookie() {
  if($.cookie('username') == undefined) {
    $("#navUser").hide()
    $("#navLogin").show()
  }
  else{
    $("#navLogin").hide()
    $("#navUser").show()
    $("#navUser").text($.cookie('username'))
  }
}
*/
