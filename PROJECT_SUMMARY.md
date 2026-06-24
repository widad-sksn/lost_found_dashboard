# Materi Presentasi Sistem Odoo: Modul "Lost & Found Dashboard"

Dokumen ini disusun sebagai panduan teknis bagi *programmer* untuk menjelaskan anatomi, arsitektur, dan logika pemrograman yang digunakan di balik modul `lost_found_dashboard`. Dokumen ini sangat cocok digunakan sebagai acuan saat presentasi teknis di hadapan dosen atau tim penilai.

---

## 1. Konsep Dasar Sistem (Framework Odoo)
Modul "Lost & Found Dashboard" dibangun menggunakan kerangka kerja (*framework*) **Odoo 17** yang secara fundamental menganut pola arsitektur **MVC (Model-View-Controller)**.

Sistem ini tidak menggunakan *query* SQL manual untuk berinteraksi dengan *database*. Odoo memanfaatkan teknologi **ORM (*Object-Relational Mapping*)**, di mana setiap tabel di *database* direpresentasikan sebagai sebuah Objek (Class) dalam bahasa Python.

**Bahasa & Teknologi yang Digunakan:**
- **Python (Backend/Logika):** Digunakan untuk membangun Model (struktur tabel *database*) dan mengatur logika bisnis.
- **XML (Frontend/Struktur Visual):** Digunakan sebagai *markup language* untuk membangun kerangka tata letak antarmuka pengguna (*form*, tabel, *kanban*).
- **PostgreSQL (Database Server):** Sistem manajemen *database* relasional yang menyimpan seluruh data yang diproses oleh Python.
- **SCSS/CSS & Bootstrap (Desain UI):** Digunakan untuk memberikan penataan visual (*styling*) agar antarmuka aplikasi menjadi responsif (*mobile-friendly*).

---

## 2. Membedah Anatomi Folder Modul (Arsitektur MVC)

Sebagai sistem berbasis MVC, modul ini memiliki struktur direktori yang memisahkan tugas pengolahan data, tampilan, dan logika rute.

### A. MODEL (Direktori: `models/`)
*Fungsi: Mendefinisikan tabel di database dan logika bisnis (Backend).*
Ditulis murni dalam bahasa Python. File di dalam direktori ini otomatis dikonversi oleh ORM Odoo menjadi tabel-tabel di dalam PostgreSQL.
- **`found_item.py`**: Mendefinisikan tabel barang temuan. Menyimpan kolom-kolom seperti nama barang, foto, lokasi ditemukan, dan tanggal penemuan.
- **`lost_claim.py`**: Mendefinisikan tabel untuk mencatat laporan *user* yang kehilangan barang.
- **`item_claim_request.py`**: Merupakan tabel transaksional penghubung antara pihak yang kehilangan (*Claimer*) dengan barang temuan. Menangani logika status persetujuan klaim: *Draft* (menunggu), *Approved* (disetujui), atau *Rejected* (ditolak).
- **`item_tag.py`**: Tabel relasional sederhana untuk mengkategorikan barang (contoh: "Elektronik", "Dompet", "Dokumen").

### B. VIEW (Direktori: `views/`)
*Fungsi: Antarmuka yang dilihat dan berinteraksi langsung dengan pengguna (Frontend).*
Ditulis dalam bahasa XML. Direktori ini bertugas mengambil data dari Model untuk ditampilkan ke layar pengguna. Modul ini memanfaatkan 3 bentuk tata letak utama Odoo:
1. **Tree View (List):** Menampilkan data berbentuk daftar baris dan kolom.
2. **Form View:** Menampilkan lembar kerja detail untuk menginput atau mengedit data suatu barang secara spesifik.
3. **Kanban View:** Menampilkan data berbentuk kartu-kartu visual (seperti papan pengumuman), sangat interaktif untuk melihat daftar barang beserta gambarnya.
- *Catatan Khusus:* Terdapat file `login_templates.xml` di mana struktur elemen UI dimodifikasi menggunakan *class* Bootstrap (`mx-auto`, `p-3`, `w-100`) agar portal halaman publik seperti reset password bersifat responsif di layar ponsel.

### C. CONTROLLER (Direktori: `controllers/`)
*Fungsi: Jembatan Routing URL Web Publik.*
Jika direktori `views/` biasanya digunakan untuk halaman admin internal (*backend*), direktori `controllers/` (Python) menangkap permintaan (*request*) dari peramban (*browser*) untuk merender halaman *website* publik (Portal). *Controller* akan menjembatani Model menuju *template* web (QWeb/XML).

---

## 3. Komponen Krusial Lainnya

### File Jantung Modul: `__manifest__.py`
File ini adalah deklarasi identitas utama dari modul. Saat proses instalasi sistem, Odoo akan membaca file ini terlebih dahulu. Isinya mencakup:
- Identitas modul (nama, deskripsi, *author*, versi).
- **Dependencies:** Modul-modul prasyarat yang wajib terpasang agar modul ini dapat berjalan (contoh: modul `base`, `mail`).
- **Data (Views & Security):** Daftar absolut *file* XML yang harus dimuat oleh mesin Odoo secara berurutan.

### Tata Kelola Hak Akses: `security/ir.model.access.csv`
File fundamental untuk sistem **Security / ACL (Access Control List)**. File ini mendefinisikan batas hak prerogatif setiap kelompok pengguna (Admin, Staf, Mahasiswa). Di file inilah sistem diinstruksikan tabel mana yang boleh di-Read (Baca), Write (Tulis), Create (Buat), atau Unlink (Hapus) oleh kelompok *user* tertentu guna mencegah manipulasi data ilegal.

---

## 4. Kapabilitas Infrastruktur Ekstra
Sebagai sebuah sistem yang utuh, modul ini juga didukung oleh arsitektur infrastruktur tingkat lanjut di tingkat Server (Linux/Docker):
1. **Odoo Database Router:** Menggunakan aturan `dbfilter` di `odoo.conf` untuk memaksa *routing* langsung ke *database* utama secara otomatis.
2. **Integrated Mail Gateway:** Penyatuan sistem email Odoo dengan Postfix (SMTP Host) menggunakan `host.docker.internal:25`, memungkinkan pengiriman email notifikasi dan reset password.
3. **Responsive UI Architecture:** Mengimplementasikan kerangka antarmuka menggunakan aturan elastisitas SCSS pada file statis (`static/src/scss/login.scss`) yang menyesuaikan otomatis di seluruh ukuran perangkat genggam.
