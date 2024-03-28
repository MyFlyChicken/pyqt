import os
import json


def creat_cfg(bin1_path, bin1_start, bin1_end, bin2_path, bin2_start, bin2_end, bin3_path, bin3_start, bin3_end, output_path, name,
_type, _algo, _algo2, _part, _fwver, _productcode):
    cfg_json = '{"name": "merge","Source": {"bootPath":"","bootOffset":0,"bootLen":0,"appPath":"","appOffset":0,"appLen":0,"generatPath":"","factoryOffset":0,"factoryLen":0},"RBL": {"type": "RBL","algo": "","algo2": "","part": "","fw_version": "","product_code": ""},"generatName":""}'
    data = json.loads(cfg_json)
    data["name"] = "merge"
    data["Source"]["bootPath"] = bin1_path
    data["Source"]["bootOffset"] = bin1_start
    data["Source"]["bootLen"] = bin1_end
    data["Source"]["appPath"] = bin2_path
    data["Source"]["appOffset"] = bin2_start
    data["Source"]["appLen"] = bin2_end
    data["Source"]["generatPath"] = bin3_path
    data["Source"]["factoryOffset"] = bin3_start
    data["Source"]["factoryLen"] = bin2_end
    data["RBL"]["type"] = _type
    data["RBL"]["algo"] = _algo
    data["RBL"]["algo2"] = _algo2
    data["RBL"]["part"] = _part
    data["RBL"]["fw_version"] =_fwver 
    data["RBL"]["product_code"] = _productcode
    data["generatName"] = name
    return data


def read_json_from_file(file_path):
    with open(file_path) as file:
        json_data = json.load(file)
    return json_data

def write_json_to_file(file_path, json_data):
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

