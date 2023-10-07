import clr # the pythonnet module.
clr.AddReference(r'C:\Users\netwokz\Documents\CODE\workspace\python\statistics\OpenHardwareMonitorLib') 
# e.g. clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib'), without .dll

from OpenHardwareMonitor import Hardware

def get_methods(data):
    list_of_methods = dir(data)
    if len(list_of_methods) > 0:
        for method in list_of_methods:
            print(method)

def get_sensors(item):
    for sensor in item:
        print(f"[{sensor.Name}], [{sensor.SensorType.ToString()}], [{sensor.Value}]")

def get_hardware():
    # Hardware.Mainboard.Mainboard
    # Hardware.CPU.AMD17CPU
    # Hardware.RAM.GenericRAM
    # Hardware.ATI.ATIGPU
    # Hardware.HDD.SSDMicron
    # Hardware.HDD.GenericHarddisk
    # Hardware.HDD.GenericHarddisk
    for i in c.Hardware: 
        print(i)

def get_all_sensors():
    c = Hardware.Computer()
    c.MainboardEnabled = True
    c.CPUEnabled = True
    c.GPUEnabled = True
    c.RAMEnabled = True
    c.HDDEnabled = True
    c.Open()
    
    CPU = c.Hardware[1]
    CPU.Update()
    cpu_temp = ''
    cpu_load = ''
    # get_sensors(CPU.Sensors) 
    for sensor in CPU.Sensors:
        if sensor.Name == "CPU Package" and sensor.SensorType.ToString() == "Temperature":
            cpu_temp = str(int(sensor.get_Value()))
        if sensor.Name == "CPU Total" and sensor.SensorType.ToString() == "Load":
            cpu_load = str(int(sensor.get_Value()))

    MEM = c.Hardware[2]
    MEM.Update()
    mem_used = ''
    mem_avail = ''
    # get_sensors(MEM.Sensors)
    for sensor in MEM.Sensors:
        if sensor.Name == "Used Memory" and sensor.SensorType.ToString() == "Data":
            mem_used = str(int(sensor.get_Value()))
        if sensor.Name == "Available Memory" and sensor.SensorType.ToString() == "Data":
            mem_avail = str(int(sensor.get_Value()))

    GPU = c.Hardware[3]
    GPU.Update()
    gpu_temp = ''
    gpu_power_draw = ''
    # get_sensors(GPU.Sensors)
    for sensor in GPU.Sensors:
        if sensor.Name == "GPU Core" and sensor.SensorType.ToString() == "Temperature":
            gpu_temp = str(int(sensor.get_Value()))
        if sensor.Name == "GPU Total" and sensor.SensorType.ToString() == "Power":
            gpu_power_draw = str(int(sensor.get_Value()))
    c.Close()
    return cpu_temp, cpu_load, mem_used, mem_avail, gpu_temp, gpu_power_draw
    # print(f"CPU Temp:  {cpu_temp}°C")
    # print(f"CPU Load:  {cpu_load}%")
    # print(f"MEM Used:  {mem_used}GB")
    # print(f"MEM Avail: {mem_avail}GB")
    # print(f"GPU Temp:  {gpu_temp}°C")
    # print(f"GPU Draw:  {gpu_power_draw}W")


from tkinter import *
from tkinter import ttk
import customtkinter
from ctypes import windll
from time import sleep
from datetime import datetime

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

def set_appwindow(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
    # re-assert the new window style
    root.withdraw()
    root.after(10, root.deiconify)

def main():
    root = customtkinter.CTk() 
    cpu_temp_label = customtkinter.CTkLabel(root, text_color="#3B8ED0") 
    cpu_temp_label.pack() 
    gpu_temp_label = customtkinter.CTkLabel(root, text_color="#3B8ED0")  
    gpu_temp_label.pack() 
    # cpu_load_label = customtkinter.CTkLabel(root) 
    # cpu_load_label.pack() 
    # mem_used_label = customtkinter.CTkLabel(root) 
    # mem_used_label.pack() 
    # mem_avail_label = customtkinter.CTkLabel(root) 
    # mem_avail_label.pack() 
    # gpu_power_draw_label = customtkinter.CTkLabel(root) 
    # gpu_power_draw_label.pack() 
    
    # style = ttk.Style()
    # style.theme_use('clam') 
    # style.configure("dark.Horizontal.TProgressbar", background="red", troughcolor ='#404040')
    
    cpu_usage= customtkinter.CTkProgressBar(master=root, orientation= HORIZONTAL, width=100)
    cpu_usage.pack()
    mem_usage= customtkinter.CTkProgressBar(master=root, orientation= HORIZONTAL, width=100)
    mem_usage.pack()
    
    def update_labels():
        cpu_temp, cpu_load, mem_used, mem_avail, gpu_temp, gpu_power_draw = get_all_sensors()
        cpu_temp_label.configure(text=f"CPU: {cpu_temp}°C")
        memusage = int(mem_used) / 64
        mem_usage.set(memusage)
        cpu_usage.set(int(cpu_load)/100)
        # cpu_load_label.configure(text=f"CPU: {cpu_load}%")
        # mem_used_label.configure(text=f"MEM: {mem_used}GB")
        # mem_avail_label.configure(text=f"MEM: {mem_avail}GB")
        gpu_temp_label.configure( text=f"GPU: {gpu_temp}°C")
        # gpu_power_draw_label.configure(text=f"GPU: {gpu_power_draw}wH")
        cpu_temp_label.after(1000, update_labels)
        
    lastClickX = 0
    lastClickY = 0
    
    def SaveLastClickPos(event):
        global lastClickX, lastClickY
        lastClickX = event.x
        lastClickY = event.y
        
    def Dragging(event):
        x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
        root.geometry("+%s+%s" % (x , y))
        
    def recenter(event):
        root.geometry("+%s+%s" % ((screen_width - width) - 5, (screen_height - height) - 50))
        
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    screen_width = root.winfo_screenwidth()
    screen_height= root.winfo_screenheight()
    root.bind('<Button-1>', SaveLastClickPos)
    root.bind('<Button-2>', recenter)
    root.bind('<B1-Motion>', Dragging)
    root.bind('<Double-ButtonRelease-3>', exit)
    root.wm_title("AppWindow Test")
    root.overrideredirect(True)
    root.option_add("*Background", "black")
    root.option_add("*Label*Background", "black")
    set_appwindow(root)
    update_labels()
    root.configure(bg='#404040')
    # root.attributes('-alpha',0.75)
    root.update()
    width = root.winfo_width()
    height = root.winfo_height()
    root.geometry(f"{(screen_width - width) - 5}+{(screen_height - height) - 50}")
    print(width, height)
    root.mainloop()

if __name__ == '__main__':
        main()
