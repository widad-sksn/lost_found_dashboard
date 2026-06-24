tes cicdd
 
 
 # Lost & Found Dashboard (Odoo 17)

Modul Odoo 17 untuk manajemen pelaporan barang hilang dan penemuan barang. Modul ini dilengkapi dengan antarmuka portal publik yang responsif, *dark-mode* modern, serta dukungan dwibahasa (Bahasa Indonesia & Bahasa Inggris).

## Cara Menjalankan Proyek Ini (Untuk Developer / Teman)

Ikuti langkah-langkah di bawah ini untuk menginstal dan menjalankan modul beserta databasenya di lokal Anda.

### Prasyarat
1. **Odoo 17** sudah terinstal dan berjalan di komputer Anda.

### Langkah 1: Pasang Modul ke Odoo
1. *Clone* atau *Download* repositori ini.
2. Pindahkan folder lost_found_dashboard ke dalam folder ddons Odoo 17 Anda.
   *Contoh path di Windows: C:\Program Files\Odoo 17.0.xxxx\server\odoo\addons\*
3. *Restart* service Odoo 17 Anda agar mendeteksi modul baru.

### Langkah 2: Restore Database via Odoo (Cara Paling Mudah)
Proyek ini menggunakan database bernama hilang_temu. File backup databasenya sudah tersedia di dalam folder ini dengan nama hilang_temu_db.sql. Anda bisa melakukan *restore* langsung melalui tampilan web Odoo:

1. Buka browser dan akses: http://localhost:8069/web/database/manager
2. Klik tombol **Restore Database**.
3. Pada kolom **File**, pilih file hilang_temu_db.sql yang ada di folder repositori ini.
4. Pada kolom **Database Name**, ketikkan nama: hilang_temu (atau nama lain yang Anda inginkan).
5. Masukkan **Master Password** Odoo Anda.
6. Klik **Continue** dan tunggu hingga proses *restore* selesai.

*(Alternatif untuk Developer: Anda juga bisa melakukan restore via terminal/Command Prompt menggunakan perintah psql -U odoo -d hilang_temu -f hilang_temu_db.sql)*

### Langkah 3: Selesai!
1. Buka browser dan akses: http://localhost:8069
2. Pilih database yang baru saja di-*restore*.
3. Login menggunakan akun yang sudah ada di database tersebut.
