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
        # Tabel Fotografer
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fotografer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                kontak TEXT NOT NULL,
                spesialisasi TEXT NOT NULL
            )
        """)

        # Tabel Klien
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS klien (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                kontak TEXT NOT NULL,
                acara TEXT NOT NULL
            )
        """)

        # Tabel Sesi (RELASI ID, bukan string)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sesi_foto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT NOT NULL,
                lokasi TEXT NOT NULL,
                fotografer_id INTEGER NOT NULL,
                klien_id INTEGER NOT NULL,
                hasil TEXT,
                FOREIGN KEY(fotografer_id) REFERENCES fotografer(id),
                FOREIGN KEY(klien_id) REFERENCES klien(id)
            )
        """)

        self.db.commit()

    # Tambah data generik
    def tambah(self, tabel, data):
        keys = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        values = tuple(data.values())

        self.cursor.execute(
            f"INSERT INTO {tabel} ({keys}) VALUES ({placeholders})",
            values
        )
        self.db.commit()

    # Ambil semua data
    def ambil_semua(self, tabel):
        self.cursor.execute(f"SELECT * FROM {tabel}")
        return self.cursor.fetchall()

    # Ambil nama berdasarkan ID
    def get_by_id(self, tabel, id_):
        self.cursor.execute(f"SELECT * FROM {tabel} WHERE id = ?", (id_,))
        return self.cursor.fetchone()

    def get_nama_by_id(self, tabel, id_):
        self.cursor.execute(f"SELECT nama FROM {tabel} WHERE id = ?", (id_,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def tutup(self):
        self.db.close()
