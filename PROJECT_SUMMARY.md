# Dokumentasi Teknis Odoo: Modul "Lost & Found Dashboard"

Selamat datang! Dokumen ini disusun khusus dari sudut pandang *Odoo Programmer* untuk membedah anatomi, arsitektur, dan bahasa pemrograman yang digunakan di balik modul `lost_found_dashboard`.

---

## 1. Arsitektur Pemrograman Odoo
Sebagai kerangka kerja (*framework*), Odoo menggunakan arsitektur **Model-View-Controller (MVC)** klasik yang sangat terstruktur. Seluruh logika dan alur sistem dibangun dengan kombinasi berbagai bahasa pemrograman berikut:

### A. Python (Logika Backend & Model)
Python adalah "otak" dari sistem ini. Semua logika bisnis, hak akses, validasi data, hingga komunikasi dengan *database* ditulis menggunakan bahasa Python 3.10. Odoo memanfaatkan teknik *Object-Relational Mapping* (ORM) sehingga kita tidak perlu menulis query SQL secara manual.
- **Contoh Penggunaan:** Memvalidasi apakah barang yang hilang sudah diklaim, atau membuat perhitungan otomatis.

### B. XML (Struktur Antarmuka & View)
Jika HTML digunakan di *web browser* standar, Odoo menggunakan XML sebagai bahasa *markup* untuk merancang tampilan aplikasinya (halaman formulir, daftar tabel, *kanban*, menu, dll).
- **Contoh Penggunaan:** `login_templates.xml` dirancang menggunakan struktur tata letak XML yang memanggil *class* Bootstrap untuk membuat tombol atau kotak *input*.

### C. SCSS / CSS (Desain Visual & Styling)
Untuk memberikan tampilan (*User Interface*) yang lebih cantik dan responsif (terutama pada halaman *frontend* atau portal), Odoo menggunakan preprosesor CSS yaitu SCSS.
- **Contoh Penggunaan:** `login.scss` yang kita ubah untuk menghilangkan `overflow: hidden` dan menambahkan elastisitas `min-height` agar tampilan selaras di HP.

### D. PostgreSQL (Database Server)
Semua struktur data yang kita bangun di Python secara otomatis diterjemahkan menjadi tabel-tabel di *database* PostgreSQL. Ini adalah jantung penyimpanan data Odoo yang sangat tangguh.

---

## 2. Pembedahan Struktur Folder Modul
Berikut adalah struktur anatomi dalam modul `lost_found_dashboard` Anda beserta peran krusialnya:

### 📁 `models/` (Python)
Folder ini menampung "Buku Besar" atau kerangka dasar *database*. Di sinilah kita mendefinisikan objek-objek utama:
- `found_item.py`: Mengatur tabel untuk barang-barang yang ditemukan.
- `lost_claim.py`: Mengatur tabel dan status laporan barang hilang.
- `item_claim_request.py`: Menghubungkan logika transaksi saat seseorang mengklaim sebuah barang.
- `item_tag.py`: Label/kategori tambahan untuk barang.

### 📁 `views/` (XML)
Tempat di mana wajah aplikasi dibentuk. File-file di sini mengatur bagaimana data dari `models` ditampilkan kepada *user*. 
- Di sinilah letak file `login_templates.xml` yang baru saja kita bedah strukturnya, memperbaiki *layout max-width*, dan menambahkan atribut Bootstrap seperti `w-100 m-auto p-3 p-md-4` agar responsif.

### 📁 `static/src/scss/` (SCSS/CSS)
Direktori statis untuk memoles tampilan. Di dalamnya terdapat file `login.scss` tempat kita mematikan (*override*) pengaturan Odoo bawaan yang membatasi *scroll* pada halaman pengguna (terutama pada *form Reset Password*).

### 📁 `controllers/` (Python)
Mengatur *routing* URL web. Jika `models` digunakan untuk *backend* staf/karyawan, `controllers` mengatur halaman yang diakses publik atau portal eksternal via URL (seperti halaman web publik Odoo).

### 📁 `security/` (XML/CSV)
Menangani tata kelola hak akses pengguna. Di sini ditentukan tabel mana yang boleh dibaca (*read*), diisi (*write*), dibuat (*create*), atau dihapus (*unlink*) oleh grup *user* tertentu.

### 📁 `deployment/config/` (Konfigurasi Server)
Folder ekstra yang kita kelola untuk menyelaraskan *environment* server, memuat dua file sakti:
- `odoo.conf`: Menjembatani sistem dengan server. Di sini kita mengatur filter `dbfilter = ^hilang_temu$` (memaksa akses langsung ke *database*) dan membuka gerbang SMTP Postfix melalui `host.docker.internal:25` agar sistem email aktif.
- `docker-compose.yml`: Arsitektur *container* server Anda secara keseluruhan.

---

## 3. Kapabilitas Infrastruktur Saat Ini
Sebagai sebuah sistem yang utuh, modul ini telah dilengkapi dengan arsitektur infrastruktur tingkat lanjut:
1. **Odoo Database Router:** Menggunakan aturan `dbfilter` di `.conf` untuk memaksa koneksi langsung ke *database* utama secara otomatis.
2. **Integrated Mail Gateway:** Penyatuan sistem email Odoo dengan SMTP Host menggunakan `host.docker.internal:25`, memungkinkan pengiriman email notifikasi dan tautan otentikasi.
3. **Responsive UI Architecture:** Mengimplementasikan kerangka elemen antarmuka yang sangat responsif (*mobile-friendly*) menggunakan struktur *wrapper* XML dan aturan elastisitas SCSS yang menyesuaikan otomatis di seluruh perangkat.

*Catatan: Dokumen ini merangkum arsitektur pemrograman Odoo dan sistem internal modul.*
