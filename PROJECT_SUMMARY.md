# Materi Presentasi Sistem Odoo: Modul "Lost & Found Dashboard"

Dokumen ini disusun sebagai panduan teknis bagi *programmer* untuk menjelaskan anatomi, arsitektur, dan logika pemrograman yang digunakan di balik modul `lost_found_dashboard`. Dokumen ini sangat cocok digunakan sebagai acuan saat presentasi teknis di hadapan dosen atau teman sejawat yang awam.

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

1. **`models/found_item.py` (Tabel Barang Temuan)**
   - **Tujuan:** Menyimpan data saat seseorang (misal Satpam) menemukan barang di area kampus.
   - **Isi Kode Penting:** 
     - Menyimpan `name` (Nama barang), `location` (Dropdown daftar panjang lokasi penemuan dari Gedung A sampai Taman), `date` (Tanggal ditemukan), dan `photo` (Gambar barang).
     - **Status Barang:** Diatur dengan nilai: *Draft* (Menunggu), *Approved* (Publik), *Rejected* (Ditolak), dan *Done* (Sudah Diklaim).
     - **Auto-Numbering:** Terdapat fungsi Python `create()` yang otomatis memberikan ID unik seperti `FND/001` setiap kali barang baru diinput.

2. **`models/lost_claim.py` (Tabel Laporan Kehilangan)**
   - **Tujuan:** Menyimpan laporan dari mahasiswa yang merasa kehilangan barangnya.
   - **Isi Kode Penting:**
     - Sama seperti barang temuan, menyimpan nama barang, tanggal hilang, dan lokasi perkiraan hilang.
     - **Logika Cerdas (Pencocokan Otomatis):** Terdapat fungsi `get_matching_pairs()` yang bertugas membandingkan laporan kehilangan ini dengan daftar barang temuan. Sistem akan memberi "Skor Kecocokan" berdasarkan: Lokasi sama (+40 poin), Kategori Tag sama (+30 poin), dan Kemiripan Nama (+10 poin).

3. **`models/item_claim_request.py` (Tabel Transaksi Klaim)**
   - **Tujuan:** Jembatan persetujuan. Jika barang yang hilang dan ditemukan dirasa cocok, sistem atau *user* akan membuat tiket permintaan klaim di tabel ini.
   - **Isi Kode Penting:**
     - Terdapat kolom `proof_description` di mana *user* harus menyertakan bukti (misal: "Itu dompet saya, di dalamnya ada KTP atas nama Budi").
     - **Logika Notifikasi:** Saat admin mengklik "Setujui" (`action_approve()`), Python akan memicu sistem untuk mengirimkan email otomatis ke penemu barang dan pengklaim bahwa barang sudah bisa diambil.

### B. VIEW (Direktori: `views/`)
*Fungsi: Antarmuka yang dilihat dan berinteraksi langsung dengan pengguna (Frontend).*
Ditulis dalam bahasa XML. Direktori ini bertugas mengambil data dari Model untuk ditampilkan ke layar pengguna. Modul ini memanfaatkan 3 bentuk tata letak utama Odoo:
1. **Tree View (List):** Menampilkan data berbentuk daftar baris dan kolom.
2. **Form View:** Menampilkan lembar kerja detail untuk menginput atau mengedit data suatu barang secara spesifik.
3. **Kanban View:** Menampilkan data berbentuk kartu-kartu visual (seperti papan pengumuman), sangat interaktif untuk melihat daftar barang beserta gambarnya.

**File Krusial UI/UX:**
- `views/login_templates.xml`: Berisi struktur elemen UI di mana kita telah menginjeksi *class* Bootstrap (`mx-auto`, `p-3`, `w-100`) agar portal halaman publik seperti *reset password* bersifat sangat responsif di layar ponsel (yang tadinya sempat terpotong).

### C. CONTROLLER (Direktori: `controllers/`)
*Fungsi: Jembatan Routing URL Web Publik.*
Jika direktori `views/` biasanya digunakan untuk halaman admin internal (*backend*), direktori `controllers/` (Python) menangkap permintaan (*request*) dari peramban (*browser*) untuk merender halaman *website* publik (Portal). *Controller* akan menjembatani data dari Model menuju *template* web (QWeb/XML) agar mahasiswa bisa melihat barang temuan tanpa harus *login* sebagai admin.

---

## 3. Komponen Krusial Lainnya

### File Jantung Modul: `__manifest__.py`
File ini adalah deklarasi identitas utama dari modul. Berada di akar/luar folder. Saat proses instalasi sistem, Odoo akan membaca file ini terlebih dahulu. Isinya mencakup:
- Identitas modul (nama: "Smart Lost & Found", versi: 1.0.17).
- **Dependencies:** Modul-modul bawaan Odoo yang wajib terpasang agar modul ini dapat berjalan (contoh: modul `mail` untuk notifikasi email, `portal` untuk web publik).
- **Data (Views & Security):** Daftar absolut *file* XML (seperti `views/found_item_views.xml`) yang harus dimuat oleh mesin Odoo secara berurutan saat server dinyalakan.

### Tata Kelola Hak Akses: `security/ir.model.access.csv`
File fundamental untuk sistem **Security / ACL (Access Control List)**. File ini mendefinisikan batas hak prerogatif setiap kelompok pengguna. Di file inilah sistem diinstruksikan tabel mana yang boleh di-Read (Baca), Write (Tulis), Create (Buat), atau Unlink (Hapus) oleh kelompok *user* tertentu guna mencegah mahasiswa sembarangan menghapus data barang temuan milik pihak keamanan kampus.

---

## 4. Kapabilitas Infrastruktur Ekstra
Sebagai sebuah sistem yang utuh, modul ini juga didukung oleh arsitektur infrastruktur tingkat lanjut di tingkat Server (Linux/Docker):
1. **Odoo Database Router:** Menggunakan aturan `dbfilter` di `odoo.conf` untuk memaksa *routing* langsung ke *database* utama secara otomatis.
2. **Integrated Mail Gateway:** Penyatuan sistem email Odoo dengan Postfix (SMTP Host) menggunakan *gateway* `host.docker.internal:25`, memungkinkan pengiriman email notifikasi dan *reset password* tanpa masalah.
3. **Responsive UI Architecture:** Mengimplementasikan kerangka antarmuka menggunakan aturan elastisitas SCSS pada file statis (`static/src/scss/login.scss`) yang menyesuaikan ukuran komponen agar tidak bertabrakan saat diakses di perangkat seluler berlayar kecil.
