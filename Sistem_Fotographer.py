# ================================================
# SISTEM MANAJEMEN STUDIO FOTOGRAFI (Versi Rich UI MAX)
# ================================================

import sqlite3
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


# ===============================
#  Bagian Database
# ===============================
class DatabaseManager:
    def __init__(self):
        # Lokasi database di
        self.db_folder = os.path.expanduser("DatabaseStudio")
        os.makedirs(self.db_folder, exist_ok=True)
        self.db_path = os.path.join(self.db_folder, "studio.db")

        try:
            self.db = sqlite3.connect(self.db_path)
            self.cursor = self.db.cursor()
            self.buat_tabel()

            console.print(
                Panel.fit(
                    f"[bold green]Database aktif di:[/bold green]\n[white]{self.db_path}[/white]",
                    title="📁 DATABASE AKTIF",
                    border_style="green",
                )
            )

        except Exception as e:
            console.print(
                Panel(
                    f"[bold red]Gagal membuka database:[/bold red] {e}",
                    border_style="red",
                )
            )

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

    def tambah_fotografer(self, nama, kontak, spesialisasi):
        self.cursor.execute("""
            INSERT INTO fotografer (nama, kontak, spesialisasi)
            VALUES (?, ?, ?)
        """, (nama, kontak, spesialisasi))
        self.db.commit()

        console.print(
            f"[bold green]✔ Fotografer '{nama}' berhasil ditambahkan.[/bold green]",
            style="green"
        )

    def tambah_klien(self, nama, kontak, acara):
        self.cursor.execute("""
            INSERT INTO klien (nama, kontak, acara)
            VALUES (?, ?, ?)
        """, (nama, kontak, acara))
        self.db.commit()

        console.print(
            f"[bold cyan]🤝 Klien '{nama}' berhasil disimpan.[/bold cyan]",
            style="cyan"
        )

    def tambah_sesi_foto(self, tanggal, lokasi, fotografer, klien, hasil):
        self.cursor.execute("""
            INSERT INTO sesi_foto (tanggal, lokasi, fotografer, klien, hasil)
            VALUES (?, ?, ?, ?, ?)
        """, (tanggal, lokasi, fotografer, klien, hasil))
        self.db.commit()

        console.print(
            f"[yellow]📅 Sesi foto di '{lokasi}' pada {tanggal} berhasil ditambahkan.[/yellow]"
        )

    def lihat_tabel(self, nama_tabel, kolom):
        try:
            self.cursor.execute(f"SELECT * FROM {nama_tabel}")
            hasil = self.cursor.fetchall()

            if not hasil:
                console.print(
                    Panel(f"[red]Belum ada data di tabel {nama_tabel}.[/red]", border_style="red")
                )
                return []  # kembalikan list kosong jika tidak ada data

            # Ambil nama kolom dari cursor.description jika tersedia
            desc = self.cursor.description
            if desc:
                nama_kolom_db = [d[0].capitalize() for d in desc]
            else:
                nama_kolom_db = kolom

            # Jika header yang diberikan tidak cocok dengan jumlah kolom DB, gunakan nama_kolom_db
            if len(kolom) != len(nama_kolom_db):
                headers = nama_kolom_db
            else:
                headers = kolom

            table = Table(
                title=f"📊 DATA {nama_tabel.upper()}",
                box=box.HEAVY_EDGE,
                border_style="bright_blue",
                title_style="bold cyan"
            )

            for h in headers:
                table.add_column(h, style="bold white")

            for row in hasil:
                table.add_row(*[str(x) for x in row])

            console.print(table)
            return hasil  # kembalikan hasil untuk dipakai pemanggil

        except Exception as e:
            console.print(Panel(f"[red]Gagal menampilkan tabel {nama_tabel}: {e}[/red]", border_style="red"))
            return []

    def dapatkan_nama(self, nama_tabel, id_):
        """Ambil kolom 'nama' dari tabel berdasarkan id; kembalikan None jika tidak ditemukan."""
        try:
            self.cursor.execute(f"SELECT nama FROM {nama_tabel} WHERE id = ?", (id_,))
            row = self.cursor.fetchone()
            return row[0] if row else None
        except Exception:
            return None

    def tutup(self):
        self.db.close()
        console.print(
            Panel("🔒 Koneksi database ditutup.", style="green", border_style="green")
        )


# ===============================
#  Bagian OOP
# ===============================
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


# ===============================
#  Program Utama
# ===============================
if __name__ == "__main__":
    console.print(
        Panel.fit(
            Text("📸 SISTEM MANAJEMEN STUDIO FOTOGRAFI 📸", style="bold cyan"),
            border_style="cyan",
        )
    )

    db = DatabaseManager()

    def input_non_empty(prompt_text):
        while True:
            val = input(prompt_text).strip()
            if val:
                return val
            console.print("[red]Input tidak boleh kosong.[/red]")

    def menu():
        console.print(Panel.fit(
            "\n".join([
                "[1] Tambah Fotografer",
                "[2] Tambah Klien",
                "[3] Tambah Sesi Foto",
                "[4] Lihat Tabel",
                "[5] Keluar"
            ]),
            title="📋 MENU UTAMA",
            border_style="bright_blue"
        ))

    while True:
        menu()
        pilihan = input("Pilih opsi (1-5): ").strip()

        if pilihan == "1":
            console.print(Panel("[bold]Tambah Fotografer[/bold]", border_style="green"))
            nama = input_non_empty("Nama: ")
            kontak = input_non_empty("Kontak: ")
            spesialisasi = input_non_empty("Spesialisasi: ")
            db.tambah_fotografer(nama, kontak, spesialisasi)

        elif pilihan == "2":
            console.print(Panel("[bold]Tambah Klien[/bold]", border_style="cyan"))
            nama = input_non_empty("Nama: ")
            kontak = input_non_empty("Kontak: ")
            acara = input_non_empty("Acara: ")
            db.tambah_klien(nama, kontak, acara)

        elif pilihan == "3":
            console.print(Panel("[bold]Tambah Sesi Foto[/bold]", border_style="yellow"))
            # Tampilkan fotografer dan klien agar user bisa memilih berdasarkan ID
            fotografer_rows = db.lihat_tabel("fotografer", ["ID", "Nama", "Kontak", "Spesialisasi"])
            klien_rows = db.lihat_tabel("klien", ["ID", "Nama", "Kontak", "Acara"])

            if not fotografer_rows or not klien_rows:
                console.print("[red]Tidak cukup data fotografer/klien. Tambahkan dulu sebelum membuat sesi.[/red]")
                continue

            tanggal = input_non_empty("Tanggal (misal 27 Oktober 2025): ")
            lokasi = input_non_empty("Lokasi: ")

            def pilih_id_dari(rows, prompt_text):
                valid_ids = {r[0] for r in rows}
                while True:
                    v = input(prompt_text).strip()
                    if not v.isdigit():
                        console.print("[red]Masukkan ID (angka).[/red]")
                        continue
                    idv = int(v)
                    if idv in valid_ids:
                        return idv
                    console.print("[red]ID tidak ditemukan. Cek tabel dan coba lagi.[/red]")

            fotografer_id = pilih_id_dari(fotografer_rows, "Masukkan ID Fotografer: ")
            klien_id = pilih_id_dari(klien_rows, "Masukkan ID Klien: ")

            fotografer_nama = db.dapatkan_nama("fotografer", fotografer_id)
            klien_nama = db.dapatkan_nama("klien", klien_id)

            hasil = input("Hasil / catatan (boleh kosong): ").strip()
            db.tambah_sesi_foto(tanggal, lokasi, fotografer_nama, klien_nama, hasil)

        elif pilihan == "4":
            console.print(Panel("[bold]Lihat Tabel[/bold]", border_style="magenta"))
            console.print("[1] Fotografer    [2] Klien    [3] Sesi Foto    [x] Kembali")
            sub = input("Pilih tabel: ").strip().lower()
            if sub == "1":
                db.lihat_tabel("fotografer", ["ID", "Nama", "Kontak", "Spesialisasi"])
            elif sub == "2":
                db.lihat_tabel("klien", ["ID", "Nama", "Kontak", "Acara"])
            elif sub == "3":
                db.lihat_tabel("sesi_foto", ["ID", "Tanggal", "Lokasi", "Fotografer", "Klien", "Hasil"])
            elif sub == "x":
                continue
            else:
                console.print("[red]Opsi tidak dikenal. Kembali ke menu utama.[/red]")
                continue

        elif pilihan == "5":
            break

        else:
            console.print("[red]Opsi tidak dikenal. Coba lagi.[/red]")

    db.tutup()
    console.print("\n[bold white on blue] Tekan ENTER untuk keluar... [/]")
    input()
