

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

## 4. Administrasi Sistem (Server, CI/CD & Monitoring)
Selain penulisan *source code* Odoo, kelancaran aplikasi ini juga ditopang oleh administrasi *server* Ubuntu dan Docker tingkat lanjut. Berikut dokumentasi pendukungnya:

### A. Konfigurasi Mail Server (Notifikasi Email)
*Fungsi: Memastikan Odoo bisa mengirim email "Reset Password" dan pemberitahuan klaim barang ke mahasiswa.*
- **Letak File:** `deployment/config/odoo.conf`
- **Konfigurasi Teknis:** Karena Odoo terisolasi di dalam *container* Docker, sementara aplikasi pengirim email (Postfix) berada di sistem utama (Host Ubuntu), kita harus membuat jembatan komunikasi jaringan. Kita menambahkan parameter:
  ```ini
  smtp_server = host.docker.internal
  smtp_port = 25
  ```
  Sistem ini berfungsi untuk meneruskan (*forward*) semua paket email dari dalam *container* Odoo keluar menuju mesin *Host* Ubuntu Anda.

### B. Otomatisasi CI/CD (GitHub Actions)
*Fungsi: Memastikan kode yang di-push ke GitHub diuji dulu secara otomatis sebelum di-deploy ke server produksi.*
- **Letak File CI/CD:** `.github/workflows/ci-cd.yml` (di dalam repositori kode lokal/GitHub).
- **Tahap Pengujian / *Continuous Integration* (Job `test`):**
  1. **Linting (`flake8`):** Robot GitHub akan memindai *typo* atau *error syntax* penulisan pada *file-file* Python (`.py`).
  2. **Uji Kompilasi Odoo:** Robot akan menciptakan sebuah lingkungan *server virtual* singkat yang berisi Docker PostgreSQL & Odoo 17, lalu memasang modul `lost_found_dashboard` Anda di sana. Jika instalasinya menyebabkan *database crash*, kode akan ditolak.
- **Tahap Rilis / *Continuous Deployment* (Job `deploy`):**
  - Menggunakan modul `appleboy/ssh-action` untuk melakukan *remote login* secara otomatis ke *server* Ubuntu Anda.
  - Skrip perintah (`bash`) yang dijalankan oleh robot secara otomatis di dalam *server* produksi:
    1. `cd /opt/lost_found_dashboard`
    2. `git pull origin main` (Menarik kode terbaru yang sudah terverifikasi)
    3. `cd deployment`
    4. `docker compose restart web` (Me-restart kontainer Odoo untuk mengaplikasikan *update*).
- **Penyesuaian Keamanan SSH Server:**
  - **Letak File:** `/etc/ssh/sshd_config.d/60-cloudimg-settings.conf` (di dalam *server* Linux).
  - Agar robot CI/CD GitHub Action bisa masuk ke server Anda menggunakan kredensial *password* otomatis, pengaturan `PasswordAuthentication no` telah diubah secara permanen menjadi `PasswordAuthentication yes`.

### C. Sistem Monitoring (Grafana & Prometheus)
*Fungsi: Memantau kesehatan dan beban *server* (CPU, RAM, Jaringan) secara visual dan realtime.*
- **Alur Kerja:** Layanan *Node Exporter* ditanam di *server* untuk membaca suhu dan metrik mesin. Data ini dikumpulkan oleh *database* runtun waktu bernama *Prometheus*. Terakhir, *Grafana* bertugas menggambar data tersebut menjadi grafik interaktif yang bisa Anda akses di `http://monitor.lostn-found.web.id`.
- **Injeksi Datasource Grafana:** Sebelumnya Grafana selalu menampilkan masalah "No Data". Untuk memperbaikinya, telah dilakukan injeksi *script* berbasis API JSON yang secara paksa mengunci *Datasource* pada *dashboard* utama ("Node Exporter Full") langsung menuju *Unique ID* (UID) mutlak milik Prometheus (`efq30lnjdnnk0e`), sehingga grafik kini menyala dengan sempurna secara presisi.
