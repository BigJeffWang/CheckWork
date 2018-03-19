# coding: utf8
# @Author  : WangYe
# @contact : bigjeffwang@163.com
# @Time    : 2018/3/12 下午8:17
# @File    : util

import xlrd, xlwt
import datetime
import os
import time

# def add_import_path():
#     import os
#     import sys
#     import_path = str(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../")))
#     sys.path.append(import_path)
#
# add_import_path()

from apps.utils import get_employe_dict, get_employe_item, get_file_path

jiejiari_list = ["1-1", "5-1", "10-1", "10-2", "10-3"]


def get_format_day(day_str):
    datetime_day = datetime.datetime.strptime(day_str, "%Y-%m-%d")
    return datetime_day.strftime("%Y-%m-%d")


def get_qingjia(file_path, work_days=None, name_index=5, begin_index=13, end_index=14, total_index=15, type_index=8):
    workbook = xlrd.open_workbook(file_path)
    sheet_0 = workbook.sheet_by_index(0)
    sheet_rows = sheet_0.nrows
    qingjia_dict = {}
    for row_index in range(sheet_rows):
        if not row_index:
            continue
        row = sheet_0.row_values(row_index)
        name = row[name_index]
        total_time = row[total_index]
        type_qingjia = row[type_index]
        if sheet_0.cell(row_index, begin_index).ctype == 3:
            begin_time_datetime = xlrd.xldate_as_datetime(row[begin_index], workbook.datemode)
        else:
            raise Exception("请假表 请假开始时间 格式不合格 非时间类型 错误在第:" + str(row_index + 1) + "行, 第:" + str(begin_index + 1) + "列!")

        if sheet_0.cell(row_index, end_index).ctype == 3:
            end_time_datetime = xlrd.xldate_as_datetime(row[end_index], workbook.datemode)
        else:
            raise Exception("请假表 请假结束时间 格式不合格 非时间类型 错误在第:" + str(row_index + 1) + "行, 第:" + str(end_index + 1) + "列!")

        qingjia_detail = get_qingjia_detail(begin_time_datetime, end_time_datetime, total_time, work_days, type_qingjia)

        if name not in qingjia_dict:
            qingjia_dict[name] = qingjia_detail
        else:
            qingjia_dict[name] = dict(qingjia_dict[name], **qingjia_detail)
    return qingjia_dict


def get_jiaban(file_path, work_days=None, name_index=6, begin_index=8, end_index=9, total_index=10):
    workbook = xlrd.open_workbook(file_path)
    sheet_0 = workbook.sheet_by_index(0)
    sheet_rows = sheet_0.nrows
    jiaban_dict = {}
    for row_index in range(sheet_rows):
        if not row_index:
            continue
        row = sheet_0.row_values(row_index)
        name = row[name_index]
        total_time = row[total_index]
        if sheet_0.cell(row_index, begin_index).ctype == 3:
            begin_time_datetime = xlrd.xldate_as_datetime(row[begin_index], workbook.datemode)
        else:
            raise Exception("加班表 加班开始时间 格式不合格 非时间类型 错误在第:" + str(row_index + 1) + "行, 第:" + str(begin_index + 1) + "列!")
        if sheet_0.cell(row_index, end_index).ctype == 3:
            end_time_datetime = xlrd.xldate_as_datetime(row[end_index], workbook.datemode)
        else:
            raise Exception("加班表 加班结束时间 格式不合格 非时间类型 错误在第:" + str(row_index + 1) + "行, 第:" + str(end_index + 1) + "列!")

        jiaban_detail = get_jiaban_detail(begin_time_datetime, end_time_datetime, total_time, work_days)

        if name not in jiaban_dict:
            jiaban_dict[name] = jiaban_detail
        else:
            jiaban_dict[name] = dict(jiaban_dict[name], **jiaban_detail)

    return jiaban_dict


def get_kaoqin(file_path, name_index=1, begin_index=3):
    workbook = xlrd.open_workbook(file_path)
    sheet_0 = workbook.sheet_by_index(0)
    sheet_rows = sheet_0.nrows
    tmp_dict = {}
    employe_dict = get_employe_dict()
    for row_index in range(sheet_rows):
        if not row_index:
            continue
        row = sheet_0.row_values(row_index)
        name = row[name_index]
        depart_name = get_employe_item(employe_dict, name, "employe_dept")
        employe_id = get_employe_item(employe_dict, name)
        try:
            begin_time_datetime = datetime.datetime.strptime(row[begin_index], "%Y/%m/%d %H:%M:%S")
        except:
            raise Exception("考勤表 时间 格式不合格 非时间类型 错误在第:" + str(row_index + 1) + "行, 第:" + str(begin_index + 1) + "列!")
        begin_time = begin_time_datetime.strftime("%Y-%m-%d %H:%M:%S")
        work_day = begin_time.split(" ")[0]
        work_day = get_format_day(work_day)
        if name not in tmp_dict:
            tmp_dict[name] = {
                work_day: {
                    "name": name,
                    "work_day": work_day,
                    "begin_time": begin_time,
                    "end_time": "",
                    "begin_time_datetime": begin_time_datetime,
                    "end_time_datetime": begin_time_datetime,
                    "depart_name": depart_name,
                    "employe_id": employe_id,
                    "relative_time": "",  # 对应时段
                    "total_attendance": "",  # 出勤总计
                    "pingri": "",  # 平日
                    "zhoumo": "*",  # 周末
                    "jiejiari": "",  # 节假日
                    "pingri_jiaban": "",  # 平日加班
                    "zhoumo_jiaban": "",  # 周末加班
                    "jiejiari_jiaban": "",  # 节假日加班
                    "chidao": "",  # 迟到,
                    "zaotui": "",  # 早退,
                    "total_queqin": "",  # 缺勤总计
                    "qingjia_begin_time": "",  # 请假开始时间
                    "qingjia_end_time": "",  # 请假结束时间
                    "qingjia_total_time": "",  # 请假总计
                    "qingjia_type": "",  # 请假类型
                    "jiaban_begin_time": "",  # 加班开始时间
                    "jiaban_end_time": "",  # 加班结束时间
                    "jiaban_total_time": "",  # 加班总计
                }
            }
        else:
            if work_day not in tmp_dict[name]:
                tmp_dict[name][work_day] = {
                    "name": name,
                    "work_day": work_day,
                    "begin_time": begin_time,
                    "end_time": "",
                    "begin_time_datetime": begin_time_datetime,
                    "end_time_datetime": begin_time_datetime,
                    "depart_name": depart_name,
                    "employe_id": employe_id,
                    "relative_time": "",  # 对应时段
                    "total_attendance": "",  # 出勤总计
                    "pingri": "",  # 平日
                    "zhoumo": "*",  # 周末
                    "jiejiari": "",  # 节假日
                    "pingri_jiaban": "",  # 平日加班
                    "zhoumo_jiaban": "",  # 周末加班
                    "jiejiari_jiaban": "",  # 节假日加班
                    "chidao": "",  # 迟到,
                    "zaotui": "",  # 早退,
                    "total_queqin": "",  # 缺勤总计
                    "qingjia_begin_time": "",  # 请假开始时间
                    "qingjia_end_time": "",  # 请假结束时间
                    "qingjia_total_time": "",  # 请假总计
                    "qingjia_type": "",  # 请假类型
                    "jiaban_begin_time": "",  # 加班开始时间
                    "jiaban_end_time": "",  # 加班结束时间
                    "jiaban_total_time": "",  # 加班总计

                }
            else:
                if begin_time_datetime <= tmp_dict[name][work_day]["begin_time_datetime"]:
                    tmp_dict[name][work_day]["begin_time_datetime"] = begin_time_datetime
                    tmp_dict[name][work_day]["begin_time"] = begin_time
                else:
                    tmp_dict[name][work_day]["end_time_datetime"] = begin_time_datetime
                    tmp_dict[name][work_day]["end_time"] = begin_time

    return tmp_dict


def get_qingjia_detail(begin_time_datetime, end_time_datetime, total_time, work_days, type_qingjia):
    begin_time = begin_time_datetime.strftime("%Y-%m-%d %H:%M")
    end_time = end_time_datetime.strftime("%Y-%m-%d %H:%M")
    begin_work_day = begin_time.split(" ")[0]
    end_work_day = end_time.split(" ")[0]
    diff_datetime = get_diff_datetime(end_time_datetime, begin_time_datetime)
    datetime_day = diff_datetime["datetime_day"]
    day_list = get_day_list(begin_time_datetime, end_time_datetime)
    day_list = [x for x in day_list if x in work_days]  # 防止请假 周五到周一 实际工作日2天
    qingjia_detail = {}
    begin_work_day = get_format_day(begin_work_day)
    if datetime_day == 0:
        qingjia_detail[begin_work_day] = {
            begin_time: {
                "begin_time": begin_time,
                "end_time": end_time,
                "total_time": total_time,
                "type_qingjia": type_qingjia
            }
        }
    else:
        for work_day in day_list:
            work_day = get_format_day(work_day)
            datetime_hour_9, datetime_hour_10, datetime_hour_18, datetime_hour_19, datetime_hour_12, datetime_hour_13 = \
                get_work_time(work_day)
            if work_day == begin_work_day:
                if begin_time_datetime > datetime_hour_9:
                    total_time_1 = get_diff_datetime(datetime_hour_19, begin_time_datetime)["datetime_hour_round"]
                    tmp_end_time = datetime_hour_19.strftime("%Y-%m-%d %H:%M")
                else:
                    total_time_1 = get_diff_datetime(datetime_hour_18, begin_time_datetime)["datetime_hour_round"]
                    tmp_end_time = datetime_hour_18.strftime("%Y-%m-%d %H:%M")

                if begin_time_datetime < datetime_hour_12:
                    total_time_1 -= 1  # 刨去午休
                if datetime_hour_12 <= begin_time_datetime <= datetime_hour_13:
                    total_time_1 = 6  # 害怕脑残 请假起始日期是午休时间段 9点以后请假 朝10晚7 下午6个小时
                qingjia_detail[work_day] = {
                    begin_time: {
                        "begin_time": begin_time,
                        "end_time": tmp_end_time,
                        "total_time": str(total_time_1),
                        "type_qingjia": type_qingjia
                    }
                }

            elif work_day == end_work_day:
                if end_time_datetime > datetime_hour_18:
                    total_time_2 = get_diff_datetime(end_time_datetime, datetime_hour_10)["datetime_hour_round"]
                    tmp_begin_time = datetime_hour_10.strftime("%Y-%m-%d %H:%M")

                else:
                    total_time_2 = get_diff_datetime(end_time_datetime, datetime_hour_9)["datetime_hour_round"]
                    tmp_begin_time = datetime_hour_9.strftime("%Y-%m-%d %H:%M")

                if end_time_datetime > datetime_hour_13:
                    total_time_2 -= 1
                if datetime_hour_12 <= end_time_datetime <= datetime_hour_13:
                    total_time_2 = 2
                qingjia_detail[work_day] = {
                    tmp_begin_time: {
                        "begin_time": tmp_begin_time,
                        "end_time": end_time,
                        "total_time": str(total_time_2),
                        "type_qingjia": type_qingjia
                    }
                }
            else:
                tmp_default_begin_time = work_day + " 09:00"
                qingjia_detail[work_day] = {
                    tmp_default_begin_time: {
                        "begin_time": work_day + " 09:00",
                        "end_time": work_day + " 18:00",
                        "total_time": "8.0",
                        "type_qingjia": type_qingjia
                    }
                }
    return qingjia_detail


def get_jiaban_detail(begin_time_datetime, end_time_datetime, total_time, work_days):
    begin_time = begin_time_datetime.strftime("%Y-%m-%d %H:%M")
    end_time = end_time_datetime.strftime("%Y-%m-%d %H:%M")
    begin_work_day = begin_time.split(" ")[0]
    end_work_day = end_time.split(" ")[0]
    diff_datetime = get_diff_datetime(end_time_datetime, begin_time_datetime)
    datetime_day = diff_datetime["datetime_day"]
    day_list = get_day_list(begin_time_datetime, end_time_datetime)
    jiaban_detail = {}

    if datetime_day == 0:
        work_day = begin_work_day
        work_day = get_format_day(work_day)
        if work_day in work_days:
            type_jiaban = "pingri"
        else:
            if work_day in jiejiari_list:
                type_jiaban = "jiejiari"
            else:
                type_jiaban = "zhoumo"
        jiaban_detail[begin_work_day] = {
            begin_time: {
                "begin_time": begin_time,
                "end_time": end_time,
                "total_time": total_time,
                "type_jiaban": type_jiaban
            }
        }
    else:
        for work_day in day_list:
            work_day = get_format_day(work_day)
            if work_day in work_days:
                type_jiaban = "pingri"
            else:
                if work_day in jiejiari_list:
                    type_jiaban = "jiejiari"
                else:
                    type_jiaban = "zhoumo"
            datetime_hour_0, datetime_hour_24 = get_0_24point_time(work_day)
            tmp_end_time = work_day + " 24:00"
            tmp_begin_time = work_day + " 00:00"
            if work_day == begin_work_day:
                total_time_1 = get_diff_datetime(datetime_hour_24, begin_time_datetime)["datetime_hour_round"]
                total_time -= total_time_1
                jiaban_detail[begin_work_day] = {
                    begin_time: {
                        "begin_time": begin_time,
                        "end_time": tmp_end_time,
                        "total_time": total_time_1,
                        "type_jiaban": type_jiaban
                    }
                }
            elif work_day == end_work_day:
                total_time_2 = get_diff_datetime(end_time_datetime, datetime_hour_0)["datetime_hour_round"]
                total_time_2 = total_time if total_time < total_time_2 else total_time_2
                jiaban_detail[begin_work_day] = {
                    tmp_begin_time: {
                        "begin_time": tmp_begin_time,
                        "end_time": end_time,
                        "total_time": total_time_2,
                        "type_jiaban": type_jiaban
                    }
                }
            else:
                jiaban_detail[begin_work_day] = {
                    tmp_begin_time: {
                        "begin_time": tmp_begin_time,
                        "end_time": tmp_end_time,
                        "total_time": "24",
                        "type_jiaban": type_jiaban
                    }
                }

    return jiaban_detail


def get_day_list(begin_time_datetime, end_time_datetime, formate_type="%Y-%m-%d"):
    day_list = [begin_time_datetime.strftime(formate_type)]
    if (end_time_datetime - begin_time_datetime).days == 0:
        return day_list
    for i in range((end_time_datetime - begin_time_datetime).days):
        append_day = (begin_time_datetime + datetime.timedelta(days=i + 1)).strftime(formate_type)
        day_list.append(append_day)
    return day_list


def get_datetime(time_str):
    return datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")


def get_round_diff_time(diff_num):
    round_num = round(diff_num)
    if diff_num > round_num:
        if round_num:
            round_num += 0.5
        else:
            round_num = 1
    return round_num


def get_diff_datetime(datetime_end, datetime_bigen):
    datetime_diff = datetime_end - datetime_bigen
    datetime_day = datetime_diff.days
    datetime_hour = datetime_diff.seconds / 3600
    datetime_hour_round = get_round_diff_time(datetime_hour)
    return {"datetime_day": datetime_day, "datetime_hour_round": datetime_hour_round}


def get_work_time(work_day):
    datetime_hour_9 = get_datetime(work_day + " 09:00:00")
    datetime_hour_10 = get_datetime(work_day + " 10:00:00")
    datetime_hour_18 = get_datetime(work_day + " 18:00:00")
    datetime_hour_19 = get_datetime(work_day + " 19:00:00")
    datetime_hour_12 = get_datetime(work_day + " 12:00:00")
    datetime_hour_13 = get_datetime(work_day + " 13:00:00")
    return datetime_hour_9, datetime_hour_10, datetime_hour_18, datetime_hour_19, datetime_hour_12, datetime_hour_13


def get_chidao_work_time(work_day):
    datetime_hour_9_30 = get_datetime(work_day + " 09:30:00")
    datetime_hour_10_30 = get_datetime(work_day + " 10:30:00")
    datetime_hour_10 = get_datetime(work_day + " 10:00:00")
    datetime_hour_10_01 = get_datetime(work_day + " 10:01:00")
    datetime_hour_09_01 = get_datetime(work_day + " 09:01:00")
    return datetime_hour_9_30, datetime_hour_10_30, datetime_hour_10, datetime_hour_10_01, datetime_hour_09_01


def get_0_24point_time(work_day):
    datetime_hour_0 = get_datetime(work_day + " 00:00:00")
    datetime_hour_24 = datetime_hour_0 + datetime.timedelta(days=1)
    return datetime_hour_0, datetime_hour_24


def get_work_day(datetime_work):
    return datetime_work.strftime("%Y-%m-%d")


def get_report(request_data):
    from_9_to_6 = "朝9晚6"
    from_10_to_7 = "朝10晚7"
    dir_kaoqin = request_data.get("dir1")
    dir_qingjia = request_data.get("dir2")
    dir_jiaban = request_data.get("dir3")
    work_days = request_data.get("work_days")
    work_days = [get_format_day(work_day) for work_day in work_days]
    file_name = work_days[0].split("-")[0] + "年" + work_days[0].split("-")[1] + "月" + "全员考勤.xls"
    path_kaoqin = get_file_path("dir1", dir_kaoqin)
    path_qingjia = get_file_path("dir2", dir_qingjia)
    path_jiaban = get_file_path("dir3", dir_jiaban)
    qingjia_dict = get_qingjia(path_qingjia, work_days)
    jiaban_dict = get_jiaban(path_jiaban, work_days)
    kaoqin_dict = get_kaoqin(path_kaoqin)
    employe_dict = get_employe_dict()
    kaoqin_abnormal_dict = {}
    kaoqin_chidao_dict = {}
    for employe_name, _ in employe_dict.items():
        if employe_name not in kaoqin_dict:
            kaoqin_dict[employe_name] = {}

    for kaoqin_name, v in kaoqin_dict.items():
        employe_id = get_employe_item(employe_dict, kaoqin_name)
        employe_dept = get_employe_item(employe_dict, kaoqin_name, "employe_dept")
        for work_day in work_days:
            datetime_hour_9, datetime_hour_10, datetime_hour_18, datetime_hour_19, datetime_hour_12, datetime_hour_13 = get_work_time(
                work_day)
            if work_day not in v:
                v[work_day] = {
                    "name": kaoqin_name,
                    "work_day": work_day,
                    "begin_time": "",
                    "end_time": "",
                    "depart_name": employe_dept,
                    "employe_id": employe_id,
                    "relative_time": "",  # 对应时段
                    "total_attendance": "",  # 出勤总计
                    "pingri": "*",  # 平日
                    "zhoumo": "",  # 周末
                    "jiejiari": "",  # 节假日
                    "pingri_jiaban": "",  # 平日加班
                    "zhoumo_jiaban": "",  # 周末加班
                    "jiejiari_jiaban": "",  # 节假日加班
                    "chidao": "",  # 迟到,
                    "zaotui": "",  # 早退,
                    "total_queqin": "",  # 缺勤总计
                    "qingjia_begin_time": "",  # 请假开始时间
                    "qingjia_end_time": "",  # 请假结束时间
                    "qingjia_total_time": "",  # 请假总计
                    "qingjia_type": "",  # 请假类型
                    "jiaban_begin_time": "",  # 加班开始时间
                    "jiaban_end_time": "",  # 加班结束时间
                    "jiaban_total_time": "",  # 加班总计

                }
            else:
                begin_datetime = v[work_day]["begin_time_datetime"]
                end_datetime = v[work_day]["end_time_datetime"]
                # 计算 迟到早退时间 和 对应时段
                if begin_datetime <= datetime_hour_9:
                    # 正常 朝九
                    if end_datetime >= datetime_hour_18:
                        v[work_day]["relative_time"] = from_9_to_6
                    else:
                        # 早退 朝九
                        v[work_day]["relative_time"] = from_9_to_6
                        diff_datetime_dict = get_diff_datetime(datetime_hour_18, end_datetime)
                        time_zaotui = diff_datetime_dict["datetime_hour_round"]
                        if datetime_hour_12 <= end_datetime <= datetime_hour_13:
                            time_zaotui = 5
                        if end_datetime < datetime_hour_12:
                            time_zaotui -= 1
                        v[work_day]["zaotui"] = str(time_zaotui)
                else:
                    if begin_datetime <= datetime_hour_10:
                        if end_datetime >= datetime_hour_19:
                            # 正常 朝十
                            v[work_day]["relative_time"] = from_10_to_7
                        else:
                            if end_datetime > datetime_hour_18:
                                # 迟到 朝九
                                v[work_day]["relative_time"] = from_9_to_6
                                diff_datetime_dict = get_diff_datetime(begin_datetime, datetime_hour_9)
                                time_chidao = diff_datetime_dict["datetime_hour_round"]
                                v[work_day]["chidao"] = str(time_chidao)
                            else:
                                # 早退 朝十
                                v[work_day]["relative_time"] = from_10_to_7
                                diff_datetime_dict = get_diff_datetime(datetime_hour_19, end_datetime)
                                time_zaotui = diff_datetime_dict["datetime_hour_round"]

                                if datetime_hour_12 <= end_datetime <= datetime_hour_13:

                                    time_zaotui = 6
                                if end_datetime < datetime_hour_12:
                                    time_zaotui -= 1
                                v[work_day]["zaotui"] = str(time_zaotui)
                    else:
                        if end_datetime >= datetime_hour_19:
                            # 迟到 朝十
                            v[work_day]["relative_time"] = from_10_to_7
                            diff_datetime_dict = get_diff_datetime(begin_datetime, datetime_hour_10)
                            time_chidao = diff_datetime_dict["datetime_hour_round"]
                            v[work_day]["chidao"] = str(time_chidao)
                        else:
                            # 迟到 早退 朝十
                            v[work_day]["relative_time"] = from_10_to_7
                            diff_datetime_dict = get_diff_datetime(begin_datetime, datetime_hour_10)
                            time_chidao = diff_datetime_dict["datetime_hour_round"]
                            v[work_day]["chidao"] = str(time_chidao)
                            diff_datetime_dict = get_diff_datetime(datetime_hour_19, end_datetime)
                            time_zaotui = diff_datetime_dict["datetime_hour_round"]
                            if datetime_hour_12 <= end_datetime <= datetime_hour_13:
                                time_zaotui = 6
                            if end_datetime < datetime_hour_12:
                                time_zaotui -= 1
                            v[work_day]["zaotui"] = str(time_zaotui)

                # 计算 缺勤时间
                total_queqin = 0
                if v[work_day]["chidao"]:
                    total_queqin += float(v[work_day]["chidao"])
                if v[work_day]["zaotui"]:
                    total_queqin += float(v[work_day]["zaotui"])
                if total_queqin:
                    if total_queqin >= 8:
                        v[work_day]["total_queqin"] = "8.0"
                    else:
                        v[work_day]["total_queqin"] = str(total_queqin)

                # 计算 出勤时间
                total_attendance = get_diff_datetime(end_datetime, begin_datetime)["datetime_hour_round"]
                if begin_datetime < datetime_hour_12 and end_datetime > datetime_hour_13:
                    total_attendance -= 1
                if total_attendance:
                    v[work_day]["total_attendance"] = total_attendance

                # 计算 平日 周末
                month_day = work_day.split("-")[1] + "-" + work_day.split("-")[2]
                if month_day in jiejiari_list:
                    v[work_day]["jiejiari"] = "*"
                else:
                    v[work_day]["pingri"] = "*"
                v[work_day]["zhoumo"] = ""

        # 把请假表 加入到 考勤表 考虑到一天请两次假 所以用循环
        if kaoqin_name in qingjia_dict:
            for qingjia_work_day, qingjia_detail in qingjia_dict[kaoqin_name].items():
                if qingjia_work_day not in v:
                    v[qingjia_work_day] = {
                        "name": kaoqin_name,
                        "work_day": qingjia_work_day,
                        "begin_time": "",
                        "end_time": "",
                        "depart_name": employe_dept,
                        "employe_id": employe_id,
                        "relative_time": "",  # 对应时段
                        "total_attendance": "",  # 出勤总计
                        "pingri": "",  # 平日
                        "zhoumo": "",  # 周末
                        "jiejiari": "",  # 节假日
                        "pingri_jiaban": "",  # 平日加班
                        "zhoumo_jiaban": "",  # 周末加班
                        "jiejiari_jiaban": "",  # 节假日加班
                        "chidao": "",  # 迟到,
                        "zaotui": "",  # 早退,
                        "total_queqin": "",  # 缺勤总计
                        "qingjia_begin_time": "",  # 请假开始时间
                        "qingjia_end_time": "",  # 请假结束时间
                        "qingjia_total_time": "",  # 请假总计
                        "qingjia_type": "",  # 请假类型
                        "jiaban_begin_time": "",  # 加班开始时间
                        "jiaban_end_time": "",  # 加班结束时间
                        "jiaban_total_time": "",  # 加班总计
                    }
                    month_day = qingjia_work_day.split("-")[1] + "-" + qingjia_work_day.split("-")[2]
                    if month_day in jiejiari_list:
                        v[qingjia_work_day]["jiejiari"] = "*"
                    elif qingjia_work_day in work_days:
                        v[qingjia_work_day]["pingri"] = "*"
                    else:
                        v[qingjia_work_day]["zhoumo"] = "*"

                for _, qingjia_begin_time in qingjia_detail.items():
                    if v[qingjia_work_day]["qingjia_begin_time"] == "":
                        v[qingjia_work_day]["qingjia_begin_time"] = qingjia_begin_time["begin_time"]
                    else:
                        v[qingjia_work_day]["qingjia_begin_time"] += "," + qingjia_begin_time["begin_time"]

                    if v[qingjia_work_day]["qingjia_end_time"] == "":
                        v[qingjia_work_day]["qingjia_end_time"] = qingjia_begin_time["end_time"]
                    else:
                        v[qingjia_work_day]["qingjia_end_time"] += "," + qingjia_begin_time["end_time"]

                    if v[qingjia_work_day]["qingjia_total_time"] == "":
                        v[qingjia_work_day]["qingjia_total_time"] = qingjia_begin_time["total_time"]
                    else:
                        v[qingjia_work_day]["qingjia_total_time"] = str(
                            float(v[qingjia_work_day]["qingjia_total_time"]) + float(qingjia_begin_time["total_time"]))

                    if v[qingjia_work_day]["qingjia_type"] == "":
                        v[qingjia_work_day]["qingjia_type"] = qingjia_begin_time["type_qingjia"]
                    else:
                        v[qingjia_work_day]["qingjia_type"] += "," + qingjia_begin_time["type_qingjia"]

        # 把加班表 加入到 考勤表 考虑到一天请两次加班 所以用循环
        if kaoqin_name in jiaban_dict:
            for jiaban_work_day, jiaban_detail in jiaban_dict[kaoqin_name].items():
                if jiaban_work_day not in v:
                    v[jiaban_work_day] = {
                        "name": kaoqin_name,
                        "work_day": jiaban_work_day,
                        "begin_time": "",
                        "end_time": "",
                        "depart_name": employe_dept,
                        "employe_id": employe_id,
                        "relative_time": "",  # 对应时段
                        "total_attendance": "",  # 出勤总计
                        "pingri": "",  # 平日
                        "zhoumo": "",  # 周末
                        "jiejiari": "",  # 节假日
                        "pingri_jiaban": "",  # 平日加班
                        "zhoumo_jiaban": "",  # 周末加班
                        "jiejiari_jiaban": "",  # 节假日加班
                        "chidao": "",  # 迟到,
                        "zaotui": "",  # 早退,
                        "total_queqin": "",  # 缺勤总计
                        "qingjia_begin_time": "",  # 请假开始时间
                        "qingjia_end_time": "",  # 请假结束时间
                        "qingjia_total_time": "",  # 请假总计
                        "qingjia_type": "",  # 请假类型
                        "jiaban_begin_time": "",  # 加班开始时间
                        "jiaban_end_time": "",  # 加班结束时间
                        "jiaban_total_time": "",  # 加班总计
                    }
                    month_day = qingjia_work_day.split("-")[1] + "-" + qingjia_work_day.split("-")[2]
                    if month_day in jiejiari_list:
                        v[jiaban_work_day]["jiejiari"] = "*"
                    elif qingjia_work_day in work_days:
                        v[jiaban_work_day]["pingri"] = "*"
                    else:
                        v[jiaban_work_day]["zhoumo"] = "*"

                for _, jiaban_begin_time in jiaban_detail.items():
                    if v[jiaban_work_day]["jiaban_begin_time"] == "":
                        v[jiaban_work_day]["jiaban_begin_time"] = jiaban_begin_time["begin_time"]
                    else:
                        v[jiaban_work_day]["jiaban_begin_time"] = "," + jiaban_begin_time["begin_time"]

                    if v[jiaban_work_day]["jiaban_end_time"] == "":
                        v[jiaban_work_day]["jiaban_end_time"] = jiaban_begin_time["end_time"]
                    else:
                        v[jiaban_work_day]["jiaban_end_time"] = "," + jiaban_begin_time["end_time"]

                    if v[jiaban_work_day]["jiaban_total_time"] == "":
                        v[jiaban_work_day]["jiaban_total_time"] = jiaban_begin_time["total_time"]
                    else:
                        v[jiaban_work_day]["jiaban_total_time"] = str(
                            float(v[jiaban_work_day]["jiaban_total_time"]) + float(jiaban_work_day["total_time"]))
                    if jiaban_begin_time["type_jiaban"] == "zhoumo":
                        v[jiaban_work_day]["zhoumo_jiaban"] = "*"
                    elif jiaban_begin_time["type_jiaban"] == "jiejiari":
                        v[jiaban_work_day]["jiejiari_jiaban"] = "*"
                    else:
                        v[jiaban_work_day]["pingri_jiaban"] = "*"

        # 根据缺勤时间 > 请假时间 或者 加班时间 > 指纹出勤时间 的异常考勤 加入到 考勤异常表
        # 早上迟到半小时的,过滤出来,单独生成一个表
        for work_day in work_days:
            ab_total_queqin = v[work_day]["total_queqin"]
            ab_total_qingjia = v[work_day]["qingjia_total_time"]
            ab_total_chuqin = v[work_day]["total_attendance"]
            ab_toal_jiaban = v[work_day]["jiaban_total_time"]
            ab_total_queqin = float(ab_total_queqin) if ab_total_queqin else 0
            ab_total_qingjia = float(ab_total_qingjia) if ab_total_qingjia else 0
            ab_total_chuqin = float(ab_total_chuqin) if ab_total_chuqin else 0
            ab_toal_jiaban = float(ab_toal_jiaban) if ab_toal_jiaban else 0
            if ab_total_queqin > ab_total_qingjia or ab_toal_jiaban > ab_total_chuqin:
                if v[work_day]["chidao"] and not v[work_day]["zaotui"]:
                    if float(v[work_day]["chidao"]) <= float(1):
                        begin_datetime = v[work_day]["begin_time_datetime"]
                        datetime_hour_9_30, datetime_hour_10_30, datetime_hour_10, datetime_hour_10_01, datetime_hour_09_01 = get_chidao_work_time(work_day)
                        if datetime_hour_09_01 <= begin_datetime <= datetime_hour_9_30:
                            kaoqin_chidao_dict[kaoqin_name] = {
                                work_day: v[work_day]
                            }
                        elif datetime_hour_10_01 <= begin_datetime <= datetime_hour_10_30:
                            kaoqin_chidao_dict[kaoqin_name] = {
                                work_day: v[work_day]
                            }
                        else:
                            kaoqin_abnormal_dict[kaoqin_name] = {
                                work_day: v[work_day]
                            }
                else:
                    kaoqin_abnormal_dict[kaoqin_name] = {
                        work_day: v[work_day]
                    }
    write_excel(file_name, kaoqin_dict, kaoqin_abnormal_dict, kaoqin_chidao_dict)
    return True


def get_sort_list(kaoqin_dict, row_keys):
    sort_list = []
    for name, name_detail in kaoqin_dict.items():
        keys = list(name_detail.keys())
        keys.sort()
        name_detail_list = [name_detail[key] for key in keys]
        for detail in name_detail_list:
            work_day_list = []
            for key in row_keys:
                work_day_list.append(detail.get(key, ""))
            sort_list.append(work_day_list)
    return sort_list


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中
    style.alignment = alignment

    style.font = font
    return style


def write_excel(file_name, kaoqin_dict, kaoqin_abnormal_dict, kaoqin_chidao_dict):
    row0 = ['部门', '考勤号码', '姓名', '日期', '对应时段', '签到时间', '签退时间', '出勤总计', '迟到', '早退', '缺勤总计', '平日', '周末', '节假日',
            '请假开始', '请假结束', '请假总计', '请假类型',
            '加班开始', '加班结束', '加班总计', '平日加班', '周末加班', '节假日加班']

    row_keys = ['depart_name', 'employe_id', 'name', 'work_day', 'relative_time', 'begin_time', 'end_time',
                'total_attendance', 'chidao', 'zaotui', 'total_queqin', 'pingri', 'zhoumo', 'jiejiari',
                'qingjia_begin_time', 'qingjia_end_time', 'qingjia_total_time', 'qingjia_type',
                'jiaban_begin_time', 'jiaban_end_time', 'jiaban_total_time', 'pingri_jiaban', 'zhoumo_jiaban',
                'jiejiari_jiaban']
    sort_kaoqin_list = get_sort_list(kaoqin_dict, row_keys)
    sort_abnormal_list = get_sort_list(kaoqin_abnormal_dict, row_keys)
    sort_chidao_list = get_sort_list(kaoqin_chidao_dict, row_keys)

    f = xlwt.Workbook()
    sheet1_name = file_name
    sheet2_name = "(异常)" + file_name
    sheet3_name = "(迟到半小时)" + file_name
    sheet1 = f.add_sheet(sheet1_name, cell_overwrite_ok=True)  # 创建sheet
    sheet2 = f.add_sheet(sheet2_name, cell_overwrite_ok=True)  # 创建sheet
    sheet3 = f.add_sheet(sheet3_name, cell_overwrite_ok=True)  # 创建sheet

    col_count = len(row0)

    if kaoqin_dict:
        for i in range(col_count):
            # 生成第一行
            sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))

        for row_index, row_line in enumerate(sort_kaoqin_list):
            for col_index in range(col_count):
                sheet1.write(row_index+1, col_index, row_line[col_index])

    if kaoqin_abnormal_dict:
        for i in range(col_count):
            # 生成第一行
            sheet2.write(0, i, row0[i], set_style('Times New Roman', 220, True))

        for row_index, row_line in enumerate(sort_abnormal_list):
            for col_index in range(col_count):
                sheet2.write(row_index + 1, col_index, row_line[col_index])

    if kaoqin_chidao_dict:
        for i in range(col_count):
            # 生成第一行
            sheet3.write(0, i, row0[i], set_style('Times New Roman', 220, True))

        for row_index, row_line in enumerate(sort_chidao_list):
            for col_index in range(col_count):
                sheet3.write(row_index + 1, col_index, row_line[col_index])

    file_name_pre, file_name_next = file_name.split(".")
    time_str = str(time.time()).split(".")[0]
    file_name = file_name_pre + time_str + "." + file_name_next
    save_file_path = get_file_path("dir5", file_name)

    print(save_file_path)
    f.save(save_file_path)  # 保存文件

