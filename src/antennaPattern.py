import matplotlib
matplotlib.use('Agg')
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 读取两张图像
img_V = cv2.imread('cylindrical_monopole_V.jpg')
img_H = cv2.imread('cylindrical_monopole_H.jpg')

# 定义坐标系参数
time_max = 36  # 秒
power_max = 30  # dBm
power_min = -70  # dBm

# 分别处理V和H的数据
def process_image(img):
    # 转换为HSV色彩空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 定义红色的HSV范围
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    
    # 创建掩码提取红色曲线
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # 获取图像尺寸
    height, width = mask.shape
    
    # 存储时间和功率数据的列表
    times = []
    powers = []
    
    # 扫描每一列获取红色曲线的位置
    for x in range(width):
        red_points = np.where(mask[:, x] > 0)[0]
        if len(red_points) > 0:
            y = np.mean(red_points)
            time = (x / width) * time_max
            power = power_max - (y / height) * (power_max - power_min)
            times.append(time)
            powers.append(power)
    
    return times, powers

# 处理两张图像
times_V, powers_V = process_image(img_V)
times_H, powers_H = process_image(img_H)

# 将times转换为numpy数组
times_array_V = np.array(times_V)
times_array_H = np.array(times_H)

# 定义时间步长（秒）
time_step = 0.1

# 存储去抖动后的数据
filtered_times = []
filtered_powers_V = []
filtered_powers_H = []

# 改进的去抖动算法
window_size = 5  # 滑动窗口大小
threshold = 10   # 与窗口平均值的最大允许偏差
smooth_window = 1  # 平滑窗口大小

# 初始化第一个窗口的数据
current_time = min(times_V[0], times_H[0])
end_time = max(times_V[-1], times_H[-1])

while current_time <= end_time:
    # 找到最接近当前时间的数据点
    closest_idx_V = np.abs(times_array_V - current_time).argmin()
    closest_idx_H = np.abs(times_array_H - current_time).argmin()
    
    # 如果是初始化窗口
    if len(filtered_powers_V) < window_size:
        filtered_times.append(current_time)
        filtered_powers_V.append(powers_V[closest_idx_V])
        filtered_powers_H.append(powers_H[closest_idx_H])
    else:
        # 计算前window_size个有效值的平均值
        window_mean_V = np.mean(filtered_powers_V[-window_size:])
        window_mean_H = np.mean(filtered_powers_H[-window_size:])
        
        # 如果当前值与窗口平均值的差异在阈值内，则保留该值
        if (abs(powers_V[closest_idx_V] - window_mean_V) < threshold and 
            abs(powers_H[closest_idx_H] - window_mean_H) < threshold):
            filtered_times.append(current_time)
            filtered_powers_V.append(powers_V[closest_idx_V])
            filtered_powers_H.append(powers_H[closest_idx_H])
    
    current_time = round(current_time + time_step, 2)

# 应用移动平均平滑处理
def smooth_data(data, window_size):
    kernel = np.ones(window_size) / window_size
    return np.convolve(data, kernel, mode='same')

# 平滑处理功率数据
filtered_powers_V = smooth_data(filtered_powers_V, smooth_window)
filtered_powers_H = smooth_data(filtered_powers_H, smooth_window)

# 生成CSV文件
data = {
    'Time(s)': filtered_times, 
    'Power_V(dBm)': [round(p, 2) for p in filtered_powers_V],
    'Power_H(dBm)': [round(p, 2) for p in filtered_powers_H]
}
df = pd.DataFrame(data)
df.to_csv('antenna_data.csv', index=False)

# 创建极坐标图
plt.figure(figsize=(10, 10))
ax = plt.subplot(111, projection='polar')

# 转换为角度（0-360度）
angles = np.array(filtered_times) * (360 / time_max)
angles_rad = np.radians(angles)

# 绘制两条曲线
ax.plot(angles_rad, filtered_powers_V, label='Vertical')
ax.plot(angles_rad, filtered_powers_H, label='Horizontal')

ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')
ax.set_title('Antenna Pattern (Polar)')
ax.grid(True)
ax.legend()

# 设置径向标签
ax.set_rgrids([-30, -20, -10, 0, 10, 20, 30], 
              labels=['-30dBm', '-20dBm', '-10dBm', 
                     '0dBm', '10dBm', '20dBm', '30dBm'])

plt.savefig('antenna_pattern2.png')
plt.close()
