$(function () {
  var show_list = function(arg) {
    var show_file_list = ["111.xlsx", "222.xlsx", "333.xlsx"];
    var show_html = "";

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
    $('#' + arg["dir_name"]).html(show_html);
  };


  var insert_checked_func = function() {
    console.log(123);
    var aaa = $('#work_excel2 input:radio[name=radio_dir1]:checked').val();
    var bbb = $('input:radio[name=radio_dir2]:checked').val();
    var ccc = $('input:radio[name=radio_dir3]:checked').val();
    var ddd = $('.radio_dir1[checked]').val();

    var eee = $('input:radio[name=asd]:checked').val();
    console.log(aaa);
    // console.log(bbb);
    // console.log(ccc);
    console.log(ddd);
    console.log(234);
    console.log(eee)
  };

  show_list({"dir_name": "dir1"});
  show_list({"dir_name": "dir2"});
  show_list({"dir_name": "dir3"});
  show_list({"dir_name": "dir4"});
  insert_checked_func();

  $("input:radio[name=radio_dir1]").click(function(){
    var aaa = $('input:radio[name=radio_dir1]:checked').val();
    console.log(aaa);
  });
});