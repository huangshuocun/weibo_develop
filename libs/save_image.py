import os
from hashlib import md5

def save_image(image_file):
    '''保存头像文件'''
    # 读取文件的二进制数据
    file_bin_data = image_file.stream.read()

    # 文件指针归零
    image_file.stream.seek(0)

    # 计算文件的 md5 值
    filename = md5(file_bin_data).hexdigest()

    # 获取项目文件夹的绝对路径
    base_dir = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

    # 文件绝对路径
    filepath = os.path.join(base_dir, 'static', 'upload', filename)

    # 保存文件
    image_file.save(filepath)

    # 文件的 URL
    image_url = f'/static/upload/{filename}'

    return image_url
