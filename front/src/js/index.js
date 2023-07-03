function Stock() {
    //  userinfo_area taba
    this.category_a = $(".tab_hda").find("li").first().attr('data-category');
    // tab_hd
    this.category_b = $(".tab_hd").find("li").first().attr('data-category');

    this.username = '';
    this.sellingShares = 0;

    // 防止重复提交
    this.btnMaiRuTag = true;
    this.btnMaiChuTag = true;
    this.receiveGoldTag = true;


}

// 获取资产数据
Stock.prototype.getAssetDataEvent = function (username, category) {
    var self = this;

    stockajax.get({
        'url': '/mosaic/assetsone/',
        'data': {
            'username': username,
            'category': category
        },
        'success': function (result) {
            if (result['code'] === 200) {
                var data = result['data'];
                var total_assets = data['total_assets'];
                var residual_assets = data['residual_assets'];
                var holding_shares = data['holding_shares'];
                var buying_shares = data['buying_shares'];
                var selling_shares = data['selling_shares'];
                self.sellingShares = parseInt(selling_shares);
                var today_price = data['today_price'];
                var yesterday_price = data['yesterday_price'];
                var personal_gain = data['personal_gain'];
                var buying_count = data['sell_count'];

                // 导航栏显示用户名
                $('.username_mark').html("尊敬的: " + data['username']);
                // 总资产
                $("#user_total_bet").html(total_assets);
                $("#dz_first-total_assets").html(total_assets);
                // 剩余资产
                $("#user_valid_bet").html(residual_assets);
                $("#dz_first-residual_assets").html(residual_assets);
                // 持有股票数量
                $("#user_hold_shares").html(holding_shares);
                $("#dz_first-holding_shares").html(holding_shares);
                // 已买入
                $("#user_buy_shares").html(buying_shares);
                $("#dz_first-buying_shares").html(buying_shares);
                // 已卖出
                $("#user_sell_shares").html(Number(buying_shares) - Number(holding_shares));
                $("#dz_first-selling_shares").html(Number(buying_shares) - Number(holding_shares));

                // 可卖股份
                $("#user_free_shares").html(buying_count);
                // 今日股价
                $("#dz_first-today-price").html(today_price);
                $("#user_auth_price").html(today_price);
                // 昨日股价
                $("#dz_first-yesterday-price").html(yesterday_price);
                // 用户名
                $("#dz_first-username").html(username);
                // 个人股价增益
                $("#user_person_price").html(personal_gain);
                $("#dz_first-gain").html(personal_gain);
                // 可兑换彩金
                var exchange = (Number(personal_gain) + Number(today_price)) * Number(selling_shares);
                $("#dz_first-exchange").html(exchange);
                $("#calc_lottery").html(exchange);

                // 可卖出股份
                $("#dz_first-can_sold").html(buying_count);
                $("#sell_shares").val(buying_count);

                // 可买入股票数量
                $("#buy_shares").val(parseInt(Number(residual_assets) / 10000));
            }
        }
    });
};


// tab按钮事件
Stock.prototype.tabUserEvent = function () {
    var self = this;
    $(".tab_hda").children().click(function () {
        $(this).addClass('on').siblings().removeClass('on');
        self.category_a = $(this).attr('data-category');
        self.getAssetDataEvent(self.username, self.category_a);
    });
};


// 判断是否登录
Stock.prototype.checkLoginEvent = function () {
    var self = this;
    stockajax.get({
        'url': '/login/',
        'data': {
            'category': self.category_a
        },
        'success': function (result) {
            if (result['code'] === 200) {
                var touristArea = $(".tourist_area");
                var userinfoArea = $(".userinfo_area");

                if (result['data']['is_login']) {
                    touristArea.hide();
                    userinfoArea.show();
                    var username = result['data']['username'];
                    self.username = username;
                    self.tabUserEvent();
                    $(".dz_first").show();
                    $(".dz_two").show();
                    $(".dz_tip").show();
                    $(".dz_three").hide();
                    $(".tab_bda").children().eq(0).show();
                    self.getAssetDataEvent(username, self.category_a);
                    // alert("已经登录");
                } else {
                    touristArea.show();
                    userinfoArea.hide();
                    $(".dz_first").hide();
                    $(".dz_two").hide();
                    $(".dz_tip").hide();
                }
            }
        }
    });
};

// 买入股票
Stock.prototype.buyStockEvent = function () {
    var self = this;
    $("#btnMaiRu").on('click', function (e) {
        e.preventDefault();
        if (self.btnMaiRuTag) {
            self.btnMaiRuTag = false;
            var count = parseInt($("#buy_shares").val());
            var residual_assets = parseInt($("#user_valid_bet").text());

            if (residual_assets / 10000 >= count && count > 0) {
                if (count && self.category_a && self.username) {
                    stockajax.post({
                        'url': '/mosaic/buydtl/',
                        'data': {
                            'user': self.username,
                            'count': count,
                            'category': self.category_a
                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                self.btnMaiRuTag = false;
                                layer.msg("交易成功", {icon: 1, time: 1000}, function () {
                                    // loginout
                                    self.getAssetDataEvent(self.username, self.category_a);
                                });
                            }
                        }
                    });
                } else {
                    layer.msg('请输入购买数量', {icon: 2, time: 1000});
                }
            } else {
                layer.msg('资产不足', {icon: 2, time: 1000});
            }
        }
    });
};


// 卖出股票
Stock.prototype.sellStockEvent = function () {
    var self = this;
    $("#btnMaiChu").on('click', function (e) {
        e.preventDefault();
        if (self.btnMaiChuTag) {
            self.btnMaiChuTag = false;
            // 卖出数量
            var count = $("#sell_shares").val();
            // 持有数量
            var holdShares = $("#user_hold_shares").text();
            // 可卖股票数量
            var userFreeShares = parseInt($("#user_free_shares").text());

            if (parseInt(count) > parseInt(holdShares) || parseInt(count) > userFreeShares) {
                layer.msg('您当前只能卖出: ' + userFreeShares + ' 股', {icon: 2, time: 1000});
            } else {
                if (count && self.category_a && self.username && parseInt(count) !== 0) {
                    stockajax.post({
                        'url': '/mosaic/selldtl/',
                        'data': {
                            'user': self.username,
                            'count': count,
                            'category': self.category_a
                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                self.btnMaiChuTag = true;
                                layer.msg("交易成功", {icon: 1, time: 1000}, function () {
                                    self.getAssetDataEvent(self.username, self.category_a);
                                });
                            }
                        }
                    });
                } else {
                    layer.msg("请输入卖出股票的数量", {icon: 2, time: 1000});
                }
            }
        }
    });
};


// 兑换彩金
Stock.prototype.redemptionEvent = function () {
    var self = this;
    $("#receive_gold").on('click', function (e) {
        e.preventDefault();
        if (self.receiveGoldTag) {
            self.receiveGoldTag = false;
            if (self.category_a && self.username && self.sellingShares !== 0) {
                stockajax.post({
                    'url': '/mosaic/receiptdtl/',
                    'data': {
                        'user': self.username,
                        'category': self.category_a
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            layer.msg('彩金兑换成功!', {icon: 1, time: 1000}, function () {
                                self.getAssetDataEvent(self.username, self.category_a);
                            });
                        }
                    }
                });
            }
        }
    });
};

Stock.prototype.loginHandler = function () {
    var self = this;
    var username = $("#username").val();
    var code = $("#verycode").val().toLowerCase();
    var vcode = $(".yancode input").val().toLowerCase();

    if (code.length < 4 || vcode !== code || vcode.length < 4) {
        layer.msg('验证码不正确!', {icon: 2, time: 1000});
        return null;
    } else if (!username) {
        layer.msg('请输入用户名', {icon: 2, time: 1000});
        return null;
    } else {
        stockajax.post({
            'url': '/login/',
            'data': {
                'username': username,
                'category': self.category_a
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    $(".tanshow").hide();
                    $(".tourist_area").hide();
                    $(".userinfo_area").show();
                    self.username = username;
                    // self.getAssetDataEvent(username, self.category_a);
                    self.checkLoginEvent();
                    layer.msg('登录成功!', {icon: 1, time: 1000});
                }
            }
        });
    }

};

// 登录
Stock.prototype.loginEvent = function () {
    var self = this;
    $("#btnLogin").bind('click', function () {
        self.loginHandler();
    });

    $(window).keydown(function (event) {
        if (event.keyCode == "13") {
            self.loginHandler();
        }
    });
};


// 登出
Stock.prototype.logoutEvent = function () {
    $("#loginout").click(function () {
        stockajax.get({
            'url': '/logout/',
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.msg("登出成功", {icon: 1, time: 1000}, function () {
                        window.location = window.location.href;
                    });
                }
            }
        });
    });
};

// 模拟计算
Stock.prototype.simulationCalculationEvent = function () {
    $("#jisuan").click(function () {
        var total = $('#total').val();     // 截止昨日拥有总数
        var price = $('#price').val();     //官方股价
        var sell = $('#sell').val();　　　  // 卖出股票数量
        var bet = $('#bet').val();　　　　  // 昨天投注额
        // 校验空值并检验数值是否为数字
        //var r = /^[0-9]*[1-9][0-9]*$/  //正整数
        var r = /^\d+$/;  // 非负整数
        var f = /^\d+(\.\d+)?$/;    //浮点数

        if (!r.test(total) || !total) {
            layer.msg('请输入正确的截止昨日拥有股票总数', {time: 1000, icon: 0});
            return false
        }
        if (!r.test(bet) || !bet) {
            layer.msg('请输入正确的昨日投注数量', {time: 1000, icon: 0});
            return false
        }
        if (!r.test(price) && !f.test(price) || !price) {
            layer.msg('请输入正确的官方股价，如8.8', {time: 1000, icon: 0});
            return false
        }
        if (!r.test(sell) || !sell) {
            layer.msg('请输入正确的卖出股票数量', {time: 1000, icon: 0});
            return false
        }
        // 不允许输出超出 5000万的投注
        if (bet > 50000000) {
            layer.msg('请输入正确的少于5000000万的投注', {time: 1000, icon: 0});
            return false
        }
        // 卖出数量不能大于截止昨日拥有总数
        if (parseInt(sell) > parseInt(total)) {
            layer.msg('卖出数量不可大于截止昨日拥有总数', {time: 1000, icon: 0});
            return false
        }
        // 获取昨日投注的增益
        var bet_gain = '';

        if (bet === 0) {
            bet_gain = -2;
        }
        if (0 < bet <= 10000) {
            bet_gain = 0;
        }
        if (bet < 50000 && bet >= 10000) {
            bet_gain = 0.1;
        }
        if (bet < 100000 && bet >= 50000) {
            bet_gain = 0.5;
        }
        if (bet < 500000 && bet >= 100000) {
            bet_gain = 0.8;
        }
        if (bet < 1000000 && bet >= 500000) {
            bet_gain = 1;
        }
        if (bet < 5000000 && bet >= 1000000) {
            bet_gain = 1.2;
        }
        if (bet < 10000000 && bet >= 5000000) {
            bet_gain = 1.3;
        }
        if (bet < 50000000 && bet >= 10000000) {
            bet_gain = 2;
        }
        if (bet >= 50000000) {
            bet_gain = 5;
        }
        // 计算
        var a = parseInt(sell) * (parseInt(bet_gain) + parseInt(price));  // 10*(10-2)
        $('#lottery').val(a)
    });
};

// 获取在线人数
Stock.prototype.getOnlineUsers = function () {
    stockajax.get({
        'url': '/mosaic/count/',
        'data': {
            'l': Math.ceil(Math.random() * 1000000)
        },
        'success': function (result) {
            if (result['code'] === 200) {
                var count = result['data']['online_count'];
                var str_html = "";
                if (!count) {
                    str_html = "已有<span>8</span><span>0</span><span>0</span>名客户";
                    $(".footer_vip_num").html(str_html)
                } else {
                    var str_count = count.toString().split('');
                    str_html = "已有";
                    $.each(str_count, function (i, obj) {
                        str_html += '<span>' + obj + '</span>'
                    });
                    str_html += '名客户';
                    $(".footer_vip_num").html(str_html)
                }
            }
        }
    })
};


// 更新在线人数
Stock.prototype.updateOnlineUsers = function () {
    var self = this;

    setInterval(function () {
        self.getOnlineUsers();
    }, 600000);
};


Stock.prototype.run = function () {
    this.getOnlineUsers();
    this.checkLoginEvent();
    this.loginEvent();
    this.logoutEvent();
    this.tabUserEvent();
    this.buyStockEvent();
    this.sellStockEvent();
    this.redemptionEvent();
    this.simulationCalculationEvent();
    this.updateOnlineUsers();
};


$(function () {
    var stock = new Stock();
    stock.run();
});
