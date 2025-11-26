
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

class View:

    @staticmethod
    def header():
        console.print(
            Panel.fit(
                Text("📸 SISTEM MANAJEMEN STUDIO FOTOGRAFI 📸", style="bold cyan"),
                border_style="cyan",
            )
        )

    @staticmethod
    def show_menu():
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

    @staticmethod
    def alert(msg, color="red"):
        console.print(f"[{color}]{msg}[/{color}]")

    @staticmethod
    def table(title, headers, rows):
        table = Table(
            title=f"📊 {title}",
            box=box.HEAVY_EDGE,
            border_style="bright_blue",
            title_style="bold cyan"
        )

        for h in headers:
            table.add_column(h, style="bold white")

        for r in rows:
            table.add_row(*(str(c) for c in r))

        console.print(table)
