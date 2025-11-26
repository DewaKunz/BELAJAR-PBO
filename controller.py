from model import DatabaseManager
from view import View

class Controller:
    def __init__(self, db: DatabaseManager, view: View):
        self.db = db
        self.view = view

    def input_non_empty(self, prompt_text):
        while True:
            v = input(prompt_text).strip()
            if v:
                return v
            self.view.alert("Input tidak boleh kosong.")

    def tambah_fotografer(self):
        nama = self.input_non_empty("Nama: ")
        kontak = self.input_non_empty("Kontak: ")
        spesialisasi = self.input_non_empty("Spesialisasi: ")

        self.db.tambah("fotografer", {
            "nama": nama,
            "kontak": kontak,
            "spesialisasi": spesialisasi
        })

        self.view.alert(f"✔ Fotografer '{nama}' ditambahkan.", "green")

    def tambah_klien(self):
        nama = self.input_non_empty("Nama: ")
        kontak = self.input_non_empty("Kontak: ")
        acara = self.input_non_empty("Acara: ")

        self.db.tambah("klien", {
            "nama": nama,
            "kontak": kontak,
            "acara": acara
        })

        self.view.alert(f"🤝 Klien '{nama}' ditambahkan.", "cyan")

    def tambah_sesi(self):
        fotografer = self.db.ambil_semua("fotografer")
        klien = self.db.ambil_semua("klien")

        if not fotografer or not klien:
            self.view.alert("Data fotografer/klien belum cukup.")
            return

        self.view.table("DATA FOTOGRAFER", ["ID", "Nama", "Kontak", "Spesialisasi"], fotografer)
        self.view.table("DATA KLIEN", ["ID", "Nama", "Kontak", "Acara"], klien)

        tanggal = self.input_non_empty("Tanggal: ")
        lokasi = self.input_non_empty("Lokasi: ")

        fid = int(self.input_non_empty("ID Fotografer: "))
        kid = int(self.input_non_empty("ID Klien: "))

        hasil = input("Catatan (opsional): ").strip()

        self.db.tambah("sesi_foto", {
            "tanggal": tanggal,
            "lokasi": lokasi,
            "fotografer_id": fid,
            "klien_id": kid,
            "hasil": hasil
        })

        self.view.alert("📅 Sesi foto berhasil ditambahkan.", "yellow")

    def lihat_tabel(self):
        print("\n[1] Fotografer\n[2] Klien\n[3] Sesi Foto\n[x] Kembali")
        p = input("Pilih tabel: ").strip()

        if p == "1":
            data = self.db.ambil_semua("fotografer")
            self.view.table("FOTOGRAFER", ["ID","Nama","Kontak","Spesialisasi"], data)

        elif p == "2":
            data = self.db.ambil_semua("klien")
            self.view.table("KLIEN", ["ID","Nama","Kontak","Acara"], data)

        elif p == "3":
            # JOIN (menampilkan nama fotografer & klien)
            self.db.cursor.execute("""
                SELECT s.id, s.tanggal, s.lokasi,
                       f.nama AS fotografer,
                       k.nama AS klien,
                       s.hasil
                FROM sesi_foto s
                JOIN fotografer f ON s.fotografer_id = f.id
                JOIN klien k ON s.klien_id = k.id
            """)
            data = self.db.cursor.fetchall()

            self.view.table("SESI FOTO", ["ID","Tanggal","Lokasi","Fotografer","Klien","Hasil"], data)

    def run(self):
        while True:
            self.view.show_menu()
            choice = input("Pilih opsi (1-5): ").strip()

            if choice == "1":
                self.tambah_fotografer()
            elif choice == "2":
                self.tambah_klien()
            elif choice == "3":
                self.tambah_sesi()
            elif choice == "4":
                self.lihat_tabel()
            elif choice == "5":
                break
            else:
                self.view.alert("Opsi tidak dikenali.")
