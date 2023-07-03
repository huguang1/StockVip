function MemberImport() {
    this.filename = '';
    this.btnCalc = $("#btn_calc");
    this.btnCalc.addClass('disabled');
    this.iptAddTime = $('#ipt_add_time');
    this.categorySelect = $("#category-select");
}

// 导入数据库
MemberImport.prototype.importDatabaseEvent = function () {
    var self = this;

    self.btnCalc.click(function () {
        layer.msg('数据正在导入', {icon: 16, time: 30000});
        var ipt_time = self.iptAddTime.val();
        var category = self.categorySelect.val();

        if (ipt_time === '') {
            layer.msg('请先选择数据的导入日期!', {icon: 5, time: 1000});
            return null;
        } else {
            stockajax.post({
                'url': '/member/import/',
                'data': {
                    'ipt_time': ipt_time,
                    'filename': self.filename,
                    'category': category
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.closeAll();
                        layer.msg('数据导入成功!', {icon: 1, time: 1000}, function () {
                            window.location.href = "/member/info/";
                        });
                    }
                }
            });
        }
    });

};


// 上传文件
MemberImport.prototype.uploadFileEvent = function () {
    var self = this;
    var imageInput = $("#fileupload");

    function progressHandle(evn) {
        var loaded = evn.loaded;
        var total = evn.total;
        var showpro = Math.round(loaded / total * 100) + "%";
        $("#sr-only").css({'width': showpro});
        $(".percent").html(showpro);
    }

    imageInput.change(function () {
        if (self.iptAddTime.val() === '') {
            layer.msg('请先选择数据的导入日期!', {icon: 5, time: 1000});
            return false;
        }
        if (self.categorySelect.val() === '') {
            layer.msg('请先选择数据的导入类型!', {icon: 5, time: 1000});
            return false;
        }

        var file = this.files[0];
        var fileExtension = file.name.split('.').pop().toLowerCase();

        if (fileExtension === 'xls' || fileExtension === 'xlsx') {
            var formData = new FormData();
            formData.append("file", file);
            stockajax.post({
                'url': '/member/upload_file/',
                'data': formData,
                'processData': false,
                'contentType': false,
                'xhr': function () {
                    var progXHR = $.ajaxSettings.xhr();
                    if (progXHR.upload) {
                        progXHR.upload.addEventListener("progress", progressHandle, false);
                    }
                    return progXHR;
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        self.filename = result['data']['name'];
                        $("#result").text('上传成功');
                        self.btnCalc.removeClass('disabled');
                    }
                }
            });
        } else {
            layer.msg("必须是excel文件，后缀名为xls或者xlsx", {icon: 2, time: 1000}, function () {
                window.location.reload();
            });
        }

    });
};

MemberImport.prototype.run = function () {
    this.importDatabaseEvent();
    this.uploadFileEvent();
};


function MemberUpdate() {

}


// 打码更新
MemberUpdate.prototype.updateMember = function () {
    $(".update-member-data-btn").click(function () {
        var prt = $(this).parent('td.td-manage');
        var updateId = prt.prevAll('.update-id').text();
        var memberDate = prt.prevAll('.update-member_date').attr('data-date');
        var isUpdate = prt.prevAll('.td-status').attr('data-is-member');

        if (isUpdate === "True") {
            return null;
        }

        layer.confirm('确定要更新？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (updateId && memberDate && isUpdate === "False") {
                layer.msg('正在更新.....', {icon: 16, time: 100000000});
                stockajax.post({
                    'url': '/member/update/',
                    'data': {
                        'update_id': updateId,
                        'date': memberDate
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            layer.closeAll();
                            layer.msg('更新成功!', {icon: 1, time: 1000}, function () {
                                window.location = window.location.href;
                            });
                        }
                    }
                });
            } else {
                layer.closeAll();
                layer.msg('更新失败!', {icon: 2, time: 1000}, function () {
                    layer.closeAll();
                });
            }
        }, function () { // 第二个按钮事件回调
            layer.closeAll(); // 关闭对话框
        });
    });
};


// 删除本日数据
MemberUpdate.prototype.deleteMemberData = function () {
    $(".del-member-data-btn").click(function () {
        var prt = $(this).parent('td.td-manage');
        var updateId = prt.prevAll('.update-id').text();
        var memberDate = prt.prevAll('.update-member_date').attr('data-date');
        var updateCategory = prt.prevAll('.update-category').attr('data-category');

        layer.confirm('确定要删除？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (updateId && memberDate) {
                stockajax.delete({
                    'url': '/member/update/',
                    'data': {
                        'update_id': updateId,
                        'date': memberDate,
                        'update_category': updateCategory
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


MemberUpdate.prototype.run = function () {
    this.updateMember();
    this.deleteMemberData();
};

function MemberInfo() {
    this.queryDate = '';
    this.queryUser = '';
}


// 添加打码信息
MemberInfo.prototype.addMembeInfoEvent = function () {
    var infoCategoryInput = $("#info-category-select");
    var infoUserInput = $("#info-user");
    var infoAmountInput = $("#info-amount");
    var infoAddTimeInput = $("#info-add_time");

    $("#membe-info-btnAdd").click(function () {
        // 初始化表单
        infoCategoryInput.val();
        infoUserInput.val();
        infoAmountInput.val();
        infoAddTimeInput.val();

        // 弹窗
        layer.open({
            type: 1,
            title: '添加打码信息',
            closeBtn: 1, //显示关闭按钮
            anim: 2,
            area: ['800px', '400px'],
            shadeClose: true, //开启遮罩关闭
            content: $("#add-info-tan")
        });
    });

    $("#add-info-submit-btn").click(function () {
        var infoCategory = infoCategoryInput.val();
        var infoUser = infoUserInput.val();
        var infoAmount = infoAmountInput.val();
        var infoAddTime = infoAddTimeInput.val();

        if (infoAmount && infoUser && infoCategory && infoAddTime) {
            layer.closeAll();
            stockajax.post({
                'url': '/member/info/',
                'data': {
                    'category': infoCategory,
                    'username': infoUser,
                    'amount': infoAmount,
                    'add_date': infoAddTime
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.msg("添加打码信息成功", {icon: 1, time: 1000}, function () {
                            window.location = window.location.href;
                        });
                    }
                }
            });
        } else {
            layer.msg("请正确填写打码信息", {icon: 2, time: 1000});
        }
    });

};

// 查询
MemberInfo.prototype.inquireBtnEvent = function () {
    var self = this;

    $("#info-btnQuery").click(function () {
        self.queryDate = $("#ipt_add_time").val();
        self.queryUser = $("#info-user_name").val();
        stockajax.get({
            'url': '/member/infolist/',
            'data': {
                'username': self.queryUser,
                'date': self.queryDate
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("info-item", {"data": data['data']});
                    var tab = $('.info-tbody');
                    tab.empty();
                    tab.append(tpl);
                    // 分页按钮
                    var page_data = data["pages_parm"];
                    var p_tpl = template("page-item", page_data);
                    var page_ul = $("#infos-page-box");
                    page_ul.empty();
                    page_ul.append(p_tpl);

                    $("#info-total_count").html(data['count']);
                    self.listenPageEvent();
                }
            }
        });
    });
};

// 导出数据
MemberInfo.prototype.downMembeInfoEvent = function () {
    $("#btnExport").click(function () {
        var date = $("#ipt_add_time").val();
        if (!date) {
            layer.msg("请选择时间", {icon: 2, time: 1000});
        } else {
            window.open("/member/downinfo/?date=" + date);
        }
    });
};

// 分页按钮
MemberInfo.prototype.listenPageEvent = function () {
    var self = this;
    var pageBtn = $(".page-btn");
    pageBtn.unbind('click');
    pageBtn.bind('click',function () {
        var page = $(this).attr("data-p");
        if (page) {
            console.log(self.queryUser, self.queryDate);
            stockajax.get({
                'url': '/member/infolist/',
                'data': {
                    'username': self.queryUser,
                    'date': self.queryDate,
                    'p': page
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        var data = result['data'];
                        var tpl = template("info-item", {"data": data['data']});
                        var tab = $('.info-tbody');
                        tab.empty();
                        tab.append(tpl);
                        // 分页按钮
                        var page_data = data["pages_parm"];
                        var p_tpl = template("page-item", page_data);
                        var page_ul = $("#infos-page-box");
                        page_ul.empty();
                        page_ul.append(p_tpl);

                        $("#info-total_count").html(data['count']);
                        self.listenPageEvent();
                    }
                }
            });
        }
    });
};


MemberInfo.prototype.run = function () {
    this.addMembeInfoEvent();
    this.downMembeInfoEvent();
    this.inquireBtnEvent();
    this.listenPageEvent();
};

