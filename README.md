# Smart Lost & Found — Odoo 17 Module

Modul ERP berbasis **Odoo 17** untuk manajemen pelaporan barang hilang dan penemuan barang di lingkungan kampus. Dilengkapi dengan portal publik responsif, *dark-mode* modern, dukungan dwibahasa (Indonesia & Inggris), serta sistem pencocokan otomatis (*auto-matching*) antara barang hilang dan barang temuan.

---

## Daftar Isi
1. [Teknologi yang Digunakan](#1-teknologi-yang-digunakan)
2. [Arsitektur Sistem (MVC)](#2-arsitektur-sistem-mvc)
3. [Struktur Direktori & Penjelasan File](#3-struktur-direktori--penjelasan-file)
4. [Administrasi Sistem](#4-administrasi-sistem-server-cicd--monitoring)
5. [Cara Menjalankan di Lokal](#5-cara-menjalankan-di-lokal-untuk-developer)

---

## 1. Teknologi yang Digunakan

| Teknologi | Peran |
|---|---|
| **Python 3.10** | Bahasa utama untuk logika bisnis (*backend*), struktur tabel *database* (ORM), dan routing URL |
| **XML (QWeb)** | *Markup language* untuk membangun antarmuka pengguna Odoo (formulir, tabel, kartu *kanban*, menu) |
| **PostgreSQL 15** | Sistem manajemen *database* relasional yang menyimpan seluruh data aplikasi |
| **SCSS / CSS** | Preprosesor *stylesheet* untuk membuat tampilan (*frontend*) responsif dan modern |
| **Bootstrap 5** | *Framework* CSS untuk tata letak kolom, tombol, dan elemen UI yang responsif di perangkat *mobile* |
| **JavaScript (OWL)** | Digunakan untuk membangun *dashboard* pencocokan barang secara interaktif di *backend* |
| **Docker & Docker Compose** | Kontainerisasi seluruh aplikasi (Odoo, PostgreSQL, Nginx, Grafana, Prometheus) di *server* produksi |
| **Nginx** | *Reverse proxy* web *server* yang meneruskan permintaan *browser* ke kontainer Odoo |
| **Cloudflare** | *CDN & Reverse Proxy* untuk enkripsi HTTPS (SSL/TLS), perlindungan DDoS, dan penyembunyian IP *server* |
| **GitHub Actions** | Platform CI/CD untuk otomatisasi pengujian kode dan *deployment* ke *server* |
| **Grafana & Prometheus** | Sistem *monitoring* kesehatan *server* (CPU, RAM, jaringan) secara *real-time* |

Odoo menggunakan teknologi **ORM (*Object-Relational Mapping*)**, di mana setiap tabel di *database* direpresentasikan sebagai Class Python. Dengan ORM, kita tidak perlu menulis *query* SQL manual — cukup mendefinisikan `fields` di Python, dan Odoo otomatis membuatkan tabel beserta kolomnya di PostgreSQL.

---

## 2. Arsitektur Sistem (MVC)

Modul ini menganut pola arsitektur **Model-View-Controller (MVC)** yang membagi sistem menjadi 3 lapisan terpisah:

```
┌─────────────────────────────────────────────────────────┐
│                      BROWSER                            │
│          (Mahasiswa / Admin / Satpam)                    │
└──────────────────────┬──────────────────────────────────┘
                       │
          ┌────────────▼────────────┐
          │   CONTROLLER (Python)   │  ← Menangkap URL request
          │   controllers/main.py   │
          └────────────┬────────────┘
                       │
        ┌──────────────▼──────────────┐
        │       MODEL (Python)        │  ← Logika bisnis & ORM
        │   models/found_item.py      │
        │   models/lost_claim.py      │
        │   models/item_claim_request.py│
        └──────────────┬──────────────┘
                       │
          ┌────────────▼────────────┐
          │     VIEW (XML/QWeb)     │  ← Tampilan antarmuka
          │   views/*_views.xml     │
          │   views/portal_templates│
          └─────────────────────────┘
```

- **Model** → Otak sistem. Mendefinisikan struktur tabel dan logika bisnis.
- **View** → Wajah sistem. Menampilkan data ke layar pengguna.
- **Controller** → Jembatan. Menghubungkan URL *browser* dengan Model dan View.

---

## 3. Struktur Direktori & Penjelasan File

```
lost_found_dashboard/
│
├── __manifest__.py              # Identitas & registrasi modul
├── __init__.py                  # Inisialisasi package Python
│
├── models/                      # MODEL — Struktur database & logika bisnis
│   ├── __init__.py
│   ├── found_item.py            # Tabel barang temuan
│   ├── lost_claim.py            # Tabel laporan kehilangan + Auto-Match
│   ├── item_claim_request.py    # Tabel transaksi klaim barang
│   └── item_tag.py              # Tabel kategori/label barang
│
├── views/                       # VIEW — Antarmuka pengguna (XML)
│   ├── menu_views.xml           # Definisi menu navigasi sidebar
│   ├── found_item_views.xml     # Form, List, Kanban barang temuan
│   ├── lost_claim_views.xml     # Form, List, Kanban laporan hilang
│   ├── item_claim_request_views.xml # Form & List permintaan klaim
│   ├── portal_templates.xml     # Halaman portal publik (website)
│   └── login_templates.xml      # Kustomisasi halaman login & reset password
│
├── controllers/                 # CONTROLLER — Routing URL publik
│   ├── __init__.py
│   ├── main.py                  # Route halaman portal publik
│   └── api.py                   # Endpoint API untuk dashboard
│
├── security/                    # Hak akses & aturan keamanan data
│   ├── security.xml             # Definisi grup pengguna
│   ├── security_rules.xml       # Record rules (pembatasan data per user)
│   └── ir.model.access.csv      # ACL: hak CRUD per grup pengguna
│
├── static/src/                  # Aset statis (CSS, JS, gambar)
│   ├── scss/
│   │   ├── login.scss           # Styling halaman login (responsif mobile)
│   │   ├── portal_theme.scss    # Tema portal publik (dark-mode)
│   │   ├── backend_theme.scss   # Tema backend admin
│   │   └── item_matching_dashboard.scss  # Styling dashboard pencocokan
│   ├── js/
│   │   └── item_matching_dashboard.js    # Logika dashboard OWL component
│   ├── xml/
│   │   └── item_matching_dashboard.xml   # Template dashboard pencocokan
│   └── img/                     # Gambar dan ikon
│
├── data/                        # Data bawaan modul
│   ├── mail_templates.xml       # Template email notifikasi otomatis
│   └── student_users.xml        # Data user mahasiswa awal
│
├── i18n/                        # File terjemahan (dwibahasa)
│
├── deployment/                  # Konfigurasi deployment server
│   ├── config/
│   │   └── odoo.conf            # Konfigurasi Odoo (DB filter, SMTP)
│   ├── nginx/
│   │   └── nginx.conf           # Konfigurasi reverse proxy & HTTPS redirect
│   ├── prometheus/
│   │   └── prometheus.yml       # Konfigurasi pengumpul metrik server
│   ├── ssl/                     # Sertifikat SSL (jika ada)
│   └── docker-compose.yml       # Orkestrasi semua container Docker
│
└── .github/workflows/
    └── ci-cd.yml                # Pipeline CI/CD GitHub Actions
```

### Detail File-File Kunci

#### `__manifest__.py` — Identitas Modul
File pertama yang dibaca Odoo saat instalasi. Berisi:
- **Nama modul:** "Smart Lost & Found"
- **Versi:** 1.0.17
- **Dependencies:** `base`, `mail`, `portal`, `website`, `auth_signup`
- **Data:** Daftar urutan file XML yang harus dimuat saat server dinyalakan
- **Assets:** Registrasi file SCSS, JS, dan XML untuk frontend dan backend

#### `models/found_item.py` — Tabel Barang Temuan
- Menyimpan: nama barang (`name`), lokasi penemuan (`location` — dropdown 80+ lokasi kampus), tanggal (`date`), foto (`photo`), dan status.
- **Status alur:** `Draft` → `Approved` → `Done` (Diklaim)
- **Auto-Numbering:** Fungsi `create()` otomatis memberi ID unik format `FND/001`, `FND/002`, dst.
- **Email Otomatis:** Setiap perubahan status memicu pengiriman email notifikasi ke pelapor.

#### `models/lost_claim.py` — Tabel Laporan Kehilangan
- Menyimpan data dari mahasiswa yang kehilangan barang.
- **Fitur Unggulan — Algoritma Auto-Match (`get_matching_pairs()`):**
  Fungsi ini membandingkan setiap laporan kehilangan dengan setiap barang temuan, lalu memberikan *Skor Kecocokan* berdasarkan:
  - Lokasi sama: **+40 poin**
  - Kategori/Tag sama: **+30 poin**
  - Rentang waktu ≤ 7 hari: **+20 poin**
  - Kemiripan nama barang: **+10 poin**
  Hasil pencocokan diurutkan dari skor tertinggi ke terendah.

#### `models/item_claim_request.py` — Tabel Transaksi Klaim
- Jembatan persetujuan antara pengklaim dan barang.
- Kolom `proof_description`: pengguna wajib menyertakan bukti kepemilikan.
- Kolom `photo_proof`: foto bukti pendukung.
- **Logika `action_approve()`:** Saat admin menyetujui klaim, Python akan:
  1. Mengubah status klaim menjadi "Diterima"
  2. Mengirim email ke pengklaim
  3. Mengirim email ke penemu asli
  4. Mengubah status barang temuan menjadi "Done"

#### `models/item_tag.py` — Tabel Kategori Barang
- Tabel sederhana untuk label/tag barang (misal: "Elektronik", "Dokumen", "Dompet").
- Memiliki atribut `color` untuk pemberian warna pada *badge* tag di tampilan *kanban*.

#### `security/ir.model.access.csv` — Hak Akses (ACL)
- Mengatur hak CRUD (*Create, Read, Update, Delete*) per grup pengguna.
- Contoh: Mahasiswa hanya bisa *Read* (melihat), Admin/Satpam bisa *Create*, *Update*, dan *Delete*.

#### `deployment/config/odoo.conf` — Konfigurasi Server Odoo
- `dbfilter = ^hilang_temu$` → Memaksa Odoo langsung terhubung ke database utama tanpa halaman pilih database.
- `smtp_server = host.docker.internal` & `smtp_port = 25` → Menjembatani Odoo (dalam Docker) ke Postfix (di Host Ubuntu) agar email bisa terkirim.

#### `deployment/nginx/nginx.conf` — Reverse Proxy & HTTPS
- Meneruskan request dari port 80 ke kontainer Odoo (port 8069) dan Grafana (port 3000).
- Mengecek header `X-Forwarded-Proto` dari Cloudflare: jika bukan `https`, paksa redirect ke `https://`.
- Mendukung WebSocket untuk fitur *live chat/bus* Odoo.

#### `.github/workflows/ci-cd.yml` — Pipeline CI/CD
- **Job `test` (Continuous Integration):**
  1. Linting Python dengan `flake8` — mendeteksi syntax error
  2. Uji kompilasi: menjalankan Docker Odoo 17 + PostgreSQL, lalu menginstal modul secara virtual
- **Job `deploy` (Continuous Deployment):**
  - Hanya berjalan jika `test` berhasil 100%
  - SSH ke server → `git pull` → `docker compose restart web`

---

## 4. Administrasi Sistem (Server, CI/CD & Monitoring)

### A. Mail Server (Notifikasi Email)
- **Letak File:** `deployment/config/odoo.conf`
- Odoo terisolasi di dalam kontainer Docker, sementara Postfix (pengirim email) berjalan di Host Ubuntu. Untuk menghubungkannya, kita menggunakan *gateway* Docker `host.docker.internal:25` yang meneruskan semua paket email keluar dari kontainer menuju Host.

### B. CI/CD Pipeline (GitHub Actions)
- **Letak File:** `.github/workflows/ci-cd.yml`
- Setiap `git push` ke branch `main` akan memicu robot GitHub untuk:
  1. Memindai kualitas kode Python (linting)
  2. Menguji instalasi modul di lingkungan virtual (Docker)
  3. Jika lulus → deploy otomatis ke server via SSH
- **Penyesuaian SSH:** File `/etc/ssh/sshd_config.d/60-cloudimg-settings.conf` di server diubah menjadi `PasswordAuthentication yes` agar robot CI/CD bisa login.

### C. Monitoring (Grafana & Prometheus)
- **URL Akses:** `https://monitor.lostn-found.web.id`
- **Alur:** Node Exporter (pembaca metrik mesin) → Prometheus (pengumpul data) → Grafana (visualisasi grafik CPU, RAM, jaringan)
- Dashboard "Node Exporter Full" di-*hardcode* datasource-nya ke UID Prometheus (`efq30lnjdnnk0e`) agar grafik langsung menyala tanpa konfigurasi manual.

### D. Keamanan Jaringan (Cloudflare)
Terdapat 3 alasan teknis mengapa proyek ini menggunakan Cloudflare:
1. **Enkripsi HTTPS (SSL/TLS):** Nginx internal hanya memancarkan HTTP (port 80). Cloudflare membungkus trafik tersebut menjadi HTTPS (gembok hijau), sehingga *password* dan data mahasiswa terenkripsi aman dari penyadapan.
2. **Reverse Proxy & Penyembunyian IP:** IP publik server Ubuntu disembunyikan di balik jaringan Cloudflare, mencegah serangan DDoS langsung ke server kampus.
3. **HTTP → HTTPS Redirect:** Nginx diprogram untuk membaca header `X-Forwarded-Proto` dari Cloudflare. Jika pengguna mengakses via `http://`, Nginx secara paksa membelokkan ke `https://`.

---

## 5. Cara Menjalankan di Lokal (Untuk Developer)

### Prasyarat
- **Odoo 17** sudah terinstal dan berjalan di komputer Anda.

### Langkah 1: Pasang Modul ke Odoo
1. *Clone* atau *Download* repositori ini.
2. Pindahkan folder `lost_found_dashboard` ke dalam folder `addons` Odoo 17 Anda.
   Contoh path di Windows: `C:\Program Files\Odoo 17.0.xxxx\server\odoo\addons\`
3. *Restart* service Odoo 17 agar mendeteksi modul baru.

### Langkah 2: Restore Database
1. Buka browser dan akses: `http://localhost:8069/web/database/manager`
2. Klik tombol **Restore Database**.
3. Pada kolom **File**, pilih file `hilang_temu_db.sql` dari folder repositori ini.
4. Pada kolom **Database Name**, ketikkan: `hilang_temu`
5. Masukkan **Master Password** Odoo Anda.
6. Klik **Continue** dan tunggu hingga proses *restore* selesai.

### Langkah 3: Selesai!
1. Buka browser dan akses: `http://localhost:8069`
2. Login menggunakan akun yang sudah ada di database tersebut.
