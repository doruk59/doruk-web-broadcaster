import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import vlc
import os
import json
import shutil
from pathlib import Path
import random
from tkcalendar import Calendar
from PIL import Image, ImageTk

class PlaylistManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Doruk Web Broadcasting - Playlist Yöneticisi")
        self.root.state('zoomed')  # Tam ekran
        
        # Tema ayarları
        self.dark_mode = tk.BooleanVar(value=True)
        self.apply_theme()
        
        # Ana veriler
        self.playlists = {}
        self.current_playlist = None
        self.video_path = "/media/doruk/KINGSTON"
        self.playlists_dir = "playlists"
        
        # Dizinleri oluştur
        os.makedirs(self.playlists_dir, exist_ok=True)
        
        self.setup_ui()
        self.load_playlists()
        
    def setup_ui(self):
        # Ana notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Sekmeler
        self.manual_tab = ttk.Frame(self.notebook)
        self.scheduled_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.manual_tab, text="Plansız Playlist")
        self.notebook.add(self.scheduled_tab, text="Planlı Playlist")
        self.notebook.add(self.history_tab, text="Geçmiş")
        
        # Plansız Playlist Sekmesi
        self.setup_manual_tab()
        
        # Planlı Playlist Sekmesi
        self.setup_scheduled_tab()
        
        # Geçmiş Sekmesi
        self.setup_history_tab()
        
        # Alt menü
        self.setup_bottom_menu()
        
    def setup_manual_tab(self):
        # Sol panel - Video listesi
        left_frame = ttk.Frame(self.manual_tab)
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Video listesi
        self.video_list = ttk.Treeview(left_frame, columns=('Duration', 'Path'), show='headings')
        self.video_list.heading('Duration', text='Süre')
        self.video_list.heading('Path', text='Dosya Yolu')
        self.video_list.pack(fill='both', expand=True)
        
        # Sağ panel - Playlist işlemleri
        right_frame = ttk.Frame(self.manual_tab)
        right_frame.pack(side='right', fill='both', padx=5, pady=5)
        
        # Playlist kontrolları
        ttk.Button(right_frame, text="Video Ekle", command=self.add_video).pack(fill='x', pady=2)
        ttk.Button(right_frame, text="Video Sil", command=self.remove_video).pack(fill='x', pady=2)
        ttk.Button(right_frame, text="İsim Değiştir", command=self.rename_video).pack(fill='x', pady=2)
        ttk.Button(right_frame, text="Ön İzleme", command=self.preview_video).pack(fill='x', pady=2)
        
        # Oynatma seçenekleri
        ttk.Label(right_frame, text="Oynatma Modu:").pack(pady=5)
        self.play_mode = tk.StringVar(value="loop")
        ttk.Radiobutton(right_frame, text="Döngüsel", variable=self.play_mode, 
                       value="loop").pack()
        ttk.Radiobutton(right_frame, text="Tek Sefer", variable=self.play_mode, 
                       value="once").pack()
        ttk.Radiobutton(right_frame, text="Karışık", variable=self.play_mode, 
                       value="random").pack()
        
    def setup_scheduled_tab(self):
        # Takvim
        self.calendar = Calendar(self.scheduled_tab)
        self.calendar.pack(pady=10)
        
        # Zamanlama kontrolleri
        schedule_frame = ttk.Frame(self.scheduled_tab)
        schedule_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(schedule_frame, text="Başlangıç Saati:").pack()
        self.time_entry = ttk.Entry(schedule_frame)
        self.time_entry.pack()
        
        ttk.Button(schedule_frame, text="Plan Ekle", 
                  command=self.add_schedule).pack(pady=5)
        
        # Planlanan yayınlar listesi
        self.schedule_list = ttk.Treeview(self.scheduled_tab, 
                                        columns=('Date', 'Time', 'Playlist'),
                                        show='headings')
        self.schedule_list.heading('Date', text='Tarih')
        self.schedule_list.heading('Time', text='Saat')
        self.schedule_list.heading('Playlist', text='Playlist')
        self.schedule_list.pack(fill='both', expand=True)
        
    def setup_history_tab(self):
        # Geçmiş kayıtları
        self.history_list = ttk.Treeview(self.history_tab,
                                       columns=('Date', 'Duration', 'Videos'),
                                       show='headings')
        self.history_list.heading('Date', text='Tarih')
        self.history_list.heading('Duration', text='Süre')
        self.history_list.heading('Videos', text='Videolar')
        self.history_list.pack(fill='both', expand=True)
        
    def setup_bottom_menu(self):
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side='bottom', fill='x', padx=5, pady=5)
        
        # Tema değiştirme
        ttk.Checkbutton(bottom_frame, text="Karanlık Mod", 
                       variable=self.dark_mode,
                       command=self.apply_theme).pack(side='left')
        
        # Yedekleme
        ttk.Button(bottom_frame, text="Yedekle", 
                  command=self.backup_playlists).pack(side='right', padx=5)
        ttk.Button(bottom_frame, text="Geri Yükle",
                  command=self.restore_playlists).pack(side='right')
        
    def apply_theme(self):
        style = ttk.Style()
        if self.dark_mode.get():
            style.configure(".", background="black", foreground="white")
            style.configure("Treeview", background="gray20", 
                          fieldbackground="gray20", foreground="white")
        else:
            style.configure(".", background="white", foreground="black")
            style.configure("Treeview", background="white",
                          fieldbackground="white", foreground="black")
    
    def add_video(self):
        files = os.listdir(self.video_path)
        videos = [f for f in files if f.endswith('.mp4')]
        
        if not videos:
            messagebox.showerror("Hata", "USB bellekte video bulunamadı!")
            return
            
        # Video seçim penceresi
        select_window = tk.Toplevel(self.root)
        select_window.title("Video Seç")
        
        for video in videos:
            path = os.path.join(self.video_path, video)
            duration = self.get_video_duration(path)
            
            frame = ttk.Frame(select_window)
            frame.pack(fill='x', padx=5, pady=2)
            
            ttk.Label(frame, text=video).pack(side='left')
            ttk.Label(frame, text=duration).pack(side='left', padx=5)
            ttk.Button(frame, text="Ekle",
                      command=lambda p=path: self.add_video_to_list(p)).pack(side='right')
    
    def add_video_to_list(self, path):
        duration = self.get_video_duration(path)
        self.video_list.insert('', 'end', values=(duration, path))
        self.update_total_duration()
    
    def remove_video(self):
        selected = self.video_list.selection()
        if selected:
            self.video_list.delete(selected)
            self.update_total_duration()
    
    def rename_video(self):
        selected = self.video_list.selection()
        if not selected:
            return
            
        # Yeni isim penceresi
        rename_window = tk.Toplevel(self.root)
        rename_window.title("İsim Değiştir")
        
        ttk.Label(rename_window, text="Yeni İsim:").pack()
        name_entry = ttk.Entry(rename_window)
        name_entry.pack()
        
        def apply_rename():
            new_name = name_entry.get()
            if new_name:
                item = self.video_list.item(selected)
                values = item['values']
                values = (values[0], new_name)
                self.video_list.item(selected, values=values)
                rename_window.destroy()
        
        ttk.Button(rename_window, text="Uygula", command=apply_rename).pack()
    
    def preview_video(self):
        selected = self.video_list.selection()
        if not selected:
            return
            
        path = self.video_list.item(selected)['values'][1]
        
        # VLC ile önizleme
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new(path)
        player.set_media(media)
        
        # Önizleme penceresi
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Ön İzleme")
        
        if os.name == "nt":
            player.set_hwnd(preview_window.winfo_id())
        else:
            player.set_xwindow(preview_window.winfo_id())
            
        player.play()
        
    def get_video_duration(self, path):
        instance = vlc.Instance()
        media = instance.media_new(path)
        media.parse()
        duration = media.get_duration() / 1000  # ms to seconds
        return f"{int(duration//60)}:{int(duration%60):02d}"
    
    def update_total_duration(self):
        total = 0
        for item in self.video_list.get_children():
            duration = self.video_list.item(item)['values'][0]
            minutes, seconds = map(int, duration.split(':'))
            total += minutes * 60 + seconds
            
        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60
        
        if hours > 0:
            duration_text = f"Toplam Süre: {hours}:{minutes:02d}:{seconds:02d}"
        else:
            duration_text = f"Toplam Süre: {minutes}:{seconds:02d}"
            
        # Toplam süreyi göster
        if hasattr(self, 'duration_label'):
            self.duration_label.config(text=duration_text)
        else:
            self.duration_label = ttk.Label(self.manual_tab, text=duration_text)
            self.duration_label.pack(side='bottom')
    
    def add_schedule(self):
        date = self.calendar.get_date()
        time = self.time_entry.get()
        
        if not time:
            messagebox.showerror("Hata", "Lütfen saat girin!")
            return
            
        # Çakışma kontrolü
        for item in self.schedule_list.get_children():
            existing_date = self.schedule_list.item(item)['values'][0]
            existing_time = self.schedule_list.item(item)['values'][1]
            
            if date == existing_date and time == existing_time:
                messagebox.showerror("Hata", "Bu zaman dilimi dolu!")
                return
        
        # Playlist seç
        playlist_name = self.select_playlist()
        if playlist_name:
            self.schedule_list.insert('', 'end', values=(date, time, playlist_name))
    
    def select_playlist(self):
        playlists = os.listdir(self.playlists_dir)
        if not playlists:
            messagebox.showerror("Hata", "Kayıtlı playlist yok!")
            return None
            
        # Playlist seçim penceresi
        select_window = tk.Toplevel(self.root)
        select_window.title("Playlist Seç")
        
        selected_playlist = tk.StringVar()
        
        for playlist in playlists:
            ttk.Radiobutton(select_window, text=playlist,
                          variable=selected_playlist,
                          value=playlist).pack()
        
        def confirm():
            select_window.destroy()
            
        ttk.Button(select_window, text="Seç", command=confirm).pack()
        
        select_window.wait_window()
        return selected_playlist.get()
    
    def save_playlist(self, name):
        videos = []
        for item in self.video_list.get_children():
            values = self.video_list.item(item)['values']
            videos.append({
                'duration': values[0],
                'path': values[1]
            })
            
        playlist_data = {
            'name': name,
            'videos': videos,
            'play_mode': self.play_mode.get(),
            'created_at': datetime.now().isoformat()
        }
        
        with open(os.path.join(self.playlists_dir, f"{name}.json"), 'w') as f:
            json.dump(playlist_data, f, indent=4)
    
    def load_playlists(self):
        if not os.path.exists(self.playlists_dir):
            return
            
        for file in os.listdir(self.playlists_dir):
            if file.endswith('.json'):
                with open(os.path.join(self.playlists_dir, file)) as f:
                    self.playlists[file[:-5]] = json.load(f)
    
    def backup_playlists(self):
        backup_dir = "playlist_backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"playlist_backup_{timestamp}.zip")
        
        shutil.make_archive(backup_file[:-4], 'zip', self.playlists_dir)
        messagebox.showinfo("Başarılı", f"Yedekleme tamamlandı:\n{backup_file}")
    
    def restore_playlists(self):
        backup_dir = "playlist_backups"
        if not os.path.exists(backup_dir):
            messagebox.showerror("Hata", "Yedek bulunamadı!")
            return
            
        backups = os.listdir(backup_dir)
        if not backups:
            messagebox.showerror("Hata", "Yedek bulunamadı!")
            return
            
        # Yedek seçim penceresi
        select_window = tk.Toplevel(self.root)
        select_window.title("Yedek Seç")
        
        selected_backup = tk.StringVar()
        
        for backup in backups:
            ttk.Radiobutton(select_window, text=backup,
                          variable=selected_backup,
                          value=backup).pack()
        
        def restore():
            backup_file = os.path.join(backup_dir, selected_backup.get())
            shutil.unpack_archive(backup_file, self.playlists_dir)
            self.load_playlists()
            select_window.destroy()
            messagebox.showinfo("Başarılı", "Yedek geri yüklendi!")
            
        ttk.Button(select_window, text="Geri Yükle", command=restore).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistManager(root)
    root.mainloop()
