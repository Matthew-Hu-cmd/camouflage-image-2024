import os
import random
from PIL import Image
from tqdm import tqdm

# 文件路径
nc4k_dir = "/home/ac/data/2023/huyang/COD_Dataset/NC4K/Imgs"
coco_dir = "/home/ac/data/2023/huyang/COD_Dataset/cocotest2017"
output_dir = "/home/ac/data/2023/huyang/COD_Dataset/coco_NC4K"

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 获取NC4K/Imgs中的图片列表和尺寸
nc4k_images = os.listdir(nc4k_dir)
nc4k_images = [img for img in nc4k_images if img.endswith('.jpg')]

# 获取cocotest2017中的图片列表
coco_images = os.listdir(coco_dir)
coco_images = [img for img in coco_images if img.endswith('.jpg')]

# 随机选择和处理图片，并显示进度条
for nc4k_img_name in tqdm(nc4k_images, desc="Processing Images"):
    # 对应的NC4K图片路径
    nc4k_img_path = os.path.join(nc4k_dir, nc4k_img_name)

    # 打开NC4K图片并获取其尺寸
    with Image.open(nc4k_img_path) as nc4k_img:
        nc4k_size = nc4k_img.size

    # 从cocotest2017中随机选择一张图片
    coco_img_name = random.choice(coco_images)
    coco_img_path = os.path.join(coco_dir, coco_img_name)

    # 打开coco图片并调整其尺寸
    with Image.open(coco_img_path) as coco_img:
        resized_coco_img = coco_img.resize(nc4k_size)

        # 根据NC4K的文件名重命名coco图片
        output_img_path = os.path.join(output_dir, nc4k_img_name)

        # 保存调整后的图片
        resized_coco_img.save(output_img_path)

print("所有图片处理完成。")