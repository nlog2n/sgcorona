# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on January 25 09:48:12 2020
@author: nlog2n

  预处理数据

  python read_excel.py > singapore.imposm-geojson/singapore_corona.geojson

"""

import json
import xlrd

EXCEL_FILE_PATH = "rawdata.xlsx"


def read_rawdata():
    """
    read geo and properties data from excel file
    :return:
    """
    raw_data = []

    xlrd.Book.encoding = "utf8"
    workbook = xlrd.open_workbook(EXCEL_FILE_PATH)

    # 取第1张工作簿
    table = workbook.sheet_by_index(0)
    rows_count = table.nrows  # 取总行数
    for i in range(rows_count):
        if i == 0:  # column names
            continue

        caseno = table.cell(i, 0).value
        lat = table.cell(i, 1).value
        lon = table.cell(i, 2).value
        date = table.cell(i, 3).value
        age = table.cell(i, 4).value
        gender = table.cell(i, 5).value
        from_place = table.cell(i, 6).value
        staty_place = table.cell(i, 7).value
        visited_places = table.cell(i, 8).value
        related_cases = table.cell(i, 9).value
        status = table.cell(i,10).value

        caseno = int(caseno)
        lat, lon = float(lat), float(lon)
        age = int(age)

        properties = {
                "id": caseno,
                "date": date,
                "age": age,
                "gender": gender,
                "home": from_place,
                "stay": staty_place,
                "visited": visited_places,
                "related": related_cases,
                "status": status
        }

        geometry = {
                "type": "Point",
                "coordinates": [lon, lat]
        }

        jsonObj = {
            "type": "Feature",
            "properties": properties,
            "geometry": geometry
        }

        raw_data.append(jsonObj)

    geojsonObj = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": raw_data
    }

    return geojsonObj


if __name__ == '__main__':

    geojsonObj = read_rawdata()
    print(json.dumps(geojsonObj))
