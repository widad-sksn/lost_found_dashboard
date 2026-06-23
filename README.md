# Lost & Found Dashboard (Odoo 17)

Modul Odoo 17 untuk manajemen pelaporan barang hilang dan penemuan barang. Modul ini dilengkapi dengan antarmuka portal publik yang responsif, *dark-mode* modern, serta dukungan dwibahasa (Bahasa Indonesia & Bahasa Inggris).

## Cara Menjalankan Proyek Ini (Untuk Developer / Teman)

Ikuti langkah-langkah di bawah ini untuk menginstal dan menjalankan modul beserta databasenya di lokal Anda.

### Prasyarat
1. **Odoo 17** sudah terinstal dan berjalan di komputer Anda.
2. **PostgreSQL** sudah terinstal.
3. Git (opsional, untuk *clone* repositori).

### Langkah 1: Pasang Modul ke Odoo
1. *Clone* atau *Download* repositori ini.
2. Pindahkan folder lost_found_dashboard ke dalam folder ddons Odoo 17 Anda.
   *Contoh path di Windows: C:\Program Files\Odoo 17.0.xxxx\server\odoo\addons\*

### Langkah 2: Restore Database
Proyek ini menggunakan database bernama hilang_temu. File backup databasenya sudah tersedia di dalam folder ini dengan nama hilang_temu_db.sql.

1. Buka terminal/Command Prompt/PowerShell.
2. Buat database kosong baru bernama hilang_temu:
   ``bash
   createdb -U odoo hilang_temu
   ``
   *(Sesuaikan username -U odoo dengan username PostgreSQL Anda)*
3. *Restore* file hilang_temu_db.sql ke dalam database tersebut:
   ``bash
   psql -U odoo -d hilang_temu -f path/to/lost_found_dashboard/hilang_temu_db.sql
   ``

### Langkah 3: Jalankan Odoo
1. *Restart* service Odoo 17 Anda.
2. Buka browser dan akses: http://localhost:8069
3. Di halaman *Database Manager* Odoo, pilih database hilang_temu.
4. Login menggunakan akun yang sudah ada di database tersebut (atau gunakan kredensial admin default Anda).

### Catatan Penting
- Jika Anda melakukan instalasi modul dari nol (tanpa *restore database*), pastikan Anda melakukan *Update Translations* (ID) di Odoo agar fitur dwibahasa berjalan sempurna.
