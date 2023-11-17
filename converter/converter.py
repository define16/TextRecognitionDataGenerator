import os
import shutil
import json

def move_image_files(rootdir, index):
    file_mapping = {}
    for it in os.scandir(rootdir):
        if it.is_dir():
            index = move_image_files(it, index)
        else:
            if it.name.endswith(".jpg"):
                shutil.move(it.path, f'/home/sagemaker-user/data_set/ko/images/image_{index}.jpg')
                file_mapping[it.name] = f"image_{index}.jpg"
                index += 1
                if index % 1000 == 0:
                    print(f"{index} 진행중")
    if file_mapping:
        with open(os.path.join(rootdir, "file_mapping.json"), 'w') as outfile:
            json.dump(file_mapping, outfile)

    return index

def read_mapping_files(rootdir):
    file_list = []
    for it in os.scandir(rootdir):
        if it.name[0] == ".":
            continue
        if it.is_dir():
            sub_file_list = read_mapping_files(it)
            file_list.extend(sub_file_list)
        else:
            if file.endswith(".json") or file.endswith(".txt"):
                file_list.append(it.path)

    return file_list


# /home/sagemaker-user/TextRecognitionDataGenerator/trdg
# 파일 옮기기
index = 0
file_count = move_image_files(os.path.join("/", "home", "sagemaker-user", "TextRecognitionDataGenerator", "out"), index)
print(file_count)

# 매핑정보 생성
file_list = read_mapping_files(os.path.join("/", "home", "sagemaker-user", "TextRecognitionDataGenerator", "out"))
file_mapping = {}
labeling = {}
for file in file_list:
    if file.endswith(".json"):
        with open(file, 'r') as f:
            data = json.load(f)
            file_mapping["/".join(file.split("/")[:-1])] = data
    if file.endswith(".txt"):
        l = {}
        with open(file, 'r') as f:
            while True:
                line = f.readline()
                if not line: break
                data = line.split(" ")
                l[data[0]] = data[1].strip()
        labeling["/".join(file.split("/")[:-1])] = l

# gt.txt 생성
gt = []
for path, files in file_mapping.items():
    print(path)
    for old, new in files.items():
        gt.append(f"{new}\t{labeling.get(path).get(old).strip()}\n")
print(gt[700:1000])

with open("/home/sagemaker-user/data_set/ko/gt.txt", 'w') as f:
    for g in gt:
        f.write(g)