import json
import pyautogui
import tkinter as tk
from pynput import keyboard
import os
from screen_click import simulate_click
from baidu_ocr import perform_ocr
from score_predict import predict_score
from zhipuai import ZhipuAI

from zhipu_ocr import zhipu_ocr_perform

pos_list = [
(1515,307),
(1573,315),
(1647,325),
(1711,320),
(1763,317),
(1830,321),
(1520,378),
(1571,382),
(1643,389)
]
class ScreenshotTool:
    def __init__(self,client):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-fullscreen', True)
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.start_x = None
        self.start_y = None
        self.cur_rect = None
        self.is_selecting = False
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        
        # 添加新的属性来存储分数窗口
        self.score_window = None
        
        # 添加新的属性来存储上次的截图区域
        self.last_region = None
        self.client = client
        
        # 添加自动截图控制变量
        self.auto_screenshot = False
        self.auto_screenshot_delay = 2000  # 2秒延迟
        
    def on_key_press(self, key):
        if key == keyboard.Key.f2:
            if not self.last_region:
                self.show_selection_window()
            else:
                if not self.auto_screenshot:
                    # 开始自动截图
                    self.auto_screenshot = True
                    self.schedule_auto_screenshot()
                else:
                    # 停止自动截图
                    self.auto_screenshot = False
                    print("自动截图已停止")
        elif key == keyboard.Key.f3:
            self.auto_screenshot = False  # 确保重置区域时也停止自动截图
            self.last_region = None
            print("截图区域已重置，下次将重新选择区域")
    
    def schedule_auto_screenshot(self):
        if self.auto_screenshot and self.last_region:
            self.take_screenshot_with_last_region()
            # 安排下一次截图
            self.root.after(self.auto_screenshot_delay, self.schedule_auto_screenshot)
    
    def take_screenshot_with_last_region(self):
        x1, y1, x2, y2 = self.last_region
        screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
        screenshot.save("screenshot.png")
        print("使用上次区域截图已保存为 screenshot.png")
        
        perform_ocr("screenshot.png")
        # 调用zhipu_ocr
        zhipu_ocr_result = zhipu_ocr_perform("screenshot.png",self.client)
        # 将结果追加至orc_results.json
        with open('ocr_results.json', 'r',encoding='utf-8') as f:
            data = json.load(f)
        data['zhipu_results']=zhipu_ocr_result
        with open('ocr_results.json', 'w',encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        # 调用评分功能
        score = predict_score(self.client)
        
        x,y = pos_list[int(score)]

        simulate_click(x, y)
        # 显示分数
        # self.show_score(score)
    
    def show_selection_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.is_selecting = False
        if self.cur_rect:
            self.canvas.delete(self.cur_rect)
            self.cur_rect = None
    
    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.is_selecting = True
        
    def on_drag(self, event):
        if not self.is_selecting:
            return
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        
        if self.cur_rect:
            self.canvas.delete(self.cur_rect)
        
        self.cur_rect = self.canvas.create_rectangle(self.start_x, self.start_y, cur_x, cur_y, outline='red')
        
    def on_release(self, event):
        if not self.is_selecting:
            return
        self.is_selecting = False
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        
        x1 = int(min(self.start_x, end_x))
        y1 = int(min(self.start_y, end_y))
        x2 = int(max(self.start_x, end_x))
        y2 = int(max(self.start_y, end_y))
        
        # 保存当前区域
        self.last_region = (x1, y1, x2, y2)
        
        self.root.withdraw()
        
        # 使用pyautogui进行截图
        screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
        
        # 保存截图
        screenshot.save("screenshot.png")
        
        print("截图已保存为 screenshot.png")
        
        # 调用OCR功能
        perform_ocr("screenshot.png")
        # 调用zhipu_ocr
        zhipu_ocr_result = zhipu_ocr_perform("screenshot.png",self.client)
        # 将结果追加至orc_results.json
        with open('ocr_results.json', 'r',encoding='utf-8') as f:
            data = json.load(f)
        data['zhipu_results']=zhipu_ocr_result
        with open('ocr_results.json', 'w',encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        # 调用评分功能
        score = predict_score(self.client)
        print('score',score)
        x,y = pos_list[int(score)]
        simulate_click(x, y)
        # 显示分数
        # self.show_score(score)


        
        # 可选：打开保存的图片
        # os.startfile("screenshot.png")
    
    def show_score(self, score):
        if self.score_window:
            self.score_window.destroy()
        
        self.score_window = tk.Toplevel()
        self.score_window.title("分数")
        self.score_window.geometry("200x100+{}+{}".format(
            self.root.winfo_screenwidth() - 220, 
            int(self.root.winfo_screenheight() / 2) - 50
        ))
        self.score_window.attributes('-topmost', True)
        
        label = tk.Label(self.score_window, text=f"预测分数: {score}", font=("Arial", 16))
        label.pack(expand=True)
        
    def run(self):
        self.root.withdraw()
        self.root.mainloop()

if __name__ == "__main__":
    client = ZhipuAI(api_key="c1a70a187972b988ece0deb79be8ca0f.E5Bd5ODqZb7ozak0")
    tool = ScreenshotTool(client)
    tool.run()
