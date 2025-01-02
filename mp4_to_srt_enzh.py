import whisper
import os
from zhconv import convert  # 简繁体转换
from tqdm import tqdm
import imageio  # 用于获取视频时长
import os
os.system('cls')  # 清空屏幕


# 获取指定格式文件列表
def find_files(path, suffix):
    """
    获取 path 下所有指定后缀的文件
    """
    video_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.' + suffix):
                video_files.append(os.path.abspath(os.path.join(root, file)))
    return video_files


# 秒转时分秒毫秒
def seconds_to_hmsm(seconds):
    """
    将秒数转换为 SRT 格式时间戳
    """
    hours = str(int(seconds // 3600))
    minutes = str(int((seconds % 3600) // 60))
    seconds = seconds % 60
    milliseconds = str(int((seconds - int(seconds)) * 1000))  # 毫秒
    # 补零
    hours = hours.zfill(2)
    minutes = minutes.zfill(2)
    seconds = str(int(seconds)).zfill(2)
    milliseconds = milliseconds.zfill(3)
    return f"{hours}:{minutes}:{seconds},{milliseconds}"


# 获取视频时长
def get_video_duration(file_path):
    """
    获取视频文件的时长（秒）
    """
    video = imageio.get_reader(file_path)
    duration = video.get_meta_data()['duration']
    video.close()
    return duration


def main():
    # 主文件夹
    file_path = r'.'
    mp4_files = find_files(file_path, suffix='mp4')
    print('视频文件:', mp4_files)

    # 加载 Whisper 模型
    model = whisper.load_model('small')

    for file in tqdm(mp4_files):
        save_file = file[:-3] + "srt"
        if os.path.exists(save_file):
            print(f"{save_file} 已存在，跳过处理。")
            continue

        # 打印视频信息
        duration = get_video_duration(file)
        print(f"正在处理文件: {file} (时长: {seconds_to_hmsm(duration)})")

        # 获取中文转录
        res_zh = model.transcribe(file, task='transcribe', fp16=False, language='Chinese')
        # 获取英文翻译
        res_en = model.transcribe(file, task='translate', fp16=False)

        # 写入双字幕到 SRT 文件
        with open(save_file, 'w', encoding='utf-8') as f:
            i = 1
            for r_zh, r_en in zip(res_zh['segments'], res_en['segments']):
                f.write(f"{i}\n")
                f.write(f"{seconds_to_hmsm(r_zh['start'])} --> {seconds_to_hmsm(r_zh['end'])}\n")
                f.write(f"{convert(r_zh['text'], 'zh-cn')}\n")  # 中文转简体
                f.write(f"{r_en['text']}\n\n")  # 英文翻译
                i += 1

        print(f"完成处理文件: {file}")


if __name__ == "__main__":
    main()
