import os
import zipfile
import io
path = r'D:\code\web_explorer\backend\t\data'
buffer = io.BytesIO()
zip = zipfile.ZipFile('./d1.zip', "w", zipfile.ZIP_DEFLATED)
for root, dirnames, filenames in os.walk(path):
    file_path = root.replace(path, '')  # 去掉根路径，只对目标文件夹下的文件及文件夹进行压缩
    # print(root,path)
    # print(file_path)
    # 循环出一个个文件名
    for filename in filenames:
        # current_path = os.path.join(root)
        # with open()
        print(os.path.join(root, filename))
        print(os.path.join('increase',filename, filename))
        zip.write(os.path.join(root, filename), os.path.join('increase',filename, filename))
zip.close()

