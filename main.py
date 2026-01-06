import tkinter as tk
from tkinter import filedialog, messagebox
import backend 
import os

# --- FUNGSI TOMBOL ---

def cari_file():
    filename = filedialog.askopenfilename(title="Pilih File untuk Diamankan")
    if filename:
        entry_lokasi.delete(0, tk.END)
        entry_lokasi.insert(0, filename)

def proses_enkripsi():
    file_path = entry_lokasi.get()
    
    # Validasi input
    if not file_path:
        messagebox.showwarning("Peringatan", "Harap pilih file terlebih dahulu!")
        return
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "File tidak ditemukan!")
        return
    
    # Panggil Backend
    try:
        backend.enkripsi_file(file_path)
        messagebox.showinfo("Berhasil", f"File berhasil DIKUNCI!\n\nNama: {os.path.basename(file_path)}\nKunci tersimpan di secret.key")
    except Exception as e:
        messagebox.showerror("Gagal", f"Terjadi kesalahan: {str(e)}")

def proses_dekripsi():
    file_path = entry_lokasi.get()
    
    if not file_path:
        messagebox.showwarning("Peringatan", "Harap pilih file terlebih dahulu!")
        return
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "File tidak ditemukan!")
        return

    # Panggil Backend
    try:
        backend.dekripsi_file(file_path)
        messagebox.showinfo("Berhasil", f"File berhasil DIBUKA!\n\nNama: {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Gagal", f"Terjadi kesalahan: {str(e)}")

# --- TAMPILAN (GUI) ---

app = tk.Tk()
app.title("SecureVault - Kelompok 7")
app.geometry("500x350")
app.configure(bg="#f0f0f0")

# Judul
label_judul = tk.Label(app, text="SecureVault", font=("Helvetica", 20, "bold"), bg="#f0f0f0", fg="#333")
label_judul.pack(pady=20)

# Input File
frame_input = tk.Frame(app, bg="#f0f0f0")
frame_input.pack(pady=10)

entry_lokasi = tk.Entry(frame_input, width=40, font=("Arial", 10))
entry_lokasi.pack(side=tk.LEFT, padx=5)

tombol_cari = tk.Button(frame_input, text=" Cari", command=cari_file, bg="#ddd")
tombol_cari.pack(side=tk.LEFT)

# Tombol Eksekusi
frame_tombol = tk.Frame(app, bg="#f0f0f0")
frame_tombol.pack(pady=20)

btn_encrypt = tk.Button(frame_tombol, text=" ENCRYPT\n(Kunci File)", 
                        font=("Arial", 11, "bold"), bg="#ffcccc", fg="#d90000",
                        width=18, height=3, command=proses_enkripsi)
btn_encrypt.pack(side=tk.LEFT, padx=15)

btn_decrypt = tk.Button(frame_tombol, text=" DECRYPT\n(Buka File)", 
                        font=("Arial", 11, "bold"), bg="#ccffcc", fg="#006600",
                        width=18, height=3, command=proses_dekripsi)
btn_decrypt.pack(side=tk.LEFT, padx=15)

# Footer
label_info = tk.Label(app, text="Mode: Individual Key (Vault System)", bg="#f0f0f0", fg="gray", font=("Arial", 8))
label_info.pack(side=tk.BOTTOM, pady=10)


app.mainloop()
