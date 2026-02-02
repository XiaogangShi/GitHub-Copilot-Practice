import numpy as np
import os
import subprocess

# 音效参数：1秒时长，切水果清脆声
sample_rate = 44100  # 标准采样率
duration = 1.0       # 1秒时长
amplitude = 32767    # 16位音频最大值
n_channels = 1       # 单声道
sample_width = 2     # 16位深度

# 生成1秒的混合声波（切水果质感）
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
# 主切割音（2000Hz，缓慢衰减适配1秒）
main_tone = amplitude * np.sin(2 * np.pi * 2000 * t) * np.exp(-t * 5)
# 高频泛音（增强清脆感）
overtone = amplitude * 0.3 * np.sin(2 * np.pi * 4500 * t) * np.exp(-t * 8)
# 轻微噪音（模拟果肉摩擦）
noise = amplitude * 0.1 * np.random.randn(len(t)) * np.exp(-t * 4)
# 混合并限制范围（避免失真）
sound = main_tone + overtone + noise
sound = np.clip(sound, -amplitude, amplitude).astype(np.int16)

# ========== 修复核心：标准WAV文件头构造 ==========
wav_file = "temp_cut_fruit_1s.wav"
with open(wav_file, 'wb') as f:
    # 1. RIFF Chunk
    f.write(b'RIFF')  # ChunkID
    data_size = len(sound) * n_channels * sample_width
    riff_size = 36 + data_size  # ChunkSize = 36 + 数据大小
    f.write(riff_size.to_bytes(4, 'little'))
    f.write(b'WAVE')  # Format

    # 2. fmt Chunk
    f.write(b'fmt ')  # Subchunk1ID
    f.write((16).to_bytes(4, 'little'))  # Subchunk1Size (PCM格式固定16)
    f.write((1).to_bytes(2, 'little'))   # AudioFormat (PCM=1)
    f.write(n_channels.to_bytes(2, 'little'))  # NumChannels
    f.write(sample_rate.to_bytes(4, 'little'))  # SampleRate
    byte_rate = sample_rate * n_channels * sample_width  # ByteRate
    f.write(byte_rate.to_bytes(4, 'little'))
    block_align = n_channels * sample_width  # BlockAlign
    f.write(block_align.to_bytes(2, 'little'))
    f.write((16).to_bytes(2, 'little'))  # BitsPerSample (16位)

    # 3. Data Chunk（修复no 'data' tag问题的关键）
    f.write(b'data')  # Subchunk2ID
    f.write(data_size.to_bytes(4, 'little'))  # Subchunk2Size
    f.write(sound.tobytes())  # 音频数据

# 用ffmpeg转换为MP3（128kbps，单声道）
mp3_file = "cut_fruit_sound_1s.mp3"
result = subprocess.run([
    'ffmpeg', '-y', '-i', wav_file,
    '-b:a', '128k', '-ac', '1', mp3_file
], capture_output=True, text=True)

# 清理临时文件
os.remove(wav_file)

# 验证生成结果
if os.path.exists(mp3_file) and os.path.getsize(mp3_file) > 0:
    file_size = os.path.getsize(mp3_file) / 1024  # 转为KB
    print(f"✅ 1秒切水果音效生成成功！")
    print(f"📄 文件路径：{os.path.abspath(mp3_file)}")
    print(f"📏 文件大小：{file_size:.2f} KB")
else:
    print("❌ 生成失败，ffmpeg输出：")
    print(result.stderr)