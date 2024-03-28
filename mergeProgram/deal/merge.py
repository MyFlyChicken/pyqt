import os
import sys
import zlib
import time
from deal.creat_rbl import MyPacket

def get_file_crc_and_size(file_path):
    # 计算文件的 CRC32 校验和
    with open(file_path, "rb") as f:
        file_data = f.read()
        crc = zlib.crc32(file_data)

    # 获取文件的大小
    file_size = len(file_data)

    return crc, file_size

def prepend_to_bin_file(packet, dst_path, file_name, src_path):
    # 将 MyPacket 对象转换为二进制数据
    packet_data = packet.to_bin()

    # 读取已有的二进制文件
    with open(src_path, "rb") as f:
        existing_data = f.read()

    # 将 MyPacket 的二进制数据追加到已有的二进制数据的开头
    new_data = packet_data + existing_data

    # 将追加后的数据写入文件
    dst_path = dst_path +'/' +file_name + ".rbl"
    with open(dst_path, "wb") as f:
        f.write(new_data)
    return dst_path


def merge_files(bin1_path, bin1_offset, bin1_len, bin2_path, bin2_offset, bin2_len, bin3_path, bin3_offset, bin3_len, output_path, out_name):
    # 读取第一个二进制文件
    with open(bin1_path, 'rb') as f1:
        data1 = f1.read()

    # 读取第二个二进制文件
    with open(bin2_path, 'rb') as f2:
        data2 = f2.read()

    # 读取第三个二进制文件
    with open(bin3_path, 'rb') as f3:
        data3 = f3.read()

    data3_back = data3
    # 确定合并后的总长度
    total_len = len(data1) + len(data2) + len(data3)

    # 对于大小不足终止地址的文件，填充0xFF
    if len(data1) < bin1_len:
        data1 += b'\xFF' * (bin1_len - len(data1))
    if len(data2) < bin2_len:
        data2 += b'\xFF' * (bin2_len - len(data2))
    if len(data3) < bin3_len:
        data3 += b'\xFF' * (bin3_len - len(data3))

    # 将三个二进制文件合并为一个文件
    data = data1 + data2 + data3

    # 将合并后的数据写入输出文件
    output_path = output_path + '/' + out_name + ".bin"
    with open(output_path, 'wb') as f4:
        f4.write(data)

    # new_path = os.path.join(os.path.dirname(output_path), out_name + ".rbl")
    # with open(new_path, 'wb') as f5:
    #     f5.write(data3_back)

def merge_running(bin1_path, bin1_offset, bin1_len, bin2_path, bin2_offset, bin2_len, bin3_path, bin3_offset, bin3_len, output_path, out_name,
_type, _algo, _algo2, _part, _fwver, _productcode, merge_en):
    crc, file_size = get_file_crc_and_size(bin2_path)
    #print(crc, file_size)
    timestamp = int(time.time())
    #RBL必须为大写，qboot会校验这个字符串
    packet = MyPacket(_type, int(_algo), int(_algo2), timestamp, _part, _fwver, _productcode, crc, crc, file_size, file_size)
    print(packet.algo)
    print(packet.algo2)
    print(packet.time_stamp)
    print(packet.part_name)
    print(packet.fw_ver)
    print(packet.prog_code)
    print(hex(packet.pkg_crc))
    print(hex(packet.raw_crc))
    print(packet.raw_size)
    print(packet.pkg_size)
    print(hex(packet.hdr_crc))

    bin3_path = prepend_to_bin_file(packet, bin3_path, out_name, bin2_path)
    # 合并文件
    if merge_en==1 :
        merge_files(bin1_path, bin1_offset, bin1_len, bin2_path, bin2_offset, bin2_len, bin3_path, bin3_offset, bin3_len, output_path, out_name)    
    print("merge finished! ok")


    