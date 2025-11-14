import threading
import customtkinter as ctk
from modules.cpu_module import connect_cpu
from modules.gpu_module import connect_gpu
from modules.network_module import connect_network
from modules.storage_module import connect_storage


ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class ModuleRow:
    """Represents one row in the modules UI with controls and status."""

    def __init__(self, parent, name, connect_fn, row):
        self.name = name
        self.connect_fn = connect_fn

        self.label = ctk.CTkLabel(parent, text=name)
        self.label.grid(row=row, column=0, padx=8, pady=8, sticky="w")

        self.enabled_var = ctk.BooleanVar(value=False)
        self.switch = ctk.CTkSwitch(parent, text="Enable", variable=self.enabled_var)
        self.switch.grid(row=row, column=1, padx=8, pady=8)

        self.intensity = ctk.CTkSlider(parent, from_=0, to=100, number_of_steps=100)
        self.intensity.set(50)
        self.intensity.grid(row=row, column=2, padx=8, pady=8)

        self.btn = ctk.CTkButton(parent, text="Connect / Test", command=self.on_connect)
        self.btn.grid(row=row, column=3, padx=8, pady=8)

        self.status = ctk.CTkLabel(parent, text="Idle", anchor="w")
        self.status.grid(row=row, column=4, padx=8, pady=8, sticky="w")

    def set_status(self, text, color=None):
        # update on main thread
        def _update():
            self.status.configure(text=text)

        app.after(0, _update)

    def on_connect(self):
        if not self.enabled_var.get():
            self.set_status("Disabled - enable first")
            return

        intensity = int(self.intensity.get())
        self.btn.configure(state="disabled")
        self.set_status("Connecting...")

        def worker():
            try:
                # call the module's connect function (stub)
                result = self.connect_fn(intensity=intensity)
                msg = result.get("message", "Done")
                ok = result.get("success", False)
                status_text = f"OK: {msg}" if ok else f"Error: {msg}"
            except Exception as e:
                status_text = f"Exception: {e}"

            def _finish():
                self.set_status(status_text)
                self.btn.configure(state="normal")

            app.after(0, _finish)

        threading.Thread(target=worker, daemon=True).start()


app = ctk.CTk()
app.title("computer-detuner — Module Connector")
app.geometry("900x320")

container = ctk.CTkFrame(app)
container.pack(fill="both", expand=True, padx=12, pady=12)

title = ctk.CTkLabel(container, text="Modules", font=ctk.CTkFont(size=20, weight="bold"))
title.pack(anchor="w", pady=(0, 8))

grid_frame = ctk.CTkFrame(container)
grid_frame.pack(fill="both", expand=True)

# header row
headers = ["Module", "Enabled", "Intensity", "Action", "Status"]
for i, h in enumerate(headers):
    lbl = ctk.CTkLabel(grid_frame, text=h, fg_color=None)
    lbl.grid(row=0, column=i, padx=8, pady=6, sticky="w")

rows = []
modules = [
    ("CPU", connect_cpu),
    ("GPU", connect_gpu),
    ("Network", connect_network),
    ("Storage", connect_storage),
]

for idx, (name, fn) in enumerate(modules, start=1):
    rows.append(ModuleRow(grid_frame, name, fn, row=idx))


def on_close():
    # perform any cleanup if needed in future
    app.destroy()


app.protocol("WM_DELETE_WINDOW", on_close)

if __name__ == "__main__":
    app.mainloop()