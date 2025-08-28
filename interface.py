import tkinter as tk
from tkinter import ttk
from projeto import ProxyViewer

class BoostLives:
    def __init__(self, root):
        self.root = root
        self.root.title("Boost Lives")
        self.root.geometry("800x600")
        self.root.configure(bg="#2d223c")  # Roxo escuro suave
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # Cores principais
        roxo_bg = "#2d223c"
        roxo_claro = "#6c4f99"
        roxo_medio = "#a084ca"
        roxo_hover = "#bfa2e4"
        branco = "#f5f5fa"
        cinza = "#3a2e4d"
        # Frames e labels
        self.style.configure("TFrame", background=roxo_bg)
        self.style.configure("TLabel", background=roxo_bg, foreground=branco, font=("Segoe UI", 10))
        self.style.configure("TLabelframe", background=roxo_bg, foreground=roxo_claro, font=("Segoe UI", 11, "bold"))
        self.style.configure("TLabelframe.Label", background=roxo_bg, foreground=roxo_claro, font=("Segoe UI", 11, "bold"))
        # Botões
        self.style.configure("TButton", background=roxo_claro, foreground=branco, font=("Segoe UI", 10, "bold"), borderwidth=0, focusthickness=2, focuscolor=roxo_hover)
        self.style.map("TButton",
            background=[('active', roxo_hover), ('!active', roxo_claro)],
            foreground=[('disabled', cinza), ('!disabled', branco)]
        )
        # Entradas
        self.style.configure("TEntry", fieldbackground=cinza, foreground=branco, borderwidth=1, font=("Segoe UI", 10))
        self.style.map("TEntry", fieldbackground=[('active', roxo_medio)])
        # Combobox
        self.style.configure("TCombobox", fieldbackground=cinza, foreground=branco, background=cinza, borderwidth=1, font=("Segoe UI", 10))
        self.style.map("TCombobox",
            fieldbackground=[('readonly', roxo_medio), ('!readonly', cinza)],
            background=[('readonly', roxo_medio), ('!readonly', cinza)],
            foreground=[('readonly', branco), ('!readonly', branco)]
        )
        self.proxy_viewer = None
        self.create_widgets()

    def create_widgets(self):
        # Top bar with logo and settings
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, pady=(5, 0))
        logo = ttk.Label(top_frame, text=" ", width=4)
        logo.pack(side=tk.LEFT, padx=(10, 0))
        title_label = ttk.Label(top_frame, text="Boost Lives", font=("Segoe UI", 18, "bold"), foreground="#a084ca", background="#2d223c")
        title_label.pack(side=tk.LEFT, padx=(10, 0))
        settings_btn = ttk.Button(top_frame, text="Settings", width=10)
        settings_btn.pack(side=tk.RIGHT, padx=10)

        # Menu bar (tabs)
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill=tk.X, pady=(5, 0))
        menu_items = [
            "Proxy Tools", "Account Tools", "Multi-Checker", "View Bots", "Follow Bot", "Chat/Raid Bot", "Revenue Tools"
        ]
        for item in menu_items:
            btn = ttk.Button(menu_frame, text=item, style="TButton", width=14)
            btn.pack(side=tk.LEFT, padx=1, pady=2)

        # Divider
        divider = ttk.Separator(self.root, orient='horizontal')
        divider.pack(fill=tk.X, pady=2)

        # Main content with two sections
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Live Views Section
        live_frame = ttk.LabelFrame(main_frame, text="Live Views")
        live_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.create_live_views(live_frame)

        # Vertical divider
        vdivider = ttk.Separator(main_frame, orient='vertical')
        vdivider.pack(side=tk.LEFT, fill=tk.Y, padx=2)

        # Clip Views Section
        clip_frame = ttk.LabelFrame(main_frame, text="Clip Views")
        clip_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.create_clip_views(clip_frame)

    def create_live_views(self, parent):
        # Channel
        channel_frame = ttk.Frame(parent)
        channel_frame.pack(fill=tk.X, pady=2, padx=5)
        ttk.Label(channel_frame, text="Channel:").pack(side=tk.LEFT, padx=(0, 5))
        self.entry_channel = ttk.Entry(channel_frame, width=20)
        self.entry_channel.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Threads
        threads_frame = ttk.Frame(parent)
        threads_frame.pack(fill=tk.X, pady=2, padx=5)
        ttk.Label(threads_frame, text="Threads:").pack(side=tk.LEFT, padx=(0, 5))
        self.entry_threads = ttk.Entry(threads_frame, width=8)
        self.entry_threads.insert(0, "35")
        self.entry_threads.pack(side=tk.LEFT)

        # Type
        type_frame = ttk.Frame(parent)
        type_frame.pack(fill=tk.X, pady=2, padx=5)
        ttk.Label(type_frame, text="Type:").pack(side=tk.LEFT, padx=(0, 5))
        self.combo_type = ttk.Combobox(type_frame, width=18, values=["Make a select...", "Option 1", "Option 2"])
        self.combo_type.current(0)
        self.combo_type.pack(side=tk.LEFT)

        # Timeout
        timeout_frame = ttk.Frame(parent)
        timeout_frame.pack(fill=tk.X, pady=2, padx=5)
        ttk.Label(timeout_frame, text="Timeout in ms").pack(side=tk.LEFT, padx=(0, 5))
        self.entry_timeout = ttk.Entry(timeout_frame, width=8)
        self.entry_timeout.insert(0, "5000")
        self.entry_timeout.pack(side=tk.LEFT)

        # Buttons
        btn_frame1 = ttk.Frame(parent)
        btn_frame1.pack(fill=tk.X, pady=4, padx=5)
        self.live_start_btn = ttk.Button(btn_frame1, text="Start", command=self.start_live_views)
        self.live_start_btn.pack(side=tk.LEFT, padx=2)
        self.load_proxies_btn = ttk.Button(btn_frame1, text="Load Proxies")
        self.load_proxies_btn.pack(side=tk.LEFT, padx=2)

        btn_frame2 = ttk.Frame(parent)
        btn_frame2.pack(fill=tk.X, pady=2, padx=5)
        self.live_stop_btn = ttk.Button(btn_frame2, text="Stop", command=self.stop_live_views)
        self.live_stop_btn.pack(side=tk.LEFT, padx=2)
        self.load_channels_btn = ttk.Button(btn_frame2, text="Load Channels")
        self.load_channels_btn.pack(side=tk.LEFT, padx=2)

        # Multi-Channel checkbox
        self.multi_channel_var = tk.BooleanVar()
        multi_channel_cb = ttk.Checkbutton(parent, text="Multi-Channel", variable=self.multi_channel_var)
        multi_channel_cb.pack(anchor=tk.W, padx=10, pady=2)

        # Info labels
        self.proxies_label = ttk.Label(parent, text="Proxies: 0")
        self.proxies_label.pack(anchor=tk.W, padx=10)
        self.channels_label = ttk.Label(parent, text="Channels: 0")
        self.channels_label.pack(anchor=tk.W, padx=10)
        self.requests_sent_label = ttk.Label(parent, text="Requests Sent: 0")
        self.requests_sent_label.pack(anchor=tk.W, padx=10)
        self.requests_failed_label = ttk.Label(parent, text="Requests Failed: 0")
        self.requests_failed_label.pack(anchor=tk.W, padx=10)
        self.live_status = ttk.Label(parent, text="Status: Idle")
        self.live_status.pack(anchor=tk.W, padx=10, pady=2)

    def create_clip_views(self, parent):
        # Channel
        channel_frame = ttk.Frame(parent)
        channel_frame.pack(fill=tk.X, pady=2, padx=5)
        ttk.Label(channel_frame, text="Channel:").pack(side=tk.LEFT, padx=(0, 5))
        self.clip_entry_channel = ttk.Entry(channel_frame, width=20)
        self.clip_entry_channel.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Clip ID
        clipid_frame = ttk.Frame(parent)
        clipid_frame.pack(fill=tk.X, pady=2, padx=5)
        ttk.Label(clipid_frame, text="Clip ID:").pack(side=tk.LEFT, padx=(0, 5))
        self.clip_entry_clipid = ttk.Entry(clipid_frame, width=20)
        self.clip_entry_clipid.insert(0, "SpunkyGrizzlyBear")
        self.clip_entry_clipid.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Threads
        threads_frame = ttk.Frame(parent)
        threads_frame.pack(fill=tk.X, pady=2, padx=5)
        ttk.Label(threads_frame, text="Threads:").pack(side=tk.LEFT, padx=(0, 5))
        self.clip_entry_threads = ttk.Entry(threads_frame, width=8)
        self.clip_entry_threads.insert(0, "35")
        self.clip_entry_threads.pack(side=tk.LEFT)

        # Type
        type_frame = ttk.Frame(parent)
        type_frame.pack(fill=tk.X, pady=2, padx=5)
        ttk.Label(type_frame, text="Type:").pack(side=tk.LEFT, padx=(0, 5))
        self.clip_combo_type = ttk.Combobox(type_frame, width=18, values=["Make a select...", "Option 1", "Option 2"])
        self.clip_combo_type.current(0)
        self.clip_combo_type.pack(side=tk.LEFT)

        # Timeout
        timeout_frame = ttk.Frame(parent)
        timeout_frame.pack(fill=tk.X, pady=2, padx=5)
        ttk.Label(timeout_frame, text="Timeout in ms").pack(side=tk.LEFT, padx=(0, 5))
        self.clip_entry_timeout = ttk.Entry(timeout_frame, width=8)
        self.clip_entry_timeout.insert(0, "5000")
        self.clip_entry_timeout.pack(side=tk.LEFT)

        # Buttons
        btn_frame1 = ttk.Frame(parent)
        btn_frame1.pack(fill=tk.X, pady=4, padx=5)
        self.clip_start_btn = ttk.Button(btn_frame1, text="Start")
        self.clip_start_btn.pack(side=tk.LEFT, padx=2)
        self.clip_load_proxies_btn = ttk.Button(btn_frame1, text="Load Proxies")
        self.clip_load_proxies_btn.pack(side=tk.LEFT, padx=2)
        self.clip_stop_btn = ttk.Button(btn_frame1, text="Stop")
        self.clip_stop_btn.pack(side=tk.LEFT, padx=2)

        # Info labels
        self.clip_proxies_label = ttk.Label(parent, text="Proxies: 0")
        self.clip_proxies_label.pack(anchor=tk.W, padx=10)
        self.clip_requests_sent_label = ttk.Label(parent, text="Requests Sent: 0")
        self.clip_requests_sent_label.pack(anchor=tk.W, padx=10)
        self.clip_requests_failed_label = ttk.Label(parent, text="Requests Failed: 0")
        self.clip_requests_failed_label.pack(anchor=tk.W, padx=10)

    def start_live_views(self):
        proxies = ["http://proxy1:8080", "http://proxy2:3128"]
        try:
            threads = int(self.entry_threads.get()) if self.entry_threads.get().isdigit() else 3
        except Exception:
            threads = 3
        self.proxy_viewer = ProxyViewer(proxies, timeout=5, max_threads=threads)
        self.live_status.config(text="Status: Executando...")
        self.root.after(100, self.run_proxy_viewer)

    def run_proxy_viewer(self):
        if self.proxy_viewer:
            resultados = self.proxy_viewer.start()
            self.live_status.config(text=f"Status: Finalizado. Sucesso: {sum(1 for r in resultados if r[1]=='sucesso')}")

    def stop_live_views(self):
        if self.proxy_viewer:
            self.proxy_viewer.active = False
            self.live_status.config(text="Status: Parado")

if __name__ == "__main__":
    root = tk.Tk()
    app = BoostLives(root)
    root.mainloop()
