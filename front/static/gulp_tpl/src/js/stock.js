function Stock() {
    this.isWeihu = $("#is_weihu");
}


// 个人股价增益编辑
Stock.prototype.editGainEvent = function () {
    var validBetInput = $("#edit-valid_bet");
    var gradeOneInput = $("#edit-grade_one");
    var gradeTwoInput = $("#edit-grade_two");
    var gradeThreeInput = $("#edit-grade_three");
    var gradeFourInput = $("#edit-grade_four");
    var gradeFiveInput = $("#edit-grade_five");
    var prt;

    // 弹窗
    $(".edit-gain-btn").click(function () {
        prt = $(this).parent('td.brand-manage');
        // 初始化表单数据
        validBetInput.val(prt.prevAll('.gain-valid-bet').text());
        gradeOneInput.val(prt.prevAll('.gain-grade-one').text());
        gradeTwoInput.val(prt.prevAll('.gain-grade-two').text());
        gradeThreeInput.val(prt.prevAll('.gain-grade-three').text());
        gradeFourInput.val(prt.prevAll('.gain-grade-four').text());
        gradeFiveInput.val(prt.prevAll('.gain-grade-five').text());
        layer.open({
            type: 1,
            title: '个人股价增益编辑',
            //skin: 'layui-layer-demo', //样式类名
            closeBtn: 1, //显示关闭按钮
            anim: 2,
            area: ['800px', '400px'],
            shadeClose: true, //开启遮罩关闭
            content: $("#edit-gain-tan")
        });
    });

    $("#edit-gain-submit-btn").click(function () {
        // 获取表单数据
        var validBet = validBetInput.val();
        var gradeOne = gradeOneInput.val();
        var gradeTwo = gradeTwoInput.val();
        var gradeThree = gradeThreeInput.val();
        var gradeFour = gradeFourInput.val();
        var gradeFive = gradeFiveInput.val();
        var gain_id = prt.prevAll('.gain-id').text();

        // 表单验证
        if (!validBet || !gradeOne || !gradeTwo || !gradeThree || !gradeFour) {
            layer.msg("值不能为空", {icon: 2, time: 1000});
        } else {
            stockajax.put({
                'url': '/stock/personal/',
                'data': {
                    'valid_bet': validBet,
                    'grade_one': gradeOne,
                    'grade_two': gradeTwo,
                    'grade_three': gradeThree,
                    'grade_four': gradeFour,
                    'grade_five':gradeFive,
                    'gain_id': gain_id
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.closeAll();
                        layer.msg("个人股价增益编辑成功!", {icon: 1, time: 1000}, function () {
                            window.location = window.location.href;
                        });
                    }
                }
            });
        }
    });
};


// 个人股价增益删除
Stock.prototype.deleteGainEvent = function () {
    $(".del-gain-btn").click(function () {
        var gain_id = $(this).attr('data-del');
        layer.confirm('确定要删除？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (gain_id) {
                stockajax.delete({
                    'url': '/stock/personal/',
                    'data': {
                        'gain_id': gain_id
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            layer.msg('删除成功!', {icon: 1, time: 1000}, function () {
                                window.location = window.location.href;
                            });
                        }
                    }
                });
            } else {
                layer.closeAll();
                layer.msg('删除失败!', {icon: 2, time: 1000}, function () {
                    layer.closeAll();
                });
            }
        }, function () { // 第二个按钮事件回调
            layer.closeAll(); // 关闭对话框
        });
    });
};

// 个人股价增益添加
Stock.prototype.addGainEvent = function () {
    var validBetInput = $("#valid_bet");
    var gradeOneInput = $("#grade_one");
    var gradeTwoInput = $("#grade_two");
    var gradeThreeInput = $("#grade_three");
    var gradeFourInput = $("#grade_four");
    var gradeFiveInput = $("#grade_five");
    // var prt;

    $("#add-gain-btn").click(function () {
        // 初始化表单
        validBetInput.val();
        gradeOneInput.val();
        gradeTwoInput.val();
        gradeThreeInput.val();
        gradeFourInput.val();
        gradeFiveInput.val();
        // 弹窗
        layer.open({
            type: 1,
            title: '个人股价增益添加',
            //skin: 'layui-layer-demo', //样式类名
            closeBtn: 1, //显示关闭按钮
            anim: 2,
            area: ['800px', '400px'],
            shadeClose: true, //开启遮罩关闭
            content: $("#add-gain-tan")
        });
    });

    $("#add-gain-submit-btn").click(function () {
        // 获取表单数据
        var validBet = validBetInput.val();
        var gradeOne = gradeOneInput.val();
        var gradeTwo = gradeTwoInput.val();
        var gradeThree = gradeThreeInput.val();
        var gradeFour = gradeFourInput.val();
        var gradeFive = gradeFiveInput.val();

        // 表单验证
        if (!validBet || !gradeOne || !gradeTwo || !gradeThree || !gradeFour) {
            layer.msg("值不能为空", {icon: 2, time: 1000});
        } else {
            stockajax.post({
                'url': '/stock/personal/',
                'data': {
                    'valid_bet': validBet,
                    'grade_one': gradeOne,
                    'grade_two': gradeTwo,
                    'grade_three': gradeThree,
                    'grade_four': gradeFour,
                    'grade_five': gradeFive
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.closeAll();
                        layer.msg("个人股价增益添加成功!", {icon: 1, time: 1000}, function () {
                            window.location = window.location.href;
                        });
                    }
                }
            });
        }
    });
};


// 添加官方报价
Stock.prototype.addPriceEvent = function () {
    var authPriceInput = $("#auth_price");
    var addTimeInpute = $("#add_time");

    $("#add-price").click(function () {
        // 初始化
        authPriceInput.val();
        addTimeInpute.val();
        // 弹框
        layer.open({
            type: 1,
            title: '官方股价添加',
            closeBtn: 1, //显示关闭按钮
            anim: 2,
            area: ['800px', '400px'],
            shadeClose: true, //开启遮罩关闭
            content: $("#add-price-tan")
        });
    });

    $("#add-price-submit-btn").click(function () {
        /*
        * add_time:股价日期
          price:官方股价
        * */
        var add_time = addTimeInpute.val();
        var price = authPriceInput.val();

        if (!add_time) {
            layer.msg("请选择时间", {icon: 2, time: 1000});
        } else if (!price) {
            layer.msg("请输入报价", {icon: 2, time: 1000});
        } else {
            stockajax.post({
                'url': '/stock/official/',
                'data': {
                    'add_time': add_time,
                    'price': price
                },
                'success': function (result) {
                    layer.closeAll();
                    if (result['code'] === 200) {
                        layer.msg("官方报价添加成功!", {icon: 1, time: 1000}, function () {
                            window.location = window.location.href;
                        });
                    }
                }
            });
        }
    });
};

// 编辑官方报价
Stock.prototype.editPriceEvent = function () {
    var authPriceInput = $("#edit-auth_price");
    var addTimeInpute = $("#show-add_time");
    var prt;

    $(".edit-price-btn").click(function () {
        // 初始化表单数据
        prt = $(this).parent('td.td-manage');
        addTimeInpute.text(prt.prevAll('.price-add_time').text());
        authPriceInput.val(prt.prevAll('.price-price').text());

        // 弹窗
        layer.open({
            type: 1,
            title: '官方股价编辑',
            closeBtn: 1, //显示关闭按钮
            anim: 2,
            area: ['800px', '400px'],
            shadeClose: true, //开启遮罩关闭
            content: $("#edit-price-tan")
        });
    });

    $("#edit-price-submit-btn").click(function () {
        var price = authPriceInput.val();
        if (!price) {
            layer.msg("请输入股价", {ico: 2});
        } else {
            stockajax.put({
                'url': '/stock/official/',
                'data': {
                    'price_id': prt.prevAll('.price-id').text(),
                    'price': price
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.closeAll();
                        layer.msg("官方股价编辑成功!", {icon: 1, time: 1000}, function () {
                            window.location = window.location.href;
                        });
                    }
                }
            });
        }
    });
};


// 删除官方报价
Stock.prototype.deletePriceEvent = function () {
    $(".del-price-btn").click(function () {
        var price_id = $(this).attr('data-id');
        layer.confirm('确定要删除？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (price_id) {
                stockajax.delete({
                    'url': '/stock/official/',
                    'data': {
                        'price_id': price_id
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            layer.msg('删除官方报价成功!', {icon: 1, time: 1000}, function () {
                                window.location = window.location.href;
                            });
                        }
                    }
                });
            } else {
                layer.closeAll();
                layer.msg('删除官方报价失败!', {icon: 2, time: 1000}, function () {
                    layer.closeAll();
                });
            }

        }, function () { // 第二个按钮事件回调
            layer.closeAll(); // 关闭对话框
        });
    });
};


/* 更新股票时间 */
Stock.prototype.listenSetTimeEvent = function () {
    var self = this;

    $("#btn-tf").click(function () {
        var startTime = $("#start_time").val();
        var endTime = $("#end_time").val();
        var closeDesc = $("#close_desc").val();
        var start1 = $("#start1").val();
        var end1 = $("#end1").val();
        // var start2 = $("#start2").val();
        // var end2 = $("#end2").val();
        var is_weihu = self.isWeihu.bootstrapSwitch('status');
        var weihuDesc = $("#weihu_desc").val();

        stockajax.post({
            'url': '/stock/transaction/',
            'data': {
                'start_time': startTime,
                'end_time': endTime,
                'is_maintain': is_weihu,
                'maintain_desc': weihuDesc,
                'start_a': start1,
                'end_a': end1,
                // 'start_b': start2,
                // 'end_b': end2,
                'close_desc': closeDesc
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.msg('股市时间设置成功!', {icon: 1, time: 1000}, function () {
                        window.location = window.location.href;
                    });
                }
            }
        });
    });
};


Stock.prototype.run = function () {
    this.listenSetTimeEvent();
    this.addGainEvent();
    this.deleteGainEvent();
    this.editGainEvent();
    this.addPriceEvent();
    this.deletePriceEvent();
    this.editPriceEvent();
};


$(function () {
    var stock = new Stock();
    stock.run();
});