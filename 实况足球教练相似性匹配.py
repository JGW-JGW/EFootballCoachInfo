# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time    : 2022-04-01 21:29
# Author  : Seto.Kaiba
from typing import Any, List, Dict, Tuple
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
            formation: str,
            atk_attack_style: str,
            atk_backfield_organization: str,
            atk_attack_area: str,
            atk_position_style: str,
            atk_defense_style: str,
            atk_defense_area: str,
            atk_scramble_style: str,
            def_attack_style: str,
            def_backfield_organization: str,
            def_attack_area: str,
            def_position_style: str,
            def_defense_style: str,
            def_defense_area: str,
            def_scramble_style: str
    ):
        self.name = name
        self.formation = formation
        self.atk_attack_style = atk_attack_style
        self.atk_backfield_organization = atk_backfield_organization
        self.atk_attack_area = atk_attack_area
        self.atk_position_style = atk_position_style
        self.atk_defense_style = atk_defense_style
        self.atk_defense_area = atk_defense_area
        self.atk_scramble_style = atk_scramble_style
        self.def_attack_style = def_attack_style
        self.def_backfield_organization = def_backfield_organization
        self.def_attack_area = def_attack_area
        self.def_position_style = def_position_style
        self.def_defense_style = def_defense_style
        self.def_defense_area = def_defense_area
        self.def_scramble_style = def_scramble_style

    def has_same_atk_def(self) -> bool:
        return self.get_atk_value() == self.get_def_value()

    def get_atk_value(self) -> List[str]:
        return [
            self.atk_attack_style,
            self.atk_backfield_organization,
            self.atk_attack_area,
            self.atk_position_style,
            self.atk_defense_style,
            self.atk_defense_area,
            self.atk_scramble_style
        ]

    def get_def_value(self) -> List[str]:
        return [
            self.def_attack_style,
            self.def_backfield_organization,
            self.def_attack_area,
            self.def_position_style,
            self.def_defense_style,
            self.def_defense_area,
            self.def_scramble_style
        ]


def calc_diff_between(a: Coach, b: Coach) -> Tuple[int, str, str]:
    """
    calculate distance between two coaches
    :param a: coach a
    :param b: coach b
    :return: (distance between two coaches, a's ATK or DEF, b's ATK or DEF)
    """

    def calc_distance(a: List[str], b: List[str]) -> int:
        ans = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                ans += 1

        return ans

    if a.has_same_atk_def() and b.has_same_atk_def():
        return (
            calc_distance(a.get_atk_value(), b.get_atk_value()),
            'BOTH',
            'BOTH'
        )

    elif a.has_same_atk_def() and not b.has_same_atk_def():
        d_1 = (calc_distance(a.get_atk_value(), b.get_atk_value()), 'BOTH', 'ATK')
        d_2 = (calc_distance(a.get_atk_value(), b.get_def_value()), 'BOTH', 'DEF')

        return d_1 if d_1[0] > d_2[0] else d_2

    elif not a.has_same_atk_def() and b.has_same_atk_def():
        d_1 = (calc_distance(a.get_atk_value(), b.get_atk_value()), 'ATK', 'BOTH')
        d_2 = (calc_distance(a.get_def_value(), b.get_atk_value()), 'DEF', 'BOTH')

        return d_1 if d_1[0] > d_2[0] else d_2

    else:  # a 的进攻战术和防守战术不相同，b 也一样
        d_list = [
            (calc_distance(a.get_atk_value(), b.get_atk_value()), 'ATK', 'ATK'),
            (calc_distance(a.get_atk_value(), b.get_def_value()), 'ATK', 'DEF'),
            (calc_distance(a.get_def_value(), b.get_atk_value()), 'DEF', 'ATK'),
            (calc_distance(a.get_def_value(), b.get_def_value()), 'DEF', 'DEF')
        ]

        d_max = d_list[0]
        for i in range(1, len(d_list)):
            if d_list[i][0] > d_max[0]:
                d_max = d_list[i]

        return d_max


if __name__ == '__main__':
    coach_list = []

    data = xlrd.open_workbook('实况足球手游教练信息.xls')

    sheet = data.sheet_by_index(0)

    n_row = sheet.nrows
    n_coach = n_row - 2

    for i in range(2, n_row):
        row = sheet.row_values(i)
        coach = Coach(
            name=row[0],
            formation=row[1],
            atk_attack_style=row[2],
            atk_backfield_organization=row[3],
            atk_attack_area=row[4],
            atk_position_style=row[5],
            atk_defense_style=row[6],
            atk_defense_area=row[7],
            atk_scramble_style=row[8],
            def_attack_style=row[9],
            def_backfield_organization=row[10],
            def_attack_area=row[11],
            def_position_style=row[12],
            def_defense_style=row[13],
            def_defense_area=row[14],
            def_scramble_style=row[15],
        )
        coach_list.append(coach)

    count = 0
    for i in range(n_coach - 1):
        for j in range(i + 1, n_coach):
            diff = calc_diff_between(coach_list[i], coach_list[j])
            if diff[0] == 7:
                count += 1
                print("{:2d}: {}({}-{}) VS {}({}-{})".format(
                    count,
                    coach_list[i].name,
                    coach_list[i].formation,
                    diff[1],
                    coach_list[j].name,
                    coach_list[j].formation,
                    diff[2]
                ))
    pass
