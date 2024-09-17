import os
from tqdm import tqdm
from PIL import Image
import numpy as np
from camouflage_image import ImageCamouflager
from file_handler import FileHandler

# 文件路径
foreground_dir = "/home/ac/data/2023/huyang/COD_Dataset/NC4K/Foreground"
background_dir = "/home/ac/data/2023/huyang/COD_Dataset/coco_NC4K"
output_dir = "result/NC4K-917"

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 初始化FileHandler和ImageCamouflager
file_handler = FileHandler()
camouflager = ImageCamouflager()

# 获取Foreground和Background文件夹中的图片列表，并按字母顺序排序
foreground_images = sorted([f for f in os.listdir(foreground_dir) if f.endswith('.png')])
background_images = sorted([f for f in os.listdir(background_dir) if f.endswith('.jpg')])

# 确保文件数量相等，防止遗漏或匹配错误
if len(foreground_images) != len(background_images):
    print("警告：前景图和背景图的数量不一致，请检查文件夹内容。")
else:
    print("前景图与背景图数量一致，开始处理。")

# 批量合成并保存结果，并显示进度条
for fg_image, bg_image in tqdm(zip(foreground_images, background_images), desc="Processing Images", total=len(foreground_images)):
    # 检查文件名前缀是否匹配，确保图片对齐
    fg_name, _ = os.path.splitext(fg_image)
    bg_name, _ = os.path.splitext(bg_image)

    if fg_name != bg_name:
        print(f"Skipping due to mismatched file names: {fg_image} and {bg_image}")
        continue

    foreground_image_path = os.path.join(foreground_dir, fg_image)
    background_image_path = os.path.join(background_dir, bg_image)

    try:
        # 读取图像
        foreground = file_handler.read(foreground_image_path, alpha=True)
        background = file_handler.read(background_image_path, colors=True)

        # 合成图像
        result = camouflager.camouflage(background, foreground)

        # 检查合成结果是否有效
        if result is None:
            print(f"Skipping {fg_name} due to texture correction failure.")
            continue

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
        output_path = os.path.join(output_dir, fg_name + "_camouflaged.png")
        result_image.save(output_path)

    except Exception as e:
        print(f"Error processing {fg_name}: {e}")
        continue  # 如果有任何错误，跳过当前图像

print("所有图片处理完成。")