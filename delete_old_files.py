import os
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
print("\033[1;44m------START OLD FILE DELETION------\033[0m")

# 创建一个文件处理程序
file_handler = logging.FileHandler('deletion_log.txt')
file_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(file_handler)

# 创建一个控制台处理程序
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

def delete_old_files(folder_paths, file_types, threshold_minutes=3):
    # 获取当前时间
    current_time = time.time()

    # 遍历指定文件夹下的所有文件
    for folder_path in folder_paths:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # 检查文件类型是否在指定的列表中，且距离上次修改超过阈值
            if any(filename.lower().endswith(file_type) for file_type in file_types) and \
                    os.path.isfile(file_path) and (current_time - os.path.getmtime(file_path)) > (threshold_minutes * 60):
                try:
                    # 删除文件
                    os.remove(file_path)
                    logging.info(f"Deleted: {file_path}")
                except Exception as e:
                    logging.error(f"Error deleting {file_path}: {str(e)}")


if __name__ == "__main__":
    # 指定文件夹路径列表
    folder_paths = ["static/upload", "static/download"]

    # 指定要处理的文件类型
    allowed_file_types = ['.pdf', '.zip']

    # 每隔一分钟扫描一次文件夹
    while True:
        delete_old_files(folder_paths, allowed_file_types)
        time.sleep(60)