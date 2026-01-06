from cryptography.fernet import Fernet
import os
import json

# Untuk mengambil lokasi folder tempat file backend.py ini berada
FOLDER_PROJECT = os.path.dirname(os.path.abspath(__file__))

# menggabungkan lokasi folder itu dengan nama file
VAULT_FILE = os.path.join(FOLDER_PROJECT, "secret.key")

# ------------------------------------------------

def muat_vault():
    """Membaca isi file secret.key"""
    if not os.path.exists(VAULT_FILE):
        return {} 
    
    try:
        with open(VAULT_FILE, "r") as f:
            return json.load(f)
    except:
        return {} 

def simpan_vault(data):
    """Menyimpan daftar kunci"""
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=4)

def enkripsi_file(path_file):
    nama_file = os.path.basename(path_file)
    
    # 1. Generate kunci unik
    kunci_baru = Fernet.generate_key()
    key_string = kunci_baru.decode()
    
    # 2. Update database
    vault = muat_vault()
    vault[nama_file] = key_string
    simpan_vault(vault)
    
    # 3. Enkripsi
    fernet = Fernet(kunci_baru)
    
    try:
        with open(path_file, "rb") as file:
            data_asli = file.read()
            
        data_terenkripsi = fernet.encrypt(data_asli)
        
        with open(path_file, "wb") as file:
            file.write(data_terenkripsi)
            
        # PRINT LOKASI FILE KUNCINYA SUPAYA JELAS
        print(f" SUKSES! File dikunci.")
        print(f" File 'secret.key' disimpan di: {VAULT_FILE}")
        
    except Exception as e:
        print(f" Error Enkripsi: {e}")
        # Lemparkan error ke main.py supaya muncul di popup
        raise e 

def dekripsi_file(path_file):
    nama_file = os.path.basename(path_file)
    vault = muat_vault()
    
    if nama_file not in vault:
        # lempar error supaya muncul di GUI
        raise Exception(f"Kunci untuk '{nama_file}' tidak ditemukan di database!")

    key_string = vault[nama_file]
    kunci_bytes = key_string.encode()
    
    fernet = Fernet(kunci_bytes)
    
    try:
        with open(path_file, "rb") as file:
            data_terenkripsi = file.read()
            
        data_asli = fernet.decrypt(data_terenkripsi)
        
        with open(path_file, "wb") as file:
            file.write(data_asli)
            
        print(f"SUKSES! File dibuka.")

    except Exception as e:
        print(f"Error Dekripsi: {e}")

        raise e

