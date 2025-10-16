import pyautogui
import ctypes
import time

# 启用高 DPI 感知
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# 提示
print("5秒内将鼠标移到相应位置上...")
# 休眠5秒
time.sleep(5)
# 获取逻辑坐标
x, y = pyautogui.position()
# 打印逻辑坐标
print(f"适配缩放后的逻辑坐标: X={x}, Y={y}")
# 打印物理坐标
print(f"物理坐标: X={x*2}, Y={y*2}")