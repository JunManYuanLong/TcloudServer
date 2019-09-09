import datetime
import random


def identity_generator():
    # 身份证号的前两位，省份代号
    sheng = (
        '11', '12', '13', '14', '15', '21', '22', '23', '31', '32', '33', '34', '35', '36', '37', '41', '42', '43',
        '44',
        '45', '46', '50', '51', '52', '53', '54', '61', '62', '63', '64', '65', '66')

    # 随机选择距离今天在7000到25000的日期作为出生日期（没有特殊要求我就随便设置的，有特殊要求的此处可以完善下）
    birthdate = (datetime.date.today() - datetime.timedelta(days=random.randint(8000, 15000)))

    # 拼接出身份证号的前17位（第3-第6位为市和区的代码，中国太大此处就偷懒了写了定值，有要求的可以做个随机来完善下；第15-第17位为出生的顺序码，随机在100到199中选择）
    ident = sheng[random.randint(0, 31)] + '0101' + birthdate.strftime("%Y%m%d") + str(random.randint(100, 199))
    # ident = '44180219921012383'
    # 前17位每位需要乘上的系数，用字典表示，比如第一位需要乘上7，最后一位需要乘上2
    coe = {
        1: 7, 2: 9, 3: 10, 4: 5, 5: 8, 6: 4, 7: 2, 8: 1, 9: 6, 10: 3, 11: 7, 12: 9, 13: 10, 14: 5, 15: 8, 16: 4,
        17: 2
    }
    summation = 0

    # for循环计算前17位每位乘上系数之后的和
    for i in range(17):
        summation = summation + int(ident[i:i + 1]) * coe[i + 1]  # ident[i:i+1]使用的是python的切片获得每位数字

    # 前17位每位乘上系数之后的和除以11得到的余数对照表，比如余数是0，那第18位就是1
    key = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}

    # 拼接得到完整的18位身份证号
    return ident + key[summation % 11]


class TraverseDict(object):
    def __init__(self):
        self.d_list = []

    def get_dict_keys_path(self, result, path=None):
        """  遍历dict，返回字典的值的路径和值组成的list

        :param result: 字典
        :param path: 递归使用，部分路径的值
        """
        for k, v in result.items():
            if isinstance(v, list) and v:  # and v  主要是v有可能为空list
                for num, a1 in enumerate(v):
                    if path:
                        self.get_dict_keys_path(a1, "{},{},{}".format(path, k, num))
                    else:
                        self.get_dict_keys_path(a1, "{},{}".format(k, num))
            elif isinstance(v, dict) and v:  # and v  主要是v有可能为dict
                if path:
                    self.get_dict_keys_path(v, "{},{}".format(path, k, ))
                else:
                    self.get_dict_keys_path(v, k)
            else:
                if path:
                    if not v:  # 当v为Fasle时，把它赋值None，已方便删除该key
                        v = None
                    _t = "{},{},{}".format(path, k, v)
                    t2 = _t.split(',')
                    for n, value in enumerate(t2):  # 遍历t2,转换里面为存数字的str为int
                        try:
                            t2[n] = int(value)
                        except Exception as e:
                            pass
                    self.d_list.append(t2)
                else:
                    self.d_list.append([k, v])

    def del_key(self, result, path_list):
        """  根据路径删除字典中指定的值

        :param result: dict
        :param path_list: 某个指定的值的路径list
        """
        num = len(path_list)
        if num == 1:
            return result.pop(path_list[0])

        return self.del_key(result[path_list.pop(0)], path_list)

    def data_tidy(self, result):
        """  删除指定规则中字典的值

        """
        for path in self.d_list:
            if path[-1] == 'None':
                self.del_key(result, path[:-1])
            elif path[-2].find('id') != -1 or path[-2].find('Id') != -1 or path[-2].find('Time') != -1:
                self.del_key(result, path[:-1])
            elif path[0].find('request') != -1:
                self.del_key(result, path[:-1])
        self.d_list.clear()  # 清理list，防止下次使用时保留上次的数据引起报错
