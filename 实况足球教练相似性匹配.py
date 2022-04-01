# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time    : 2022-04-01 21:29
# Author  : Seto.Kaiba
from typing import Any, List, Dict
import random
import math
import xlrd

"""
匹配实况足球手游教练的风格相似度，寻找风格相差最多的教练
"""


class Coach(object):
    def __init__(
            self,
            name: str,
            attack_formation: str,
            attack_style: str,
            backfield_organization: str,
            attack_area: str,
            position_style: str,
            defense_style: str,
            defense_area: str,
            scramble_style: str
    ):
        self.name = name
        self.attack_formation = attack_formation
        self.attack_style = attack_style
        self.backfield_organization = backfield_organization
        self.attack_area = attack_area
        self.position_style = position_style
        self.defense_style = defense_style
        self.defense_area = defense_area
        self.scramble_style = scramble_style

    def to_dict(self) -> Dict:
        return self.__dict__

    def to_value_list(self) -> List[str]:
        return [
            self.attack_style,
            self.backfield_organization,
            self.attack_area,
            self.position_style,
            self.defense_style,
            self.defense_area,
            self.scramble_style
        ]

    def to_translated_dict(self) -> Dict[str, str]:
        return {
            "姓名": self.name,
            "进攻阵型": self.attack_formation,
            "进攻风格": self.attack_style,
            "后场组织者": self.backfield_organization,
            "进攻区域": self.attack_area,
            "跑位": self.position_style,
            "防守风格": self.defense_style,
            "围堵区域": self.defense_area,
            "施压": self.scramble_style
        }


def calc_diff_between(a: Coach, b: Coach) -> int:
    a_list = a.to_value_list()
    b_list = b.to_value_list()
    n = len(a_list)
    diff = 0
    for index in range(n):
        if a_list[index] != b_list[index]:
            diff += 1

    return diff


if __name__ == '__main__':
    coach_list = []

    data = xlrd.open_workbook('实况足球手游教练信息.xlsx')

    sheet = data.sheet_by_index(0)

    n_row = sheet.nrows
    n_coach = n_row - 1

    for i in range(1, n_row):
        row = sheet.row_values(i)
        coach = Coach(
            name=row[0],
            attack_formation=row[1],
            attack_style=row[2],
            backfield_organization=row[3],
            attack_area=row[4],
            position_style=row[5],
            defense_style=row[6],
            defense_area=row[7],
            scramble_style=row[8]
        )
        coach_list.append(coach)

    count = 0
    for i in range(n_coach - 1):
        for j in range(i + 1, n_coach):
            if calc_diff_between(coach_list[i], coach_list[j]) == 7:
                count += 1
                print("{:2d}: {} VS {}".format(
                    count,
                    coach_list[i].name,
                    coach_list[j].name
                ))
    pass
