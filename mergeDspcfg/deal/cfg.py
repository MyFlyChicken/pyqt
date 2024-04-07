import os
import json


def creat_cfg(bin1_path, output_path, name,
_type, _algo, _algo2, _part, _fwver, _productcode):
    cfg_json = '{"name": "merge","Source": {"datPath":"","generatPath":""},"RBL": {"type": "RBL","algo": "","algo2": "","part": "","fw_version": "","product_code": ""},"generatName":""}'
    data = json.loads(cfg_json)
    data["name"] = "dspCfg"
    data["Source"]["datPath"] = bin1_path
    data["Source"]["generatPath"] = output_path
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

