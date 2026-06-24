# Rangkuman Pengembangan Proyek "Lost & Found Dashboard"

Dokumen ini berisi rangkuman detail mengenai seluruh konfigurasi, perbaikan, dan fitur yang telah kita bangun bersama dari awal hingga tahap otomatisasi *deployment* (CI/CD). 

## 1. Konfigurasi Server & Database Odoo
**Masalah Awal:** Saat mengakses halaman *login*, pengguna justru diarahkan ke halaman pemilihan *database* (Database Manager).
**Solusi:**
- **Lokasi File:** `deployment/config/odoo.conf`
- **Perubahan:** Menambahkan konfigurasi `dbfilter = ^hilang_temu$` agar Odoo secara otomatis memilih *database* bernama `hilang_temu` dan langsung menampilkan halaman *login* tanpa melalui halaman pemilihan *database*.

## 2. Konfigurasi Mail Server (Reset Password & Notifikasi)
**Masalah Awal:** Pengiriman email dari dalam Odoo (seperti fitur *Lupa Password*) tidak berfungsi, meskipun *server* Ubuntu sudah bisa mengirim email via `sendmail`/Postfix.
**Solusi:**
- **Lokasi File:** `deployment/config/odoo.conf`
- **Perubahan:** Menambahkan konfigurasi SMTP:
  ```ini
  smtp_server = host.docker.internal
  smtp_port = 25
  ```
  Ini mengizinkan Odoo (yang berada di dalam wadah Docker) untuk berkomunikasi langsung dengan sistem Postfix yang ada di komputer *host* server Ubuntu Anda.

## 3. Perbaikan Desain Tampilan (UI) Halaman Reset Password
**Masalah Awal:** Halaman *Reset Password* terpotong di perangkat *mobile* (HP) sehingga tombol konfirmasi di bawah tidak terlihat dan halaman tidak bisa digulir (*scroll*).
**Solusi:**
- **Lokasi File XML:** `views/login_templates.xml`
  - *Perubahan:* Menghapus batasan lebar statis (*fixed max-width*) pada kotak *login* dan menggunakan *class* Bootstrap yang responsif seperti `mx-auto`, `p-3`, dan `p-md-4` agar lebar kotak menyesuaikan ukuran layar HP.
- **Lokasi File CSS:** `static/src/scss/login.scss`
  - *Perubahan:* Menghapus atribut `overflow: hidden;` yang mengunci *scroll*, dan mengubah `height: 100vh;` menjadi `min-height: 100vh;` agar kotak bisa memanjang secara elastis ke bawah mengikuti jumlah kolom formulir yang ada.

## 4. Konfigurasi Dashboard Monitoring (Grafana & Prometheus)
**Masalah Awal:** *Dashboard* monitoring server di Grafana menampilkan "No Data" dan pengguna kesulitan mengatur *Datasource* Prometheus.
**Solusi:**
- **Aksi:** Memodifikasi konfigurasi *dashboard* JSON (*Node Exporter Full*) langsung di dalam *server* menggunakan *script* otomatis.
- **Perubahan:** Mengunci (*hardcode*) sumber data (*Datasource*) setiap grafik agar langsung menunjuk ke ID Prometheus. Hasilnya, begitu Anda membuka URL `monitor.lostn-found.web.id`, semua grafik pemantauan CPU, RAM, dan Jaringan langsung menyala secara otomatis.

## 5. Konfigurasi Keamanan SSH Server
**Masalah Awal:** GitHub Actions gagal masuk ke *server* karena *server* secara *default* menolak otentikasi menggunakan *password* otomatis.
**Solusi:**
- **Lokasi File (di dalam Server):** `/etc/ssh/sshd_config.d/60-cloudimg-settings.conf`
- **Perubahan:** Mengubah nilai `PasswordAuthentication no` menjadi `PasswordAuthentication yes` dan me-restart layanan SSH di server agar robot GitHub Actions bisa masuk.

## 6. Arsitektur Otomatisasi CI/CD (GitHub Actions)
**Masalah Awal:** Perlu cara untuk menarik kode terbaru secara otomatis dari GitHub ke *server* Odoo dengan aman.
**Solusi:**
- **Lokasi File:** `.github/workflows/ci-cd.yml`
- **Perubahan:** Membangun *pipeline* CI/CD lengkap yang terdiri dari 2 tahapan (*Jobs*):
  1. **Job `test` (Continuous Integration):**
     - **Linting:** Memeriksa seluruh *syntax* Python dengan `flake8`.
     - **Uji Kompilasi:** Membuat simulasi wadah Odoo dan PostgreSQL di dalam GitHub Actions untuk melakukan *dry-run* instalasi modul. Jika *database crash*, kode akan ditolak.
  2. **Job `deploy` (Continuous Deployment):**
     - Berjalan **hanya jika** Job `test` berhasil.
     - *Script* akan melakukan `git pull origin main` secara otomatis ke dalam direktori `/opt/lost_found_dashboard` di *server*.
     - Menjalankan `docker compose restart web` di *server* untuk mengaplikasikan versi *website* yang paling baru.

---
**Status Terkini:**
Semua *source code* di lingkungan lokal Anda (Windows), di repositori GitHub, dan di *server* produksi Ubuntu sudah **100% tersinkronisasi** dengan mulus melalui sistem otomatisasi di atas.
