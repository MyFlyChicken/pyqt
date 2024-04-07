import re
import struct
import os
import sys
import zlib
import time
from deal.dsp_cfg_Packet import dsp_cfg_Packet
from deal.dsp_cfg_rbl import MyPacket

def extract_comment_number(data_string):
    pattern = r'/\*\s\((\d+)\)\s.*\*/'
    match = re.search(pattern, data_string)
    
    if match:
        comment_number = int(match.group(1))
        return True, comment_number
    else:
        return False, -1

def count_bytes(data_string):
    # 分割字符串并去掉空格
    bytes_list = data_string.split(", ")

    # 检查最后一个元素是否为空字符串
    if bytes_list[-1] == "":
        bytes_list = bytes_list[:-1]

    # 计算字节的数量
    num_bytes = len(bytes_list)
    return num_bytes

def input_file_parse(input_file):
    steup = 0
    map_group = 0
    addr = 0
    data_offset = 0
    data_length = 0
    map_str = ""
    dsp_string = ""
    numbers = 0
    map = []
    packed_data = []

    pattern = r"Delay"

    with open(input_file, "r") as file:
        file_contents = file.readlines()

    
    for line in file_contents:
        line = line.strip()  # 去除行首和行尾的空格和换行符
        if line.startswith("0x"):
            has_number, number = extract_comment_number(line)
            hex_values = re.findall(r'0x([A-Fa-f0-9]+)(?:\s*,\s*/\*.+\*/)?', line)
            match = re.search(pattern, line)
            if has_number:
                map_group += 1
                #加上reg_data_length                
                data_offset = data_offset + data_length + 2 # 偏移+长度+地址占用的2字节
                #清除之前复位len
                if 1234 == steup:                    
                    map.append(data_length)
                    packed_data = struct.pack('<H', map[0]) + struct.pack('<I', map[1]) + struct.pack('<H', map[2])
                    map_str += packed_data.hex()
                    map.clear()
                    data_length = 0
                    steup = 0
                reg_addr = int(''.join(hex_values), 16)
                if match:
                    reg_addr = 0xFFFF
                map.append(reg_addr)
                map.append(data_offset)
                
            else:
                steup = 1234
                line_sizes = count_bytes(line) #获取字节数
                data_length = line_sizes + data_length #累加字节数
            
            hex_values_str = ''.join(hex_values)
            dsp_string += hex_values_str  # 去除"0x"前缀
    dsp_string = dsp_string.replace(" ", "").replace("\n", "").replace("\t", "")

    map.append(data_length)
    packed_data = struct.pack('<H', map[0]) + struct.pack('<I', map[1]) + struct.pack('<H', map[2])
    map_str += packed_data.hex()
    
    return map_group, map_str, dsp_string

def hex_to_bin_file(input_file_path, generat_file_path, outname,
    _type, _algo, _algo2, _part, _fwver, _productcode):
    dsp_group_dat = bytearray()
    dsp_cfg_data = bytearray()
    packet_data = bytearray
    output_file_data = bytearray()

    reg_map_group, reg_map_str, dsp_cfg_string = input_file_parse(input_file_path)    

    #寄存器组
    for i in range(0, len(reg_map_str), 2):
        hex_byte = reg_map_str[i:i+2]
        dsp_group_dat.append(int(hex_byte, 16))

    #实际DSP数据
    for i in range(0, len(dsp_cfg_string), 2):
        hex_byte = dsp_cfg_string[i:i+2]
        dsp_cfg_data.append(int(hex_byte, 16))
    
    grp_crc = zlib.crc32(dsp_group_dat)
    cfg_crc = zlib.crc32(dsp_cfg_data)    
    
    timestamp = int(time.time())
    packet = dsp_cfg_Packet("RBL", 0, 0, timestamp, _part, _fwver, _productcode, len(dsp_group_dat), grp_crc, len(dsp_cfg_data), cfg_crc)
    packet_data = packet.to_bin()
    print("===>>>dsp_cfg data creat<<<===")
    print(packet.algo)
    print(packet.algo2)
    print(packet.time_stamp)
    print(packet.part_name)
    print(packet.fw_ver)
    print(packet.prog_code)
    print(hex(packet.dsp_grp_crc))
    print(hex(packet.dsp_cfg_crc))
    print(packet.dsp_cfg_size)
    print(packet.dsp_grp_size)
    print(hex(packet.hdr_crc))

    print(len(packet_data))      

    #数据结合
    output_file_data.extend(packet_data)
    output_file_data.extend(dsp_group_dat)
    
    #填充剩余字节数
    padding_length = 1024 - len(output_file_data)
    for i in range(padding_length):
        output_file_data.append(0xFF)

    output_file_data.extend(dsp_cfg_data)

    print("===>>>dsp_cfg rbl creat<<<===")
    dsp_cfg_crc = zlib.crc32(output_file_data)
    dsp_cfg_size = len(output_file_data)
    dsp_cfg_rbl = MyPacket("RBL", 0, 0, timestamp, _part, _fwver, _productcode, dsp_cfg_crc, dsp_cfg_crc, dsp_cfg_size, dsp_cfg_size)    
        
    print(dsp_cfg_rbl.algo)
    print(dsp_cfg_rbl.algo2)
    print(dsp_cfg_rbl.time_stamp)
    print(dsp_cfg_rbl.part_name)
    print(dsp_cfg_rbl.fw_ver)
    print(dsp_cfg_rbl.prog_code)
    print(hex(dsp_cfg_rbl.pkg_crc))
    print(hex(dsp_cfg_rbl.raw_crc))
    print(dsp_cfg_rbl.raw_size)
    print(dsp_cfg_rbl.pkg_size)
    print(hex(dsp_cfg_rbl.hdr_crc))  

    tmpPath = generat_file_path + '/' + outname + ".bin"
    with open(tmpPath, "wb") as file:#dsp_cfg文件
        file.write(output_file_data)

    tmpPath = generat_file_path + '/' + outname + ".rbl"
    with open(tmpPath, "wb") as file:#dsp_cfg文件
        file.write(dsp_cfg_rbl.to_bin() +  output_file_data)
    