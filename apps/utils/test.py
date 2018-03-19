# coding: utf8
# @Author  : WangYe
# @contact : bigjeffwang@163.com
# @Time    : 2018/3/9 下午6:47
# @File    : test

import xlrd, xlwt
import datetime

# from apps.utils.util import get_work_time, get_datetime, get_round_diff_time, get_diff_datetime, get_day_list, get_0_24point_time
#
# work_day = "2018-2-27"
# work_time = "10:00:00"
#
# work_day2 = "2018-3-2"
# work_time2 = "19:00:00"
#
# datetime_hour_9, datetime_hour_10, datetime_hour_18, datetime_hour_19, datetime_hour_12, datetime_hour_13 = get_work_time(
#     work_day)
#
# datetime_work_time = get_datetime(work_day + " " + work_time)
#
# print(datetime_hour_9, datetime_hour_10, datetime_hour_18, datetime_hour_19, datetime_hour_12, datetime_hour_13)
#
# print(datetime_work_time)
#
# time_res = datetime_work_time - datetime_hour_9
#
# diff_day = time_res.days
# diff_hour = time_res.seconds / 3600
#
# print(diff_day)
# print(diff_hour)
#
# diff_hour_round = get_round_diff_time(diff_hour)
# diff_hour_round1 = get_round_diff_time(1.534563)
# diff_hour_round2 = get_round_diff_time(1.634563)
# diff_hour_round3 = get_round_diff_time(0.5)
# diff_hour_round4 = get_round_diff_time(0.3)
#
# print(diff_hour_round)
# print(diff_hour_round2)
# print(diff_hour_round3)
# print(diff_hour_round4)
#
# print(str(get_round_diff_time(diff_hour)))
# print(str(1.5))
#
# end_time_datetime = get_datetime(work_day2 + " " + work_time2)
# begin_time_datetime = get_datetime(work_day + " " + work_time)
#
# diff_datetime = get_diff_datetime(end_time_datetime, begin_time_datetime)
# datetime_day = diff_datetime["datetime_day"]
# datetime_hour_round = diff_datetime["datetime_hour_round"]
# print(datetime_day)
# print(datetime_hour_round)
#
# for i in range(2):
#     print(i)
#
# day_list = get_day_list(begin_time_datetime, end_time_datetime)
# print(day_list)
#
# tmp_dict = {}
# b = "asd"
# bb = "asd"
# bbb = "asd"
# tmp_dict["a"] = {
#     b: {
#         "asd": bb,
#         "asd2": bbb
#     }
# }
# for i in range(3):
#     t_dict = {str(i): str(i + 1)}
#     # t_dict = {"a": {str(i): str(i + 1)}}
#     tmp_dict["a"] = dict(tmp_dict["a"], **t_dict)
#
# print(tmp_dict)
#
#
# datetime_hour_0, datetime_hour_24 = get_0_24point_time(work_day)
# print(datetime_hour_24)
#
# count_hours = get_diff_datetime(datetime_hour_24, begin_time_datetime)
# print(count_hours)
#
# tmp_dict["b"] = {"c":{"d":"123"}}
# print(tmp_dict)

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    # style.borders = borders

    return style


# 写excel
def write_excel():
    f = xlwt.Workbook()  # 创建工作簿

    '''
    创建第一个sheet:
      sheet1
    '''
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'业务', u'状态', u'北京', u'上海', u'广州', u'深圳', u'状态小计', u'合计']
    column0 = [u'机票', u'船票', u'火车票', u'汽车票', u'其它']
    status = [u'预订', u'出票', u'退票', u'业务小计']

    # 生成第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))

    # 生成第一列和最后一列(合并4行)
    i, j = 1, 0
    while i < 4 * len(column0) and j < len(column0):
        sheet1.write_merge(i, i + 3, 0, 0, column0[j], set_style('Arial', 220, True))  # 第一列
        sheet1.write_merge(i, i + 3, 7, 7)  # 最后一列"合计"
        i += 4
        j += 1

    sheet1.write_merge(21, 21, 0, 1, u'合计', set_style('Times New Roman', 220, True))

    # 生成第二列
    i = 0
    while i < 4 * len(column0):
        for j in range(0, len(status)):
            sheet1.write(j + i + 1, 1, status[j])
        i += 4

    f.save('demo1.xlsx')  # 保存文件


if __name__ == '__main__':
    # generate_workbook()
    # read_excel()
    write_excel()