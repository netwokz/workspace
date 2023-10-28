import customtkinter
from pylogix import PLC

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("800x500")

sorters = {"AFE1": "10.79.218.12", "AFE2": "10.79.219.12", "SHP": "10.79.216.201", "MRS": "10.79.216.171"}

current_speeds = {"AFE1": "", "AFE2": "", "SHP": "", "MRS": ""}


def login():
    print("Login:")


def multi_ping(sl2, ip):
    with PLC(ip) as comm:
        speed = comm.Read("SORT_SPD.SORT_SPD_REQ")
        if speed.Value is None:
            speed.Value = "Oops!"
        current_speeds[sl2] = speed.Value


def update_stats():
    afe1_sl2 = customtkinter.CTkLabel(master=frame, text=f"AFE1 is running at {current_speeds['AFE1']} ")
    afe1_sl2.pack(pady=20, padx=10)

    afe2_sl2 = customtkinter.CTkLabel(master=frame, text=f"AFE2 is running at {current_speeds['AFE2']} ")
    afe2_sl2.pack(pady=20, padx=20)

    shp_sl2 = customtkinter.CTkLabel(master=frame, text=f"SHP is running at {current_speeds['SHP']} ")
    shp_sl2.pack(pady=20, padx=30)

    mrs_sl2 = customtkinter.CTkLabel(master=frame, text=f"MRS is running at {current_speeds['MRS']} ")
    mrs_sl2.pack(pady=20, padx=40)


def get_stats():
    for sl2, ip in sorters.items():
        multi_ping(sl2, ip)
    update_stats()


def connect():
    x = customtkinter.CTkButton(master=frame, text="Get Sorter Stats", command=get_stats)
    x.pack(pady=12, padx=10)


root.bind()

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="PLC Stats from Python!!", font=("Helvetica", 24))
label.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Connect to PLC", command=connect)
button.pack(pady=12, padx=10)

root.mainloop()
