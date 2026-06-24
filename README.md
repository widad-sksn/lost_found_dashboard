# Smart Lost & Found — Odoo 17 Module

Modul ERP berbasis **Odoo 17** untuk manajemen pelaporan barang hilang dan penemuan barang di lingkungan kampus. Dilengkapi dengan portal publik responsif, *dark-mode* modern, dukungan dwibahasa (Indonesia & Inggris), serta sistem pencocokan otomatis (*auto-matching*) antara barang hilang dan barang temuan.

---

## Daftar Isi
1. [Teknologi yang Digunakan](#1-teknologi-yang-digunakan)
2. [Arsitektur Sistem (MVC)](#2-arsitektur-sistem-mvc)
3. [Struktur Direktori & Penjelasan File](#3-struktur-direktori--penjelasan-file)
4. [Administrasi Sistem](#4-administrasi-sistem-server-cicd--monitoring)

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

### A. Mail Server (Notifikasi Email & Reset Password)

Agar Odoo dapat mengirimkan email (notifikasi klaim, reset password, dsb), diperlukan konfigurasi di dua sisi: **Odoo (dalam Docker)** dan **Postfix (di Host Ubuntu)**.

#### Sisi Odoo — File: `deployment/config/odoo.conf`
```ini
[options]
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
data_dir = /var/lib/odoo
admin_passwd = admin
# Proxy configuration
proxy_mode = True
# Logging
logfile = /var/log/odoo/odoo-server.log
# SMTP
smtp_server = host.docker.internal
smtp_port = 25
# DB Filter
dbfilter = ^hilang_temu$
```

Penjelasan baris per baris:
- `addons_path` → Lokasi folder modul Odoo di dalam kontainer Docker.
- `proxy_mode = True` → Mengaktifkan mode proxy agar Odoo percaya header dari Nginx/Cloudflare (X-Forwarded-For, X-Forwarded-Proto).
- `smtp_server = host.docker.internal` → Alamat khusus Docker yang mengarah ke mesin Host (Ubuntu). Karena Postfix berjalan di Host, bukan di dalam kontainer, maka Odoo harus menggunakan alamat ini sebagai jembatan.
- `smtp_port = 25` → Port standar SMTP tanpa enkripsi (aman karena komunikasi hanya terjadi secara internal antara Docker dan Host).
- `dbfilter = ^hilang_temu$` → Regex yang memaksa Odoo langsung memilih database `hilang_temu` tanpa menampilkan halaman pilih database.

#### Sisi Host Ubuntu — Konfigurasi Postfix
Postfix adalah aplikasi MTA (*Mail Transfer Agent*) yang terinstal langsung di sistem operasi Ubuntu server. Konfigurasi utamanya berada di:

**File: `/etc/postfix/main.cf`**
```ini
smtpd_banner = $myhostname ESMTP $mail_name
biff = no
append_dot_mydomain = no

myhostname = lostn-found.web.id
mydomain = lostn-found.web.id
myorigin = $mydomain
mydestination = $myhostname, localhost.$mydomain, localhost
relayhost =
mynetworks = 127.0.0.0/8 172.16.0.0/12 [::1]/128
inet_interfaces = all
inet_protocols = ipv4

mailbox_size_limit = 0
recipient_delimiter = +
```

Penjelasan kunci:
- `myhostname = lostn-found.web.id` → Identitas pengirim email. Email yang keluar akan berformat `noreply@lostn-found.web.id`.
- `mynetworks = 127.0.0.0/8 172.16.0.0/12` → Mengizinkan koneksi SMTP dari localhost DAN dari jaringan internal Docker (subnet `172.16.x.x`). Tanpa baris ini, Postfix akan menolak email dari kontainer Odoo.
- `inet_interfaces = all` → Mendengarkan koneksi di semua *network interface*, termasuk `docker0`.

**Alur pengiriman email:**
```
Odoo (Docker) → host.docker.internal:25 → Postfix (Host Ubuntu) → Internet → Gmail/Yahoo mahasiswa
```

---

### B. Docker Compose — Orkestrasi Kontainer

**File: `deployment/docker-compose.yml`**

Seluruh infrastruktur server dijalankan menggunakan Docker Compose yang mengorkestrasi 6 kontainer sekaligus:

| Kontainer | Image | Port | Fungsi |
|---|---|---|---|
| `odoo_web` | `odoo:17.0` | 8069 (internal) | Aplikasi Odoo utama |
| `odoo_db` | `postgres:15` | 5432 (internal) | Database PostgreSQL |
| `nginx_proxy` | `nginx:alpine` | 80, 443 | Reverse proxy & HTTPS redirect |
| `prometheus` | `prom/prometheus` | 9090 (internal) | Pengumpul metrik server |
| `grafana` | `grafana/grafana` | 3000 (internal) | Visualisasi grafik monitoring |
| `node_exporter` | `prom/node-exporter` | 9100 (internal) | Pembaca metrik CPU/RAM/Disk |

Catatan: Hanya Nginx yang mengekspos port ke publik (80 & 443). Semua kontainer lainnya berkomunikasi secara internal melalui jaringan Docker.

**Isi lengkap `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  web:
    image: odoo:17.0
    container_name: odoo_web
    depends_on:
      - db
    ports:
      - "127.0.0.1:8069:8069"
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./config/odoo.conf:/etc/odoo/odoo.conf:ro
      - ../:/mnt/extra-addons/lost_found_dashboard
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - HOST=db
      - USER=${POSTGRES_USER}
      - PASSWORD=${POSTGRES_PASSWORD}
    restart: unless-stopped

  db:
    image: postgres:15
    container_name: odoo_db
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_USER=${POSTGRES_USER}
    volumes:
      - odoo-db-data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: nginx_proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
      - grafana
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

  node_exporter:
    image: prom/node-exporter:latest
    container_name: node_exporter
    command:
      - '--path.rootfs=/host'
    pid: host
    restart: unless-stopped
    volumes:
      - '/:/host:ro,rslave'

volumes:
  odoo-web-data:
  odoo-db-data:
  prometheus_data:
  grafana_data:
```

Penjelasan konfigurasi kunci:
- `127.0.0.1:8069:8069` → Odoo hanya bisa diakses dari localhost (Nginx), **bukan** dari luar server secara langsung. Ini adalah lapisan keamanan tambahan.
- `extra_hosts: host.docker.internal:host-gateway` → Membuat alias DNS `host.docker.internal` yang mengarah ke IP gateway Docker. Inilah yang memungkinkan Odoo mengirim email ke Postfix di Host.
- `./config/odoo.conf:/etc/odoo/odoo.conf:ro` → Me-*mount* file konfigurasi lokal ke dalam kontainer. Flag `:ro` berarti *read-only* (kontainer tidak bisa mengubah file ini).
- `${POSTGRES_USER}` dan `${POSTGRES_PASSWORD}` → Variabel *environment* yang dibaca dari file `.env` di folder `deployment/`.
- `pid: host` pada Node Exporter → Mengizinkan kontainer melihat seluruh proses di mesin Host, diperlukan agar metrik CPU dan RAM akurat.
- `'/:/host:ro,rslave'` → Me-*mount* seluruh *filesystem* Host ke dalam kontainer Node Exporter secara *read-only*.

---

### C. Reverse Proxy Nginx — HTTPS Redirect & Load Balancing

**File: `deployment/nginx/nginx.conf`**

```nginx
events {
    worker_connections 1024;
}

http {
    # WebSocket support
    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    upstream odoo {
        server web:8069;
    }

    upstream grafana {
        server grafana:3000;
    }

    # Main Odoo Server Block
    server {
        listen 80 default_server;
        server_name lostn-found.web.id www.lostn-found.web.id _;

        # Paksa redirect HTTP → HTTPS via Cloudflare header
        if ($http_x_forwarded_proto != "https") {
            return 301 https://$host$request_uri;
        }

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 100M;

        proxy_read_timeout 720s;
        proxy_connect_timeout 720s;
        proxy_send_timeout 720s;

        location / {
            proxy_pass http://odoo;
            proxy_redirect off;
        }

        # WebSocket untuk fitur live chat Odoo
        location /websocket {
            proxy_pass http://odoo;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
        }

        # Cache file statis (CSS, JS, gambar)
        location ~* /web/static/ {
            proxy_pass http://odoo;
            proxy_cache_valid 200 60m;
            expires 864000;
        }
    }

    # Grafana Monitoring Server Block
    server {
        listen 80;
        server_name monitor.lostn-found.web.id;

        if ($http_x_forwarded_proto != "https") {
            return 301 https://$host$request_uri;
        }

        location / {
            proxy_pass http://grafana;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

Penjelasan blok krusial:
- `upstream odoo` → Mendefinisikan bahwa nama `odoo` merujuk ke kontainer `web` di port 8069.
- `if ($http_x_forwarded_proto != "https")` → Cloudflare mengirimkan header `X-Forwarded-Proto` berisi `http` atau `https`. Jika bukan `https`, Nginx mengembalikan kode **301 (Permanent Redirect)** ke versi HTTPS.
- `client_max_body_size 100M` → Mengizinkan upload foto barang temuan hingga 100 MB.
- `proxy_read_timeout 720s` → Timeout 12 menit untuk request berat (misal: generate laporan PDF).
- `location /websocket` → Mendukung koneksi WebSocket untuk fitur notifikasi *real-time* Odoo.

---

### D. CI/CD Pipeline (GitHub Actions)

**File: `.github/workflows/ci-cd.yml`**

Pipeline CI/CD terdiri dari 2 tahap berurutan:

**Tahap 1 — `test` (Continuous Integration):**
1. `actions/checkout@v7` → Mengunduh *source code* dari repositori.
2. `actions/setup-python@v6` → Menyiapkan Python 3.10 di *runner* GitHub.
3. `flake8` → Memindai seluruh file `.py` untuk mendeteksi *syntax error* dan variabel yang tidak terdefinisi.
4. `docker run postgres:15` → Membuat kontainer database PostgreSQL sementara.
5. `docker run odoo:17.0 odoo -i lost_found_dashboard --stop-after-init` → Menginstal modul secara virtual. Jika ada error di Model atau View, proses ini akan gagal dan menolak kode.

**Tahap 2 — `deploy` (Continuous Deployment):**
- Hanya berjalan jika tahap `test` berhasil 100%.
- Menggunakan `appleboy/ssh-action@v1.0.0` untuk *remote login* ke server.
- Perintah yang dieksekusi di server:
  ```bash
  cd /opt/lost_found_dashboard
  git pull origin main
  cd deployment
  docker compose restart web
  ```

**Konfigurasi GitHub Secrets yang Dibutuhkan:**
| Secret Name | Contoh Nilai | Keterangan |
|---|---|---|
| `SERVER_HOST` | `157.66.9.172` | IP publik server Ubuntu |
| `SERVER_USER` | `root` | Username SSH |
| `SERVER_PASSWORD` | `********` | Password SSH |

**Konfigurasi SSH Server:**
- **File:** `/etc/ssh/sshd_config.d/60-cloudimg-settings.conf`
- **Isi:** `PasswordAuthentication yes`
- Tanpa konfigurasi ini, robot GitHub tidak bisa login karena Ubuntu secara default menolak otentikasi password dari koneksi otomatis.

---

### E. Monitoring Server (Grafana & Prometheus)

**URL Akses:** `https://monitor.lostn-found.web.id`

Sistem monitoring terdiri dari 3 komponen yang saling terhubung:

```
Node Exporter (pembaca metrik) → Prometheus (pengumpul data) → Grafana (visualisasi grafik)
```

**File konfigurasi Prometheus: `deployment/prometheus/prometheus.yml`**
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['node_exporter:9100']
```

Penjelasan:
- `scrape_interval: 15s` → Prometheus mengambil data dari Node Exporter setiap 15 detik.
- `targets: ['node_exporter:9100']` → Alamat kontainer Node Exporter yang mengekspos metrik CPU, RAM, disk, dan jaringan.

**Dashboard Grafana:**
- Menggunakan dashboard bawaan "Node Exporter Full" (ID: `1860`).
- Datasource telah di-*hardcode* langsung ke UID Prometheus (`efq30lnjdnnk0e`) agar grafik langsung menyala tanpa konfigurasi manual saat pertama kali diakses.

---

### F. Keamanan Jaringan (Cloudflare)

Terdapat 3 alasan teknis mengapa proyek ini menggunakan Cloudflare:
1. **Enkripsi HTTPS (SSL/TLS):** Nginx internal hanya memancarkan HTTP (port 80). Cloudflare membungkus trafik tersebut menjadi HTTPS (gembok hijau), sehingga *password* dan data mahasiswa terenkripsi aman dari penyadapan.
2. **Reverse Proxy & Penyembunyian IP:** IP publik server Ubuntu disembunyikan di balik jaringan Cloudflare, mencegah serangan DDoS langsung ke server kampus.
3. **HTTP → HTTPS Redirect:** Nginx diprogram untuk membaca header `X-Forwarded-Proto` dari Cloudflare. Jika pengguna mengakses via `http://`, Nginx secara paksa membelokkan ke `https://`.

**Konfigurasi Cloudflare yang diaktifkan:**
- **SSL/TLS Mode:** Full
- **Always Use HTTPS:** ON
- **Proxied (Orange Cloud):** Aktif pada record DNS `lostn-found.web.id` dan `monitor.lostn-found.web.id`

