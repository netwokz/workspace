import customtkinter
from pylogix import PLC

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("800x500")

current_val = False


def login():
    print("Login:")


def multi_ping(ip):
    with PLC(ip) as comm:
        speed = comm.Read("SORT_SPD.SORT_SPD_REQ")
        if speed.Value is None:
            speed.Value = "Oops!"
        current_val = speed.Value


def update_stats():
    afe1_sl2 = customtkinter.CTkLabel(master=frame, text=f"Flats ESTOP is {current_val} ")
    afe1_sl2.pack(pady=20, padx=10)


def get_stats():
    multi_ping("10.79.216.223")
    update_stats()


# def connect():
#     x = customtkinter.CTkButton(master=frame, text="Get Sorter Stats", command=get_stats)
#     x.pack(pady=12, padx=10)


root.bind()

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="PLC Stats from Python!!", font=("Helvetica", 24))
label.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Connect to PLC", command=get_stats)
button.pack(pady=12, padx=10)

root.mainloop()
