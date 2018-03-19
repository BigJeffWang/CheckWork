$(function () {
  // 考勤文件上传
  $("#upload1").click(function () {
    $("#imgWait1").show();
    var formData = new FormData();
    formData.append("dir_name", "dir1");
    formData.append("upload_file", document.getElementById("file1").files[0]);
    $.ajax({
      url: "/upload",
      type: "POST",
      cache: false,
      data: formData,
      dataType:"json",
      contentType: false,
      processData: false,
      success: function (data) {
        if (data.status === "True") {
          alert("上传成功！");
        }
        if (data.status === "False") {
          alert(data.msg);
        }
        $("#imgWait1").hide();
        var dir_name = {"dir_name": "dir1"};
        refresh_list_func(dir_name);
      },
      error: function () {
        alert("上传失败！");
        $("#imgWait1").hide();
      }
    });
  });


  // 请假文件上传
  $("#upload2").click(function () {
    $("#imgWait2").show();
    var formData = new FormData();
    formData.append("dir_name", "dir2");
    formData.append("upload_file", document.getElementById("file2").files[0]);
    $.ajax({
      url: "/upload",
      type: "POST",
      cache: false,
      data: formData,
      dataType:"json",
      contentType: false,
      processData: false,
      success: function (data) {
        if (data.status === "True") {
          alert("上传成功！");
        }
        if (data.status === "False") {
          alert(data.msg);
        }
        $("#imgWait2").hide();
        var dir_name = {"dir_name": "dir2"};
        refresh_list_func(dir_name);
      },
      error: function () {
        alert("上传失败！");
        $("#imgWait2").hide();
      }
    });
  });


  // 加班文件上传
  $("#upload3").click(function () {
    $("#imgWait3").show();
    var formData = new FormData();
    formData.append("dir_name", "dir3");
    formData.append("upload_file", document.getElementById("file3").files[0]);
    $.ajax({
      url: "/upload",
      type: "POST",
      cache: false,
      data: formData,
      dataType:"json",
      contentType: false,
      processData: false,
      success: function (data) {
        if (data.status === "True") {
          alert("上传成功！");
        }
        if (data.status === "False") {
          alert(data.msg);
        }
        $("#imgWait3").hide();
        var dir_name = {"dir_name": "dir3"};
        refresh_list_func(dir_name);
      },
      error: function () {
        alert("上传失败！");
        $("#imgWait3").hide();
      }
    });
  });


  // 考勤全选
  var isCheckAll1 = false;
  $('#all1').click(function () {
    if (isCheckAll1) {
      $("#checkbox_list1").find("input:checkbox").each(function() {
          this.checked = false;
        });
        isCheckAll1 = false;
    } else {
        $("#checkbox_list1").find("input:checkbox").each(function() {
          this.checked = true;
        });
        isCheckAll1 = true;
    }
  });

  // 请假全选
  var isCheckAll2 = false;
  $('#all2').click(function () {
    if (isCheckAll2) {
        $("#checkbox_list2").find("input:checkbox").each(function() {
          this.checked = false;
        });
        isCheckAll2 = false;
    } else {
        $("#checkbox_list2").find("input:checkbox").each(function() {
          this.checked = true;
        });
        isCheckAll2 = true;
    }
  });


  // 加班全选
  var isCheckAll3 = false;
  $('#all3').click(function () {
    if (isCheckAll3) {
        $("#checkbox_list3").find("input:checkbox").each(function() {
          this.checked = false;
        });
        isCheckAll3 = false;
    } else {
        $("#checkbox_list3").find("input:checkbox").each(function() {
          this.checked = true;
        });
        isCheckAll3 = true;
    }
  });


  // 报告全选
  var isCheckAll5 = false;
  $('#all5').click(function () {
    if (isCheckAll5) {
        $("#checkbox_list5").find("input:checkbox").each(function() {
          this.checked = false;
        });
        isCheckAll5 = false;
    } else {
        $("#checkbox_list5").find("input:checkbox").each(function() {
          this.checked = true;
        });
        isCheckAll5 = true;
    }
  });


  // 员工全选
  var isCheckAll4 = false;
  $('#all4').click(function () {
    if (isCheckAll4) {
        $("#checkbox_list4").find("input:checkbox").each(function() {
          this.checked = false;
        });
        isCheckAll4 = false;
    } else {
        $("#checkbox_list4").find("input:checkbox").each(function() {
          this.checked = true;
        });
        isCheckAll4 = true;
    }
  });


  // 刷新列表
  var refresh_list_func = function(arg) {
    $.ajax({
      url: "/refreshlist",
      type: "POST",
      data: arg,
      dataType:"json",
      success: function (data) {
        var show_file_list = data["show_file_list"];
        var show_html = "";
        if (arg.dir_name === "dir4") {
          show_html += "<p>员工总计: " + data["list_len"] + "人</p>";
        }
        $.each(show_file_list, function(i, val){
          show_html += '<div class="check_file">';
          if (arg.dir_name !== "dir4"){
            if (i === 0){
              show_html += '<input type="radio" class="radio_' + arg["dir_name"] + '" name="radio_' + arg["dir_name"] + '" value="'+ val + '" checked />';
            }else{
              show_html += '<input type="radio" class="radio_' + arg["dir_name"] + '" name="radio_' + arg["dir_name"] + '" value="'+ val + '"/>';
            }
          }
          show_html += '<input type="checkbox" name="vehicle" value="' + val + '"/><span>' + val + '</span></div>';
        });
        $("#" + arg["dir_name"]).html(show_html);
        insert_checked_func();
      },
      error: function () {
        alert("上传失败！");
      }
    });
  };


  // 删除列表
  var del_list_func = function (arg) {
    var show_arg = {"dir_name": arg["dir_name"]};
    var status = confirm("确定要删除?");
    if (!status) {
      return false;
    }
    $.ajax({
      url: "/dellist",
      type: "POST",
      data: arg,
      dataType: "json",
      success: function (data) {
        if (data.status === "True") {
          alert("删除成功！");
        }
        if (data.status === "False") {
          alert(data.msg);
        }
        refresh_list_func(show_arg);
      },
      error: function () {
        alert("上传失败！");
      }
    });
  };


  // 考勤删除
  $('#del1').click(function () {
    var del_dict = {};
    del_dict['dir_name'] = "dir1";
    del_dict['del_list'] = [];
    $("#checkbox_list1").find("input:checkbox:checked").each(function() {
      del_dict['del_list'].push($(this).val());
    });
    del_dict['del_list'] = "['" + del_dict['del_list'].join("','") + "']";
    del_list_func(del_dict);
  });


  // 请假删除
  $('#del2').click(function () {
    var del_dict = {};
    del_dict['dir_name'] = "dir2";
    del_dict['del_list'] = [];
    $("#checkbox_list2").find("input:checkbox:checked").each(function() {
      del_dict['del_list'].push($(this).val());
    });
    del_dict['del_list'] = "['" + del_dict['del_list'].join("','") + "']";
    del_list_func(del_dict);
  });


  // 加班删除
  $('#del3').click(function () {
    var del_dict = {};
    del_dict['dir_name'] = "dir3";
    del_dict['del_list'] = [];
    $("#checkbox_list3").find("input:checkbox:checked").each(function() {
      del_dict['del_list'].push($(this).val());
    });
    del_dict['del_list'] = "['" + del_dict['del_list'].join("','") + "']";
    del_list_func(del_dict);
  });


  // 报告删除
  $('#del5').click(function () {
    var del_dict = {};
    del_dict['dir_name'] = "dir5";
    del_dict['del_list'] = [];
    $("#checkbox_list5").find("input:checkbox:checked").each(function() {
      del_dict['del_list'].push($(this).val());
    });
    del_dict['del_list'] = "['" + del_dict['del_list'].join("','") + "']";
    del_list_func(del_dict);
  });


  // 员工删除
  $('#del4').click(function () {
    var del_dict = {};
    del_dict['dir_name'] = "dir4";
    del_dict['del_list'] = [];
    $("#checkbox_list4").find("input:checkbox:checked").each(function() {
      del_dict['del_list'].push($(this).val());
    });
    del_dict['del_list'] = "['" + del_dict['del_list'].join("','") + "']";
    del_list_func(del_dict);
  });

  // 员工新增
  $('#add4').click(function () {
    $(".employe").show();
  });

  // 员工新增隐藏
  $('#add4_hidden').click(function () {
    $(".employe").hide();
  });

  // 员工提交
  $('#upload4').click(function () {
    var emp_id = $("input[name='emp_id']").val();
    var emp_name = $("input[name='emp_name']").val();
    var emp_dept = $("input[name='emp_dept']").val();
    var emp_email = $("input[name='emp_email']").val();
    if (emp_email === ""){
      emp_email = "xxx@licaifan.com";
    }

    $("input[name='emp_id']").val('');
    $("input[name='emp_name']").val('');
    $("input[name='emp_dept']").val('');
    $("input[name='emp_email']").val('');
    var form_data = {
      "emp_id": emp_id,
      "emp_name": emp_name,
      "emp_dept": emp_dept,
      "emp_email": emp_email,
      "dir_name": "dir4"
    };
    $.ajax({
      url: "/emp_add",
      type: "POST",
      data: form_data,
      dataType: "json",
      success: function (data) {
        if (data.status === "True") {
        }
        if (data.status === "False") {
          alert(data.msg);
        }
        refresh_list_func({"dir_name": "dir4"});
      },
      error: function () {
        alert("新增失败！");
      }
    });
  });


  // 插入生成报告所用信息
  var insert_checked_func = function() {
    var radio_check_dir1 = $('input:radio[name=radio_dir1]:checked').val();
    var radio_check_dir2 = $('input:radio[name=radio_dir2]:checked').val();
    var radio_check_dir3 = $('input:radio[name=radio_dir3]:checked').val();

    $("input:radio[name=radio_dir1]").click(function(){
      radio_check_dir1 = $('input:radio[name=radio_dir1]:checked').val();
      $("#kaoqin").val(radio_check_dir1);
    });
    $("input:radio[name=radio_dir2]").click(function(){
      radio_check_dir2 = $('input:radio[name=radio_dir2]:checked').val();
      $("#qingjia").val(radio_check_dir2);
    });
    $("input:radio[name=radio_dir3]").click(function(){
      radio_check_dir3 = $('input:radio[name=radio_dir3]:checked').val();
      $("#jiaban").val(radio_check_dir3);
    });

    $("#kaoqin").val(radio_check_dir1);
    $("#qingjia").val(radio_check_dir2);
    $("#jiaban").val(radio_check_dir3);
  };



  refresh_list_func({"dir_name": "dir1"});
  refresh_list_func({"dir_name": "dir2"});
  refresh_list_func({"dir_name": "dir3"});
  refresh_list_func({"dir_name": "dir4"});
  refresh_list_func({"dir_name": "dir5"});


  var get_selected_day = function() {
    var selectYear = document.querySelector('.sc-select-year').value;
    var selectMonth = document.querySelector('.sc-select-month').value;
    var days = document.querySelectorAll('.sc-selected');

    var year_val = selectYear.valueOf();
    var month_val = selectMonth.valueOf();
    var work_days = [];

    days.forEach(function (v, i) {
      var tmp_day = v.querySelector('.day').innerHTML;
      work_days.push(year_val + "-" + month_val + "-" + tmp_day);
    });

    work_days_list = work_days.valueOf();
  };


  // 生成报告事件
  $("#report").click(function () {
    var kaoqin = $("#kaoqin").val();
    var qingjia = $("#qingjia").val();
    var jiaban = $("#jiaban").val();
    var work_days = '[';
    var confirm_days = "\n| ";
    get_selected_day();
    $.each(work_days_list, function(i, v){
      work_days += "'" + v + "',";

      confirm_days += v + " | ";
      if((i+1)%5 === 0 && i!== 0){
        confirm_days += "\n| ";
      }
    });
    work_days += ']';
    var arg = {
      "dir1": kaoqin,
      "dir2": qingjia,
      "dir3": jiaban,
      "work_days": work_days
    };

    var check_confirm = "确定要提交? \n"
    +"考勤: " + kaoqin + "\n"
    +"请假: " + qingjia + "\n"
    +"加班: " + jiaban + "\n"
    +"日期: " + confirm_days + "\n"
    +"共计: " + work_days_list.length + "天";

    var status = confirm(check_confirm);
    if (!status) {
      return false;
    }
    $("#imgWait4").show();
    $.ajax({
      url: "/report",
      type: "POST",
      data: arg,
      dataType: "json",
      success: function (data) {
        if (data.status === "True") {
          alert("生成报告成功！");
        }
        if (data.status === "False") {
          alert(data.msg);
        }
        $("#imgWait4").hide();
        refresh_list_func({"dir_name": "dir5"});
      },
      error: function () {
        alert("生成报告失败！");
        $("#imgWait4").hide();
      }
    });
  });

  // 报告文件下载
  $("#download5").click(function () {
    var file_name = $('input:radio[name=radio_dir5]:checked').val();
    var arg = {
      "dir_name": "dir5",
      "file_name": file_name
    };
    window.open("/download?file_name="+file_name)
  });



});

