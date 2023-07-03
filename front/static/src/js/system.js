function Auth() {
    this.errorTips = $("#error_tips");
    this.errorTips.hide();
    this.imageCodeId = "";
}


//获取url中的参数
Auth.prototype.getUrlParam = function (name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return unescape(r[2]);
    return null; //返回参数值
};

// 生成UUID
Auth.prototype.generateUUID = function () {
    var d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    var uuid_code = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid_code;
};

// 生成图片验证码
Auth.prototype.generateImageCode = function () {
    var self = this;
    var preImageCodeId = self.imageCodeId;
    // 新的要请求的图片验证码的编号
    self.imageCodeId = self.generateUUID();
    // "src", "/api/imagecode?p="+preImageCodeId+"&c="+imageCodeId
    $("#imgshow").attr('src', '/system/img_captcha/?p=' + preImageCodeId + '&c=' + self.imageCodeId);
};

// 图片验证码更新
Auth.prototype.listCaptchaUpdate = function () {
    var self = this;
    $("#kanbuq").click(function () {
        self.generateImageCode();
    });
};

// 错误提示
Auth.prototype.tipsShow = function (t) {
    var self = this;
    self.errorTips.text(t);
    self.errorTips.show().delay(2000).fadeOut();
};

Auth.prototype.loginHandler = function () {
    var self = this;
    var username = $("#user").val();
    var password = $("#pass").val();
    var img_captcha = $("#imgcode").val();
    if (!username) {
        self.tipsShow("请输入用户名");
        return null;
    } else if (!password) {
        self.tipsShow("请输入密码");
        return null;
    } else if (!img_captcha) {
        self.tipsShow("请输入验证码");
        return null;
    } else {
        self.errorTips.hide();
        stockajax.post({
            'url': '/system/login/',
            'data': {
                'username': username,
                'password': password,
                'img_captcha': img_captcha,
                'img_code_id': self.imageCodeId
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var next = self.getUrlParam("next");
                    if (next) {
                        window.location.href = next;
                    } else {
                        window.location.href = "/system/index/";
                    }

                }
            }
        });
    }
};

// 登录按钮
Auth.prototype.listenSignupEvent = function () {
    var self = this;

    $("#btn-Login").click(function () {
        self.loginHandler();
    });

    $(window).keydown(function (event) {
        if (event.keyCode == "13") {
            self.loginHandler();
        }
    });
};


// 修改当前登录用户密码
Auth.prototype.updatePasswordEvent = function () {
    $("#change-pwd-btn").click(function () {
        // 获取表单数据
        var oldPwd = $("#old_pass").val();
        var newPwd = $("#password").val();
        var newPwd2 = $("#password_confirm").val();
        // 表单验证
        if (!oldPwd) {
            layer.msg('请输入原始登录密码', {icon: 2, time: 2000});
            return null;
        } else if (!newPwd || !newPwd2) {
            layer.msg('请输入新的登录密码', {icon: 2, time: 2000});
            return null;
        } else if (!(newPwd2 === newPwd)) {
            layer.msg("两次输入的密码不一致", {icon: 2, time: 2000});
            return null;
        } else {
            stockajax.post({
                'url': '/system/changepwd/',
                'data': {
                    'oldpwd': oldPwd,
                    'newpwd1': newPwd,
                    'newpwd2': newPwd2
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.msg("修改登录密码成功", {icon: 1, time: 1000}, function () {
                            window.location.href = "/system/login/";
                        });
                    }
                }
            });
        }

    });
};


// 添加用户
Auth.prototype.addUserEvent = function () {
    var usernameInput = $("#add-username");
    var passwordInput = $("#add-password");
    var passwordConfirm = $("#add-password-confirm");
    var userDescInput = $("#add-user-desc");
    $("#add-user-btn").click(function () {
        // 初始化
        usernameInput.val('');
        passwordInput.val('');
        passwordConfirm.val('');
        userDescInput.val('');
        // 弹框
        layer.open({
            type: 1,
            title: '添加用户',
            closeBtn: 1, //显示关闭按钮
            anim: 2,
            area: ['800px', '400px'],
            shadeClose: true, //开启遮罩关闭
            content: $("#add-user-tan")
        });
    });

    $("#add-user-submit").click(function () {
        // 获取表单参数
        var username = usernameInput.val();
        var pwd1 = passwordInput.val();
        var pwd2 = passwordConfirm.val();
        var userDesc = userDescInput.val();
        var is_activation = $(".add-user-enable");
        var not_activation = $(".add-user-disable");
        var userType = $("#add-user-select-type").val();
        var user_type = 0;
        var activation = 0;

        // 表单验证
        if (!username) {
            layer.msg('请输入用户名', {icon: 2});
            return null;
        } else if (!pwd1 || !pwd2) {
            layer.msg('请输入密码', {icon: 2});
            return null;
        } else if (pwd1.length < 8 || pwd2.length < 8) {
            layer.msg('密码长度不能小于8个字符', {icon: 2});
            return null;
        } else if (!(pwd2 === pwd1)) {
            layer.msg('两次输入密码不一致', {icon: 2});
            return null;
        } else {
            // 参数处理
            if (is_activation.prop("checked")) {
                activation = 1;
            }
            if (not_activation.prop("checked")) {
                activation = 0;
            }

            if (userType === '2') {
                user_type = 1;
            } else if (userType === '3') {
                user_type = 0;
            }
            layer.closeAll();
            // ajax提交数据
            stockajax.post({
                'url': '/system/sysuser/',
                'data': {
                    'username': username,
                    'pwd1': pwd1,
                    'pwd2': pwd2,
                    'desc': userDesc,
                    'user_type': user_type,
                    'activation': activation
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.closeAll();
                        layer.msg('添加用户成功!', {icon: 1, time: 1000}, function () {
                            window.location = window.location.href;
                        });
                    }
                },
                'fail': function () {
                    layer.msg('添加用户失败!', {icon: 1, time: 1000});
                }
            });
        }

    });
};


// 编辑用户
Auth.prototype.editUserEvent = function () {
    // var self = this;
    var editUsernameInput = $("#edit-username");
    var editDescInput = $("#edit-desc");
    var editUserTypeInput = $("#edit-user-select-type");
    var editUserEnableInput = $(".edit-user-enable");
    var editUserDisableInput = $(".edit-user-disable");
    var prt;

    $(".edit-user-btn").click(function () {
        // var user_id = $(this).attr("data-user-id");
        prt = $(this).parent('td.brand-manage');
        editUsernameInput.text(prt.prevAll('.user-name').text());
        editDescInput.val(prt.prevAll('.user-desc').text());
        var user_type = prt.prevAll('.user-type').attr('data-is');

        if (user_type === 'True') {
            editUserTypeInput.val(2)
        } else {
            editUserTypeInput.val(3)
        }
        layer.open({
            type: 1,
            title: '编辑',
            closeBtn: 1, //显示关闭按钮
            anim: 2,
            area: ['800px', '400px'],
            shadeClose: true, //开启遮罩关闭
            content: $("#add-user-tan-edit")
        });
    });

    $("#edit-user-submit").click(function () {
        var user_id = prt.prevAll('.user-id').text();
        var userDesc = editDescInput.val();
        var userType = editUserTypeInput.val();
        var user_type = 0;
        var activation = 0;

        // 参数处理
        if (editUserEnableInput.prop("checked")) {
            activation = 1;
        }
        if (editUserDisableInput.prop("checked")) {
            activation = 0;
        }

        if (userType === '2') {
            user_type = 1;
        } else if (userType === '3') {
            user_type = 0;
        }

        layer.closeAll();
        // ajax提交数据
        stockajax.put({
            'url': '/system/sysuser/',
            'data': {
                'user_id': user_id,
                'desc': userDesc,
                'user_type': user_type,
                'activation': activation
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.closeAll();
                    layer.msg('编辑成功!', {icon: 1, time: 1000}, function () {
                        window.location = window.location.href;
                    });
                }
            },
            'fail': function () {
                layer.msg('编辑失败!', {icon: 1, time: 1000});
            }
        });
    });
};


// 修改密码  changeallpwd/
Auth.prototype.passwordEditEvent = function () {
    // var self = this;
    var user_id;
    var prt;

    $(".pwd-user-btn").click(function () {
        var pwdBtn = $(this);
        prt = pwdBtn.parent('td.brand-manage');
        user_id = pwdBtn.attr("data-user-id");
        $("#change-pwd-username").html(prt.prevAll('.user-name').text());

        layer.open({ // 弹窗
            type: 1,
            title: '修改密码',
            closeBtn: 1, //显示关闭按钮
            anim: 2,
            area: ['800px', '400px'],
            shadeClose: true, //开启遮罩关闭
            content: $("#add-user-tan-pwd")
        });
    });

    $("#pwd-user-submit").click(function () {
        layer.closeAll();
        var pwd1 = $("#change-pwd-password").val();
        var pwd2 = $("#change-pwd-password_confirm").val();
        if (pwd1 === pwd2) {
            // ajax提交数据
            stockajax.post({
                'url': '/system/changeallpwd/',
                'data': {
                    'user_id': user_id,
                    'newpwd1': pwd1,
                    'newpwd2': pwd2
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.msg('密码修改成功!', {icon: 1, time: 1000}, function () {
                            window.location = window.location.href;
                        });
                    }
                },
                'fail': function () {
                    layer.msg('密码修改失败!', {icon: 1, time: 1000});
                }
            });
        } else {
            layer.msg('两次输入的密码不一致', {icon: 1, time: 1000});
        }
    });
};


// 删除用户
Auth.prototype.delUserEditEvent = function () {
    $(".del-user-btn").click(function () {
        var user_id = $(this).attr("data-user-id");

        layer.confirm('确定要删除？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            layer.closeAll();
            stockajax.delete({
                'url': '/system/sysuser/',
                'data': {
                    'user_id': user_id
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.msg('删除成功!', {icon: 1, time: 1000}, function () {
                            window.location = window.location.href;
                        });
                    }
                }
            });

        }, function () { // 第二个按钮事件回调
            layer.closeAll();
        });
    });
};

// main方法
Auth.prototype.run = function () {
    this.generateImageCode();
    this.listCaptchaUpdate();
    this.listenSignupEvent();
    this.updatePasswordEvent();
    this.addUserEvent();
    this.editUserEvent();
    this.passwordEditEvent();
    this.delUserEditEvent();
};


$(function () {
    var auth = new Auth();
    auth.run();
});