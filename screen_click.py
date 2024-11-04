import pyautogui
import time


def show_mouse_position():
    """显示当前鼠标位置"""
    try:
        while True:
            x, y = pyautogui.position()
            position_str = f"当前鼠标位置: X: {x}, Y: {y}"
            print(position_str, end='\r')
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n退出程序")

def simulate_click(x, y):
    """模拟屏幕点击"""
    pyautogui.click(x, y)
    print(f"已在位置 (X: {x}, Y: {y}) 模拟点击")

if __name__ == "__main__":
    print("1. 显示鼠标位置")
    print("2. 模拟屏幕点击")
    choice = input("请选择功能 (1/2): ")

    if choice == '1':
        show_mouse_position()
    elif choice == '2':
        x = int(input("请输入要点击的 X 坐标: "))
        y = int(input("请输入要点击的 Y 坐标: "))
        simulate_click(x, y)
    else:
        print("无效的选择")
