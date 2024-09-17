import os
from tqdm import tqdm
from PIL import Image
import numpy as np
from camouflage_image import ImageCamouflager
from file_handler import FileHandler

# 文件路径
foreground_dir = "/home/ac/data/2023/huyang/COD_Dataset/NC4K/Foreground"
background_dir = "/home/ac/data/2023/huyang/COD_Dataset/coco_NC4K"
output_dir = "result/NC4K"

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 初始化FileHandler和ImageCamouflager
file_handler = FileHandler()
camouflager = ImageCamouflager()

# 获取Foreground和Background文件夹中的图片列表
foreground_images = [f for f in os.listdir(foreground_dir) if f.endswith('.png')]
background_images = [f for f in os.listdir(background_dir) if f.endswith('.jpg')]

# 获取公共图片名称
common_names = set([os.path.splitext(f)[0] for f in foreground_images]) & \
               set([os.path.splitext(f)[0] for f in background_images])

# 批量合成并保存结果，并显示进度条
for name in tqdm(common_names, desc="Processing Images"):
    foreground_image_path = os.path.join(foreground_dir, name + ".png")
    background_image_path = os.path.join(background_dir, name + ".jpg")

    # 读取图像
    foreground = file_handler.read(foreground_image_path, alpha=True)
    background = file_handler.read(background_image_path, colors=True)

    # 合成图像
    result = camouflager.camouflage(background, foreground)

    # 检查图像通道数并选择模式
    if result.shape[2] == 4:  # 如果是4个通道，使用RGBA
        # 转换为 RGBA 图像（假设 result 是 BGRA）
        result = result[:, :, [2, 1, 0, 3]]  # 交换 BGR -> RGB
        result_image = Image.fromarray(result.astype(np.uint8), 'RGBA')
    elif result.shape[2] == 3:  # 如果是3个通道，使用RGB
        # 转换为 RGB 图像（假设 result 是 BGR）
        result = result[:, :, [2, 1, 0]]  # 交换 BGR -> RGB
        result_image = Image.fromarray(result.astype(np.uint8), 'RGB')
    else:
        raise ValueError(f"Unexpected number of channels in the image: {result.shape[2]}")

    # 保存结果
    output_path = os.path.join(output_dir, name + "_camouflaged.png")
    result_image.save(output_path)

    # 打印处理信息（可选）
    # print(f"Processed {name}.png and {name}.jpg, saved to {output_path}")

print("所有图片处理完成。")