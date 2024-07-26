import matplotlib.pyplot as plt
import numpy as np

# 文件路径
file_path = "ble_data.txt"

def read_data(file_path):
    """读取txt文件中的数据"""
    with open(file_path, "r") as f:
        lines = f.readlines()
    data = [int(line.strip().replace("mV", "")) for line in lines]
    return data

def plot_data(data):
    """绘制数据曲线图"""
    plt.figure(figsize=(10, 5))
    plt.plot(data, marker='o', linestyle='-', color='b')
    plt.title('BLE Data Curve')
    plt.xlabel('Sample Number')
    plt.ylabel('Value (mV)')
    plt.grid(True)
    plt.show()

# 用来检验采样频率
def plot_fft(data, sampling_rate=1000):
    """绘制数据的FFT曲线图"""
    N = len(data)
    T = 1.0 / sampling_rate
    yf = np.fft.fft(data)
    xf = np.fft.fftfreq(N, T)[:N//2]

    plt.figure(figsize=(10, 5))
    plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))
    plt.title('FFT of BLE Data')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

# 读取数据
data = read_data(file_path)

# 绘制数据曲线图
plot_data(data)

# 绘制FFT曲线图
plot_fft(data)
