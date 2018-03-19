# coding: utf8
# @Author  : WangYe
# @contact : bigjeffwang@163.com
# @Time    : 2018/3/8 上午11:29
# @File    : index

from apps.app import app
from flask_mako import render_template
from flask import request, jsonify, send_file, send_from_directory, make_response
from apps.utils import save_upload_file, get_argument_dict, del_file, show_file, employe_add, get_file_path, get_dir_path
from apps.utils.util import get_report


msg = " 失败! 请联系王晔:18612570985"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        request_data = get_argument_dict(request)
        upload_file = request.files['upload_file']
        if upload_file:
            file_name = upload_file.filename
            handwork = upload_file.read()
            request_data["upload_file"] = handwork
            request_data["file_name"] = file_name
        else:
            return jsonify({"status": "False", "msg": "上传文件,写入服务器" + msg})

        file_path = save_upload_file(request_data)
        return jsonify({"status": "True"}) if file_path else jsonify(
            {"status": "False", "msg": "上传文件,写入服务器" + msg})


@app.route('/dellist', methods=['POST'])
def del_list():
    if request.method == 'POST':
        request_data = get_argument_dict(request)
        res = del_file(request_data)
        return jsonify({"status": "True"}) if res else jsonify(
            {"status": "False", "msg": "删除文件,写入服务器" + msg})


@app.route('/refreshlist', methods=['POST'])
def refresh_list():
    if request.method == 'POST':
        request_data = get_argument_dict(request)
        res = show_file(request_data)
        return jsonify({"show_file_list": res, "list_len": len(res)})


@app.route('/emp_add', methods=['POST'])
def emp_add():
    if request.method == 'POST':
        request_data = get_argument_dict(request)
        res = employe_add(request_data)
        return jsonify({"status": "True"}) if res else jsonify(
            {"status": "False", "msg": "新员工添加" + msg})


@app.route('/report', methods=['POST'])
def report():
    if request.method == 'POST':
        request_data = get_argument_dict(request)
        res = ""
        err = ""
        try:
            res = get_report(request_data)
        except Exception as e:
            err += str(e)
        return jsonify({"status": "True"}) if res else jsonify({"status": "False", "msg": "生成考勤报告" + msg + err})


@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        request_data = get_argument_dict(request)
        dir_name = "dir5"
        file_name = request_data["file_name"]
        dir_path = get_dir_path(dir_name)

        response = make_response(send_from_directory(dir_path, file_name, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name.encode().decode('latin-1'))
        return response

    if request.method == 'GET':
        request_data = get_argument_dict(request)
        # res = send_down_file(request_data)
        ONE_MONTH = 60 * 60 * 24 * 30
        dir_name = "dir5"
        file_name = request_data["file_name"]
        file_path = get_file_path(dir_name, file_name)
        return send_file(open(file_path, 'rb'),
                         mimetype='application/octet-stream',
                         cache_timeout=ONE_MONTH,
                         as_attachment=True,
                         attachment_filename=file_name.encode('utf-8'))


