import asyncio
from bleak import BleakClient, BleakError

# DA14531设备的地址和特征UUID
DEVICE_ADDRESS = "80:EA:CA:70:00:04"
CHARACTERISTIC_UUID = "772ae37c-b3d2-4f8e-4042-5481d1e0098c"

# 文件路径
file_path = "ble_data.txt"

# 清空文件内容
with open(file_path, "w") as f:
    f.write("")

def calculate_values(data):
    """将20个字节拆分成10个电压值"""
    values = []
    for i in range(0, len(data), 2):
        pair = data[i:i+2]
        reversed_pair = pair[::-1]  # 倒序
        value = int.from_bytes(reversed_pair, byteorder='big')  # 计算值
        values.append(value)
    return values

async def notification_handler(sender, data):
    """处理接收到的通知"""
    values = calculate_values(data)
    with open(file_path, "a") as f:
        for value in values:
            f.write(f"{value}mV\n")

async def connect_and_listen():
    while True:
        try:
            async with BleakClient(DEVICE_ADDRESS) as client:
                await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
                print(f"Connected to {DEVICE_ADDRESS}, receiving notifications...")

                # 持续运行以接收通知
                while True:
                    await asyncio.sleep(1)
        except BleakError as e:
            print(f"Connection failed: {e}. Retrying...")

# 运行主程序
loop = asyncio.get_event_loop()
loop.run_until_complete(connect_and_listen())
