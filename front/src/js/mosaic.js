// 会员资产
function MosaicAssets() {
    this.tabAssets = $(".tab-assets");
    this.tabAssets.find("li").first().addClass('cut');
    this.category = this.tabAssets.find("li").first().attr('data-id');
    this.username = '';

}

// 删除所有数据
MosaicAssets.prototype.deleteAssetsEvent = function () {
    var self = this;
    var delBtn = $("#assets-btnDel");
    delBtn.unbind('click');

    delBtn.bind('click', function () {
        layer.confirm('确定要删除所有用户资产？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (self.category) {
                layer.msg('正在删除.....', {icon: 16, time: 100000000});
                stockajax.delete({
                    'url': '/mosaic/assets/',
                    'data': {
                        'category': self.category
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            layer.closeAll();
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

// 导出数据
MosaicAssets.prototype.ouputDateEvent = function () {
    var self = this;
    $("#assets-btnExport").click(function () {
        window.open('/mosaic/memberassetcsv/?category=' + self.category);
    });
};

// 分类按钮
MosaicAssets.prototype.listenCategoryEvent = function () {
    var self = this;
    var tabAssetsLi = $(".tab-assets li");
    tabAssetsLi.unbind('click');

    tabAssetsLi.bind('click', function () {
        var cut_li = $(this);
        cut_li.addClass('cut').siblings().removeClass('cut');
        self.category = parseInt(cut_li.attr("data-id"));
        // console.log(self.category);
        stockajax.get({
            'url': '/mosaic/assetslist/',
            'data': {
                'category': self.category
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("asset-item", {"data": data['data']});
                    var tab = $('.asset-tbody');
                    tab.empty();
                    tab.append(tpl);

                    // 分页按钮
                    var page_data = data["pages_parm"];
                    var p_tpl = template("page-item", page_data);
                    var page_ul = $("#assets-page-box");
                    page_ul.empty();
                    page_ul.append(p_tpl);
                    $("#assets-total_count").text(data['count']);
                    self.listenPageEvent();
                }
            }
        });
    });
};


// 分页按钮
MosaicAssets.prototype.listenPageEvent = function () {
    var self = this;
    var pageBtn = $(".page-btn");
    pageBtn.unbind('click')
    pageBtn.bind('click', function () {
        var page = $(this).attr("data-p");
        if (page) {
            stockajax.get({
                'url': '/mosaic/assetslist/',
                'data': {
                    'category': self.category,
                    'p': page,
                    'username': self.username
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        var data = result['data'];
                        var tpl = template("asset-item", {"data": data['data']});
                        var tab = $('.asset-tbody');
                        tab.empty();
                        tab.append(tpl);

                        // 分页按钮
                        var page_data = data["pages_parm"];
                        var p_tpl = template("page-item", page_data);
                        var page_ul = $("#assets-page-box");
                        page_ul.empty();
                        page_ul.append(p_tpl);
                        $("#assets-total_count").text(data['count']);
                        self.listenPageEvent();
                    }
                }
            });
        }
    });
};


// 搜索
MosaicAssets.prototype.sourchBtnEvent = function () {
    var self = this;

    $("#assets-btnQuery").click(function () {
        self.username = $("#assets_user_name").val();
        if (self.username) {
            stockajax.get({
                'url': '/mosaic/assetslist/',
                'data': {
                    'category': self.category,
                    'username': self.username
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        var data = result['data'];
                        var tpl = template("asset-item", {"data": data['data']});
                        var tab = $('.asset-tbody');
                        tab.empty();
                        tab.append(tpl);
                        // 分页按钮
                        var page_data = data["pages_parm"];
                        var p_tpl = template("page-item", page_data);
                        var page_ul = $("#assets-page-box");
                        page_ul.empty();
                        page_ul.append(p_tpl);
                        $("#assets-total_count").text(data['count']);
                        self.listenPageEvent();
                    }
                }
            });
        } else {
            layer.msg("请输入用户名", {icon: 2, time: 1000});
            return null;
        }
    });
};


MosaicAssets.prototype.run = function () {
    this.listenCategoryEvent();
    this.listenPageEvent();
    this.ouputDateEvent();
    this.sourchBtnEvent();
    this.deleteAssetsEvent();
};


// 买入明细
function MosaicBuyDetails() {
    this.tabBuy = $(".tab-buy");
    this.tabBuy.find("li").first().addClass('cut');
    this.category = this.tabBuy.find("li").first().attr('data-id');
    this.username = '';
    this.date = '';
}


// 分页按钮
MosaicBuyDetails.prototype.listenPageEvent = function () {
    var self = this;
    var pageBtn = $(".page-btn");
    pageBtn.unbind('click');

    pageBtn.bind('click', function () {
        var page = $(this).attr("data-p");
        if (page) {
            stockajax.get({
                'url': '/mosaic/buydtllist/',
                'data': {
                    'category': self.category,
                    'p': page,
                    'user': self.username,
                    'date': self.date
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        var data = result['data'];
                        var tpl = template("buy-item", {"data": data['data']});
                        var tab = $('.buy-tbody');
                        tab.empty();
                        tab.append(tpl);
                        // 分页按钮
                        var page_data = data["pages_parm"];
                        var p_tpl = template("page-item", page_data);
                        var page_ul = $("#buy-page-box");
                        page_ul.empty();
                        page_ul.append(p_tpl);
                        $("#buy-total_count").text(data['count']);
                        self.listenPageEvent();
                    }
                }
            });
        }
    });
};


// 分类按钮
MosaicBuyDetails.prototype.listenCategoryEvent = function () {
    var self = this;
    var tabBuyLi = $(".tab-buy li");

    tabBuyLi.unbind('click');

    tabBuyLi.bind('click', function () {
        var cut_li = $(this);
        cut_li.addClass('cut').siblings().removeClass('cut');
        self.category = parseInt(cut_li.attr("data-id"));

        stockajax.get({
            'url': '/mosaic/buydtllist/',
            'data': {
                'category': self.category
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("buy-item", {"data": data['data']});
                    var tab = $('.buy-tbody');
                    tab.empty();
                    tab.append(tpl);

                    // 分页按钮
                    var page_data = data["pages_parm"];
                    var p_tpl = template("page-item", page_data);
                    var page_ul = $("#buy-page-box");
                    page_ul.empty();
                    page_ul.append(p_tpl);
                    $("#buy-total_count").text(data['count']);
                    self.listenPageEvent();
                }
            }
        });
    });
};


// 搜索
MosaicBuyDetails.prototype.searchBtnEvent = function () {
    var self = this;
    $("#buy-btnQuery").click(function () {
        self.username = $("#buy_user_name").val();
        self.date = $("#buy_add_time").val();

        stockajax.get({
            'url': '/mosaic/buydtllist/',
            'data': {
                'category': self.category,
                'date': self.date,
                'user': self.username
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("buy-item", {"data": data['data']});
                    var tab = $('.buy-tbody');
                    tab.empty();
                    tab.append(tpl);

                    // 分页按钮
                    var page_data = data["pages_parm"];
                    var p_tpl = template("page-item", page_data);
                    var page_ul = $("#buy-page-box");
                    page_ul.empty();
                    page_ul.append(p_tpl);
                    $("#buy-total_count").text(data['count']);
                    self.listenPageEvent();
                }
            }
        });
    });
};

// 删除所有会员买入明细
MosaicBuyDetails.prototype.deleteBuyBtnEvent = function () {
    var self = this;

    var buyDelBtn = $("#buy-btnDel");
    buyDelBtn.unbind('click');

    buyDelBtn.bind('click', function () {
        layer.confirm('确定要删除所有会员买入明细数据？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (self.category) {
                layer.msg('正在删除.....', {icon: 16, time: 100000000});
                stockajax.delete({
                    'url': '/mosaic/buydtl/',
                    'data': {
                        'category': self.category
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            layer.closeAll();
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


MosaicBuyDetails.prototype.run = function () {
    this.deleteBuyBtnEvent();
    this.listenCategoryEvent();
    this.listenPageEvent();
    this.searchBtnEvent();
};

// 卖出明细
function MosaicSellDetails() {
    this.tabSell = $(".tab-sell");
    this.tabSell.find("li").first().addClass('cut');
    this.category = this.tabSell.find("li").first().attr('data-id');
    this.username = '';
    this.date = '';
}

// 分页按钮
MosaicSellDetails.prototype.listenPageEvent = function () {
    var self = this;
    var pageBtn = $(".page-btn");
    pageBtn.unbind('click')
    pageBtn.bind('click', function () {
        var page = $(this).attr("data-p");
        if (page) {
            stockajax.get({
                'url': '/mosaic/selldtllist/',
                'data': {
                    'category': self.category,
                    'p': page,
                    'username': self.username
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        var data = result['data'];
                        var tpl = template("sell-item", {"data": data['data']});
                        var tab = $('.sell-tbody');
                        tab.empty();
                        tab.append(tpl);
                        // 分页按钮
                        var page_data = data["pages_parm"];
                        var p_tpl = template("page-item", page_data);
                        var page_ul = $("#sell-page-box");
                        page_ul.empty();
                        page_ul.append(p_tpl);
                        $("#sell-total_count").text(data['count']);
                        self.listenPageEvent();
                    }
                }
            });
        }
    });
};

// 分类按钮
MosaicSellDetails.prototype.listenCategoryEvent = function () {
    var self = this;
    var tabSellLi = $(".tab-sell li");
    tabSellLi.unbind('click');
    tabSellLi.bind('click', function () {
        var cut_li = $(this);
        cut_li.addClass('cut').siblings().removeClass('cut');
        self.category = parseInt(cut_li.attr("data-id"));
        stockajax.get({
            'url': '/mosaic/selldtllist/',
            'data': {
                'category': self.category
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("sell-item", {"data": data['data']});
                    var tab = $('.sell-tbody');
                    tab.empty();
                    tab.append(tpl);
                    // 分页按钮
                    var page_data = data["pages_parm"];
                    var p_tpl = template("page-item", page_data);
                    var page_ul = $("#sell-page-box");
                    page_ul.empty();
                    page_ul.append(p_tpl);
                    $("#sell-total_count").text(data['count']);
                    self.listenPageEvent();
                }
            }
        });
    });
};

// 搜索
MosaicSellDetails.prototype.searchBtnEvent = function () {
    var self = this;

    $("#sell-btnQuery").click(function () {
        self.username = $("#sell-user_name").val();
        self.date = $("#sell-add_time").val();
        console.log(self.username, self.date, self.category);
        stockajax.get({
            'url': '/mosaic/selldtllist/',
            'data': {
                'category': self.category,
                'date': self.date,
                'user': self.username
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("sell-item", {"data": data['data']});
                    var tab = $('.sell-tbody');
                    tab.empty();
                    tab.append(tpl);

                    // 分页按钮
                    var page_data = data["pages_parm"];
                    var p_tpl = template("page-item", page_data);
                    var page_ul = $("#sell-page-box");
                    page_ul.empty();
                    page_ul.append(p_tpl);
                    $("#sell-total_count").text(data['count']);
                    self.listenPageEvent();
                }
            }
        });
    });
};


// 删除所有会员卖出明细
MosaicSellDetails.prototype.deleteSellBtnEvent = function () {
    var self = this;
    var sellDelBtn = $("#sell-btnDel");
    sellDelBtn.unbind('click');
    sellDelBtn.bind('click', function () {
        layer.confirm('确定要删除所有会员卖出明细数据？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (self.category) {
                layer.msg('正在删除.....', {icon: 16, time: 100000000});
                stockajax.delete({
                    'url': '/mosaic/selldtl/',
                    'data': {
                        'category': self.category
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            layer.closeAll();
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

MosaicSellDetails.prototype.run = function () {
    this.deleteSellBtnEvent();
    this.listenCategoryEvent();
    this.listenPageEvent();
    this.searchBtnEvent();
};


// 彩金
function MosaicLotteryReceiptDetails() {
    this.tabLotteryReceiptDetails = $(".tab-lrd");
    this.tabLotteryReceiptDetails.find("li").first().addClass('cut');
    this.category = this.tabLotteryReceiptDetails.find("li").first().attr('data-id');
    this.username = '';
    this.start_time = '';
    this.end_time = '';
}

// 导出数据
MosaicLotteryReceiptDetails.prototype.ouputDateEvent = function () {
    var self = this;

    $("#lrd-btnExport").click(function () {
        var start_time = $("#ipt_start_time").val();
        var end_time = $("#ipt_end_time").val();

        if (!start_time || !end_time) {
            layer.msg("请选择时间", {icon: 2, time: 1000});
        } else {
            window.open("/mosaic/lotteryreceiptcsv/?category=" + self.category + '&start_time=' + start_time + '&end_time=' + end_time);
        }
    });
};

// 派彩
MosaicLotteryReceiptDetails.prototype.payoutEvent = function () {
    var self = this;
    var payoutBtn = $(".payout-btn");
    payoutBtn.unbind('click');
    payoutBtn.bind('click', function () {
        var prt = $(this).parent('td.td-manage');
        var receiptId = prt.prevAll('.receipt-id').attr('data-receipt-id');
        var is_send = prt.prevAll('.td-status').attr("data-is_send");
        if(is_send === 'True') {
            layer.msg("已经派彩", {icon: 3, time: 2000});
            return null;
        }

        layer.confirm('确定要派彩吗？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (receiptId) {
                stockajax.put({
                    'url': '/mosaic/receiptdtl/',
                    'data': {
                        'receipt_id': receiptId
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            layer.msg("派彩成功", {icon: 1, time: 1000}, function () {
                                window.location = window.location.href;
                            });
                        }
                    }
                });
            } else {
                layer.msg("派彩失败, 请刷新数据重试", {icon: 2, time: 1000}, function () {
                    layer.closeAll();
                });
            }
        }, function () { // 第二个按钮事件回调
            layer.closeAll(); // 关闭对话框
        });
    })
};


// 删除所有用户彩金领取明细数据
MosaicLotteryReceiptDetails.prototype.deleteLrdBtnEvent = function () {
    var self = this;

    var LrdDelBtn = $("#lrd-btnDel");
    LrdDelBtn.unbind('click');

    LrdDelBtn.bind('click', function () {
        layer.confirm('确定要删除所有用户彩金领取明细数据？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (self.category) {
                layer.msg('正在删除.....', {icon: 16, time: 100000000});
                stockajax.delete({
                    'url': '/mosaic/receiptdtl/',
                    'data': {
                        'category': self.category
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            layer.closeAll();
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


// 分页按钮
MosaicLotteryReceiptDetails.prototype.listenPageEvent = function () {
    var self = this;
    var pageBtn = $(".page-btn");

    pageBtn.unbind('click');

    pageBtn.bind('click', function () {
        var page = $(this).attr("data-p");
        if (page) {
            stockajax.get({
                'url': '/mosaic/receiptdtllist/',
                'data': {
                    'category': self.category,
                    'p': page,
                    'start_time': self.start_time,
                    'end_time': self.end_time,
                    'user': self.username
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        var data = result['data'];
                        var tpl = template("lrd-item", {"data": data['data']});
                        var tab = $('.lrd-tbody');
                        tab.empty();
                        tab.append(tpl);
                        // 分页按钮
                        var page_data = data["pages_parm"];
                        var p_tpl = template("page-item", page_data);
                        var page_ul = $("#lrd-page-box");
                        page_ul.empty();
                        page_ul.append(p_tpl);
                        $("#lrd-total_count").text(data['count']);
                        self.listenPageEvent();
                        self.payoutEvent();
                    }
                }
            });
        }
    });
};

// 分类按钮
MosaicLotteryReceiptDetails.prototype.listenCategoryEvent = function () {
    var self = this;
    var tabLrdLi = $(".tab-lrd li");
    tabLrdLi.unbind('click');
    tabLrdLi.bind('click', function () {
        var cut_li = $(this);
        cut_li.addClass('cut').siblings().removeClass('cut');
        self.category = parseInt(cut_li.attr("data-id"));
        stockajax.get({
            'url': '/mosaic/receiptdtllist/',
            'data': {
                'category': self.category
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("lrd-item", {"data": data['data']});
                    var tab = $('.lrd-tbody');
                    tab.empty();
                    tab.append(tpl);
                    // 分页按钮
                    var page_data = data["pages_parm"];
                    var p_tpl = template("page-item", page_data);
                    var page_ul = $("#lrd-page-box");
                    page_ul.empty();
                    page_ul.append(p_tpl);
                    $("#lrd-total_count").text(data['count']);
                    self.listenPageEvent();
                }
            }
        });
    });
};

// 搜索
MosaicLotteryReceiptDetails.prototype.searchBtnEvent = function () {
    var self = this;

    $("#lrd-btnQuery").click(function () {
        self.username = $("#lrd-user_name").val();
        self.start_time = $("#lrd-start_time").val();
        self.end_time = $("#lrd-end_time").val();

        stockajax.get({
            'url': '/mosaic/receiptdtllist/',
            'data': {
                'category': self.category,
                'start_time': self.start_time,
                'end_time': self.end_time,
                'user': self.username
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("lrd-item", {"data": data['data']});
                    var tab = $('.lrd-tbody');
                    tab.empty();
                    tab.append(tpl);

                    // 分页按钮
                    var page_data = data["pages_parm"];
                    var p_tpl = template("page-item", page_data);
                    var page_ul = $("#lrd-page-box");
                    page_ul.empty();
                    page_ul.append(p_tpl);
                    $("#lrd-total_count").text(data['count']);
                    self.listenPageEvent();
                    self.payoutEvent();
                }
            }
        });
    });
};


MosaicLotteryReceiptDetails.prototype.run = function () {
    this.ouputDateEvent();
    this.payoutEvent();
    this.deleteLrdBtnEvent();
    this.listenPageEvent();
    this.searchBtnEvent();
    this.listenCategoryEvent();

};
