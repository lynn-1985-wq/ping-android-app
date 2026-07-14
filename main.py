from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import mainthread
import subprocess
import threading
import os
from datetime import datetime

PING_COUNT = 1
PING_TIMEOUT = 1

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 8
        self.is_working = False

        self.label_ip = Label(text="IP列表（一行一个）", size_hint_y=0.06)
        self.ip_input = TextInput(
            hint_text="192.168.1.1\n192.168.1.100",
            size_hint_y=0.22,
            font_size=14
        )

        btn_layout = BoxLayout(size_hint_y=0.09, spacing=6)
        self.btn_start = Button(text="开始检测")
        self.btn_clear = Button(text="清空日志")
        self.btn_save = Button(text="保存日志")

        self.btn_start.bind(on_press=self.start_task)
        self.btn_clear.bind(on_press=self.clear_log)
        self.btn_save.bind(on_press=self.save_log)

        btn_layout.add_widget(self.btn_start)
        btn_layout.add_widget(self.btn_clear)
        btn_layout.add_widget(self.btn_save)

        self.label_log = Label(text="检测日志", size_hint_y=0.06)
        scroll = ScrollView(size_hint_y=0.57)
        self.log_view = TextInput(readonly=True, font_size=13)
        scroll.add_widget(self.log_view)

        self.add_widget(self.label_ip)
        self.add_widget(self.ip_input)
        self.add_widget(btn_layout)
        self.add_widget(self.label_log)
        self.add_widget(scroll)

    def ping(self, ip):
        try:
            cmd = ["ping", "-c", str(PING_COUNT), "-W", str(PING_TIMEOUT), ip]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=PING_TIMEOUT+2)
            return res.returncode == 0
        except Exception:
            return False

    @mainthread
    def add_log(self, text):
        t = datetime.now().strftime("%H:%M:%S")
        self.log_view.text += f"[{t}] {text}\n"

    def clear_log(self, instance):
        self.log_view.text = ""

    def task_loop(self):
        self.is_working = True
        self.btn_start.disabled = True

        data = self.ip_input.text.strip()
        if not data:
            self.add_log("错误：未填写IP地址！")
            self.is_working = False
            self.btn_start.disabled = False
            return

        ip_list = data.splitlines()
        self.add_log("===== 开始批量检测 =====")
        for ip in ip_list:
            ip = ip.strip()
            if not ip:
                continue
            status = self.ping(ip)
            if status:
                self.add_log(f"{ip} 连通 ✅")
            else:
                self.add_log(f"{ip} 断开 ❌")
        self.add_log("===== 本轮检测结束 =====\n")

        self.is_working = False
        self.btn_start.disabled = False

    def start_task(self, instance):
        if self.is_working:
            self.add_log("提示：正在检测，请等待完成！")
            return
        t = threading.Thread(target=self.task_loop, daemon=True)
        t.start()

    def save_log(self, instance):
        content = self.log_view.text.strip()
        if not content:
            self.add_log("提示：日志为空，无需保存")
            return
        try:
            filename = "ping_log.txt"
            path = f"/storage/emulated/0/Download/{filename}"
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.add_log(f"✅ 日志保存成功 {path}")
        except Exception as e:
            self.add_log(f"❌ 保存失败：{str(e)}")


class PingApp(App):
    def build(self):
        self.title = "IP Ping检测工具"
        return MainLayout()


if __name__ == "__main__":
    PingApp().run()