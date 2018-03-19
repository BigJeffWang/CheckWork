# coding: utf8
# @Author  : WangYe
# @contact : bigjeffwang@163.com
# @Time    : 2018/3/9 下午12:19
# @File    : __init__.py

import time
import os
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import random
import string
# from config import get_config_json


def get_parent_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_argument_dict(request, keys=None, format_str=False, format_keys=True, format_eval=True):
    """
    :param request: 前端请求
    :param keys: keys=["aa", "bb"] 判断出入列表里的值,是否在请求参数里,没有报错
    :param format_str: 是否需要把所有int类型,强转成字符串
    :param format_eval: 是否开启 把字符串 '["a","b"]' '{"a":1,"b":"1"}' 强转回list dict
    :param format_keys: 是否开启 把key的值 转为全小写
    :return:
    """
    # 获取参数字典
    tmp = {}
    request_type = request.headers.get('Content-Type')
    if request_type:
        content_type = request_type.split(';')[0].lower()
        if content_type == "application/json":
            request_args = request.get_json()
        else:  # multipart/form-data
            request_args = request.values
    else:
        request_args = request.values
    if keys:
        for key in keys:
            if key not in request_args:
                raise Exception("请求缺少 [%s] 参数" % key)
    for key, value in request_args.items():
        if format_eval and isinstance(value, str) and value:
            if value[0] in ("[", "{", "(") and value[-1] in ("]", "}", ")"):
                value = eval(value)
        if format_keys:
            key_lower = key.lower()
        else:
            key_lower = key
        if format_str:
            if isinstance(value, (int, float)):
                value = str(value)

        tmp[key_lower] = value

    args = dict(filter(lambda x: x[1] != '', tmp.items()))
    return args


def get_values(values):
    tmp = {}
    for key in values:
        tmp[key] = values.get(key).encode('utf8').replace("'", "\"").replace("\n", "").replace("\t", "").replace("\r", "")
    return tmp


def get_hash_id():
    return '%s%s' % (time.strftime("%Y%m%d%H%M%S", time.localtime()), get_random_str(6))


def new_report(testreport):
    lists = os.listdir(testreport)
    lists.sort(key=lambda fn: os.path.getmtime(testreport + "/" + fn))
    file_new = ""
    if lists:
        file_new = os.path.join(testreport, lists[-1])
    return file_new


def send_mail(file_path, to_users):
    website_data = get_config_json()['cife']['website']
    _user = website_data['email_user']
    _pwd = website_data['email_pwd']
    _to = to_users
    _subject = website_data['email_subject']

    with open(file_path, 'rb') as f:
        mail_body = f.read()

    msg = MIMEText(mail_body, 'html', 'utf-8')

    msg['Subject'] = Header(_subject, "utf-8")
    msg["From"] = _user
    msg["To"] = Header(",".join(_to), 'utf-8')

    # try:
    s = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
    s.login(_user, _pwd)
    s.sendmail(_user, _to, msg.as_string())
    s.quit()
    # except smtplib.SMTPException,e:


def get_random_str(num):
    str1 = "".join([str(i) for i in range(10)])
    str2 = string.ascii_letters
    return "".join(random.sample(str1 + str2, num))


def encodeutf8(data):
    tmp_list = []
    for t in data:
        tmp_tuple = []
        for i in t:
            if isinstance(i, unicode):
                tmp_tuple.append(i.encode('utf8'))
            else:
                tmp_tuple.append(i)
        tmp_list.append(tmp_tuple)
    return tmp_list


def del_old_file(file_path, reserve_count, buffer_count):
    """

    :param file_path:
    :param reserve_count: 删掉文件后所保留剩余个数
    :param buffer_count: 缓冲个数,超出缓冲个数,将会按创建时间,删掉文件时间较旧的文件
    :return:
    """
    if len(os.listdir(file_path)) > buffer_count:
        file_list = [os.sep.join([file_path, v]) for v in os.listdir(file_path)]
        file_list.sort(key=lambda fn: os.path.getmtime(fn), reverse=True)
        for i in file_list[reserve_count:]:
            os.remove(i)


def save_upload_file(request_data):
    parent_path = get_parent_path()
    upload_path = os.path.join(parent_path, "uploads")
    file_name = request_data["file_name"]
    dir_name = request_data["dir_name"]
    file_path = os.path.join(upload_path, dir_name, file_name)
    with open(file_path, 'wb') as f:
        f.write(request_data["upload_file"])
    return file_path


def del_file(args):
    dir_name = args.get("dir_name")
    del_list = args.get("del_list")

    if not del_list:
        return False
    parent_path = get_parent_path()

    if "dir4" in dir_name:
        del_employe(args)
    else:
        for tmp_file_name in del_list:
            del_file_path = os.path.join(parent_path, "uploads", dir_name, tmp_file_name)
            if os.path.isfile(del_file_path):
                os.remove(del_file_path)
    return True


def del_employe(args):
    dir_name = args.get("dir_name")
    del_list = args.get("del_list")
    parent_path = get_parent_path()
    show_path = os.path.join(parent_path, "uploads", dir_name)
    show_list = get_employe(show_path)
    write_list = []
    for show in show_list:
        if show not in del_list:
            write_list.append(show + "\n")

    employe_file = get_employe_file_path(show_path)
    with open(employe_file, "w", encoding="utf-8") as f:
        f.writelines(write_list)

    return True


def show_file(args):
    dir_name = args.get("dir_name")
    if not dir_name:
        return False
    parent_path = get_parent_path()
    show_path = os.path.join(parent_path, "uploads", dir_name)
    show_file_list = []
    if os.path.isdir(show_path):
        if "dir4" in dir_name:
            show_file_list = get_employe(show_path)
        else:
            show_file_list = sort_file_list(show_path)
    return show_file_list


def get_employe(show_path):
    employe_file = get_employe_file_path(show_path)
    show_file_list = []
    with open(employe_file, "r", encoding="utf-8") as f:
        for line in f:
            tmp_line = line.replace('\n', '')
            if tmp_line:
                show_file_list.append(tmp_line)
    return show_file_list


def get_employe_dict(show_path=None, dir_name="dir4"):
    if not show_path:
        parent_path = get_parent_path()
        show_path = os.path.join(parent_path, "uploads", dir_name)

    employe_list = get_employe(show_path)

    employe_dict = {}
    if not employe_list:
        return employe_dict

    for item in employe_list:
        employe_id, employe_name, employe_dept, employe_email = item.split(" ")
        employe_dict[employe_name] = {
            "employe_name": employe_name,
            "employe_id": employe_id,
            "employe_dept": employe_dept,
            "employe_email": employe_email,
        }

    return employe_dict


def get_employe_item(employe_dict, employe_name, key="employe_id"):
    employe_item = ""
    if employe_name in employe_dict:
        employe_item = employe_dict[employe_name].get(key, "")
    return employe_item


def employe_add(args):
    dir_name = args.get("dir_name")
    emp_id = args.get("emp_id").strip()
    emp_dept = args.get("emp_dept").strip()
    emp_email = args.get("emp_email").strip()
    emp_name = args.get("emp_name").strip()
    if not (dir_name and emp_id and emp_name and emp_dept and emp_email):
        return False
    new_employe = " ".join([emp_id, emp_name, emp_dept, emp_email])
    parent_path = get_parent_path()
    show_path = os.path.join(parent_path, "uploads", dir_name)
    employe_file = get_employe_file_path(show_path)
    show_list = get_employe(show_path)
    write_list = map(lambda x: x + "\n", [new_employe] + show_list)

    with open(employe_file, "w", encoding="utf-8") as f:
        f.writelines(write_list)
    return True


def get_employe_file_path(show_path, file_name="employe.txt"):
    return os.path.join(show_path, file_name)


def get_file_create_time(file_path):
    t = os.stat(file_path).st_ctime
    return t


def sort_file_list(show_path):
    show_file_list = os.listdir(show_path)
    file_dict = {}
    for item in show_file_list:
        tmp_file_path = os.path.join(show_path, item)
        file_dict[get_file_create_time(tmp_file_path)] = item
    sort_keys = sorted(file_dict.keys(), reverse=True)
    file_list = [file_dict[x] for x in sort_keys]
    return file_list


def get_file_path(dir_name, file_name):
    parent_path = get_parent_path()
    file_path = os.path.join(parent_path, "uploads", dir_name, file_name)
    return file_path


def get_dir_path(dir_name):
    parent_path = get_parent_path()
    dir_path = os.path.join(parent_path, "uploads", dir_name)
    return dir_path


# if __name__ == "__main__":
#     get_employe_id()

# mystring=replace(mystring,chr(39),"&acute;") '替换单引号
#
# mystring=replace(mystring,chr(34),"&quot;")    '替换双引号
#
# mystring=replace(mystring,"<","&lt;")    '替换<
#
# mystring=replace(mystring,">","&gt;")    '替换>
#
# mystring=replace(mystring,chr(13),"<br>") '替换回车符
#
# mystring=replace(mystring,chr(32),"&nbsp;") '替换空格符
#
# mystring=replace(mystring,chr(9),"&nbsp; &nbsp; &nbsp; &nbsp;") '替换tab符
