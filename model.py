# ============================================
# MODEL
# ============================================

import sqlite3
import os

class DatabaseManager:
    def __init__(self):
        self.db_folder = os.path.expanduser("DatabaseStudio")
        os.makedirs(self.db_folder, exist_ok=True)
        self.db_path = os.path.join(self.db_folder, "studio.db")

        self.db = sqlite3.connect(self.db_path)
        self.cursor = self.db.cursor()
        self.buat_tabel()

    def buat_tabel(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fotografer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT,
                kontak TEXT,
                spesialisasi TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS klien (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT,
                kontak TEXT,
                acara TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sesi_foto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT,
                lokasi TEXT,
                fotografer TEXT,
                klien TEXT,
                hasil TEXT
            )
        """)
        self.db.commit()

    def tambah(self, tabel, data):
        keys = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = tuple(data.values())

        self.cursor.execute(
            f"INSERT INTO {tabel} ({keys}) VALUES ({placeholders})",
            values
        )
        self.db.commit()

    def ambil_semua(self, tabel):
        self.cursor.execute(f"SELECT * FROM {tabel}")
        return self.cursor.fetchall()

    def get_nama_by_id(self, tabel, id_):
        self.cursor.execute(f"SELECT nama FROM {tabel} WHERE id = ?", (id_,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def tutup(self):
        self.db.close()


# Entity Class (Opsional)
class Orang:
    def __init__(self, nama, kontak):
        self.nama = nama
        self.kontak = kontak

class Fotografer(Orang):
    def __init__(self, nama, kontak, spesialisasi):
        super().__init__(nama, kontak)
        self.spesialisasi = spesialisasi

class Klien(Orang):
    def __init__(self, nama, kontak, acara):
        super().__init__(nama, kontak)
        self.acara = acara

class SesiFoto:
    def __init__(self, tanggal, lokasi, fotografer, klien, hasil):
        self.tanggal = tanggal
        self.lokasi = lokasi
        self.fotografer = fotografer
        self.klien = klien
        self.hasil = hasil
