import threading
import customtkinter as ctk
from modules.cpu_module import connect_cpu
from modules.gpu_module import connect_gpu
from modules.network_module import connect_network, start_universal_latency, stop_universal_latency, status as network_status
from modules.storage_module import connect_storage


ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("yellow.json")


class ModuleRow:
    """Represents one row in the modules UI with controls and a Start/Stop toggle."""

    def __init__(self, parent, name, connect_fn, row):
        import inspect

        self.name = name
        self.connect_fn = connect_fn
        self._supports_stop = False
        # detect if connect_fn accepts a cooperative stop event
        try:
            sig = inspect.signature(connect_fn)
            self._supports_stop = 'stop_event' in sig.parameters or 'cancel_event' in sig.parameters
        except Exception:
            self._supports_stop = False

        self._running = False
        self._stop_event = threading.Event()

        self.label = ctk.CTkLabel(parent, text=name)
        self.label.grid(row=row, column=0, padx=8, pady=8, sticky="w")

        self.intensity = ctk.CTkSlider(parent, from_=1, to=5, number_of_steps=5)
        self.intensity.set(5)
        self.intensity.grid(row=row, column=1, padx=8, pady=8)

        # Single toggle button shared style with NetworkRow
        self.toggle_btn = ctk.CTkButton(parent, text="Start", command=self.on_toggle)
        self.toggle_btn.grid(row=row, column=2, padx=8, pady=8)

        self.status = ctk.CTkLabel(parent, text="Idle", anchor="w")
        self.status.grid(row=row, column=3, padx=8, pady=8, sticky="w")

    def set_status(self, text):
        def _update():
            self.status.configure(text=text)

        app.after(0, _update)

    def on_toggle(self):
        # Start or request stop depending on current state
        if not self._running:
            # start
            intensity = int(self.intensity.get())
            self.toggle_btn.configure(state="disabled")
            self.set_status("Starting...")
            self._stop_event.clear()
            self._running = True

            def worker():
                try:
                    # try passing cooperative stop_event if supported
                    if self._supports_stop:
                        # prefer parameter name stop_event if available
                        try:
                            result = self.connect_fn(intensity=intensity, stop_event=self._stop_event)
                        except TypeError:
                            result = self.connect_fn(intensity=intensity, cancel_event=self._stop_event)
                    else:
                        result = self.connect_fn(intensity=intensity)

                    msg = result.get('message', 'Done') if isinstance(result, dict) else str(result)
                    ok = result.get('success', False) if isinstance(result, dict) else True
                    status_text = f"OK: {msg}" if ok else f"Error: {msg}"
                except Exception as e:
                    status_text = f"Exception: {e}"
                finally:
                    self._running = False

                def _finish():
                    self.set_status(status_text)
                    self.toggle_btn.configure(text="Start")
                    self.toggle_btn.configure(state="normal")

                app.after(0, _finish)

            self.toggle_btn.configure(text="Stop")
            threading.Thread(target=worker, daemon=True).start()
        else:
            # request stop
            self.toggle_btn.configure(state="disabled")
            self.set_status("Stopping...")
            # signal the worker if it supports cooperative stop
            try:
                self._stop_event.set()
            except Exception:
                pass

            # update UI immediately; actual worker will finalize when it notices stop
            def _finish():
                self.set_status("Stop requested")
                self.toggle_btn.configure(text="Start")
                self.toggle_btn.configure(state="normal")

            app.after(0, _finish)


app = ctk.CTk() # Create the main application window

app.title("computer-detuner — Module Connector")
app.geometry("900x320")

container = ctk.CTkFrame(app)
container.pack(fill="both", expand=True, padx=12, pady=12)

title = ctk.CTkLabel(container, text="Modules", font=ctk.CTkFont(size=20, weight="bold"))
title.pack(anchor="w", pady=(0, 8))

grid_frame = ctk.CTkFrame(container)
grid_frame.pack(fill="both", expand=True)

# header row
headers = ["Module", "Intensity", "Action", "Status"]
for i, h in enumerate(headers):
    lbl = ctk.CTkLabel(grid_frame, text=h, fg_color=None)
    lbl.grid(row=0, column=i, padx=8, pady=6, sticky="w")

rows = []
class NetworkRow:
    """Special row with a single toggle button for the network latency proxy."""

    def __init__(self, parent, row):
        self.label = ctk.CTkLabel(parent, text="Network")
        self.label.grid(row=row, column=0, padx=8, pady=8, sticky="w")

        self.intensity = ctk.CTkSlider(parent, from_=1, to=5, number_of_steps=5)
        self.intensity.set(5)
        self.intensity.grid(row=row, column=1, padx=8, pady=8)

        # Single toggle button that starts or stops the proxy
        self.toggle_btn = ctk.CTkButton(parent, text="Start", command=self.on_toggle)
        self.toggle_btn.grid(row=row, column=2, padx=8, pady=8)

        self.status = ctk.CTkLabel(parent, text="Idle", anchor="w")
        self.status.grid(row=row, column=3, padx=8, pady=8, sticky="w")

        # Initialize UI to reflect current proxy state
        self._refresh_ui()

    def set_status(self, text):
        def _update():
            self.status.configure(text=text)

        app.after(0, _update)

    def _refresh_ui(self):
        st = network_status()
        running = bool(st.get('running'))

        def _update():
            self.toggle_btn.configure(text="Stop" if running else "Start")
            self.set_status(f"Running: {st.get('latency_ms',0)}ms" if running else "Idle")

        app.after(0, _update)

    def on_toggle(self):
        intensity = int(self.intensity.get())
        # disable while working
        self.toggle_btn.configure(state="disabled")
        self.set_status("Working...")

        def worker():
            try:
                # call the network module's toggle helper which starts/stops based on state
                result = connect_network(intensity=intensity)
                status_text = result.get('message', '')
            except Exception as e:
                status_text = f"Error: {e}"

            def _finish():
                self.set_status(status_text)
                # refresh button text/state to reflect new running state
                try:
                    st = network_status()
                    running = bool(st.get('running'))
                    self.toggle_btn.configure(text="Stop" if running else "Start")
                except Exception:
                    self.toggle_btn.configure(text="Start")
                self.toggle_btn.configure(state="normal")

            app.after(0, _finish)

        threading.Thread(target=worker, daemon=True).start()


# create rows manually so Network has custom controls
rows.append(ModuleRow(grid_frame, "CPU", connect_cpu, row=1))
rows.append(ModuleRow(grid_frame, "GPU", connect_gpu, row=2))
rows.append(NetworkRow(grid_frame, row=3))
rows.append(ModuleRow(grid_frame, "Storage", connect_storage, row=4))


def on_close():
    # perform any cleanup if needed in future
    app.destroy()


app.protocol("WM_DELETE_WINDOW", on_close)

if __name__ == "__main__":
    app.mainloop()