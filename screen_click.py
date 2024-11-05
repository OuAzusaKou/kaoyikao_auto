import pyautogui
import time
import keyboard


def show_mouse_position():
    """显示当前鼠标位置，按空格记录位置"""
    positions = []  # 存储记录的位置
    try:
        print("移动鼠标查看位置，按空格记录位置，按 Ctrl+C 退出")
        while True:
            x, y = pyautogui.position()
            position_str = f"当前鼠标位置: X: {x}, Y: {y} | 已记录位置数: {len(positions)}"
            print(position_str, end='\r')
            
            # 检测空格键是否按下
            if keyboard.is_pressed('space'):
                positions.append((x, y))
                print(f"\n已记录位置点 {len(positions)}: X: {x}, Y: {y}")
                time.sleep(0.3)  # 防止一次按键多次记录
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n记录的位置点:")
        for i, pos in enumerate(positions, 1):
            print(f"位置 {i}: X: {pos[0]}, Y: {pos[1]}")
        
        # 保存位置到文件
        with open('mouse_positions.txt', 'w', encoding='utf-8') as f:
            for pos in positions:
                f.write(f"{pos[0]},{pos[1]}\n")
        print(f"\n位置已保存到 mouse_positions.txt")
        print("退出程序")

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
