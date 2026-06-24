# Panduan Lengkap Konfigurasi Server: Mail, CI/CD, dan Monitoring

Dokumen ini membedah secara teknis letak *file* dan isi konfigurasi dari tiga infrastruktur utama yang ada di sistem Odoo Anda.

---

## 1. Mail Server (Email & Reset Password)
Mail Server digunakan agar Odoo bisa mengirimkan email notifikasi dan tautan *reset password* ke pengguna.

- **Letak File Konfigurasi:** `deployment/config/odoo.conf` (di komputer lokal dan server)
- **Cara Kerja:** Karena Odoo berjalan di dalam kontainer Docker, sedangkan aplikasi pengirim email (Postfix) berjalan langsung di sistem utama Ubuntu (Host), kita harus menghubungkan Odoo ke Host menggunakan *gateway* khusus Docker yaitu `host.docker.internal`.
- **Isi Konfigurasi yang Ditambahkan:**
  ```ini
  [options]
  # ... konfigurasi lainnya ...
  
  # Konfigurasi SMTP (Mail Server)
  smtp_server = host.docker.internal
  smtp_port = 25
  ```

---

## 2. CI/CD Pipeline (GitHub Actions)
CI/CD bertugas untuk mengotomatisasi pengujian kode dan rilis pembaruan ke *server* setiap kali Anda menekan perintah `git push`.

- **Letak File CI/CD:** `.github/workflows/ci-cd.yml` (berada di dalam repositori proyek Anda)
- **Letak Konfigurasi Izin Server:** `/etc/ssh/sshd_config.d/60-cloudimg-settings.conf` (berada di dalam OS Ubuntu *server* Anda)
- **Cara Kerja & Konfigurasi Utama:**
  
  **A. Di dalam Server (Mengizinkan Robot Masuk):**
  Secara *default*, Ubuntu menolak *login* robot menggunakan *password*. Kita harus mengubah izinnya dengan mengubah baris berikut:
  ```text
  PasswordAuthentication yes
  ```
  *(Setelah diubah, layanan SSH di-restart menggunakan `systemctl restart ssh`)*

  **B. Di dalam file `ci-cd.yml` (Alur Otomatisasi):**
  File ini berisi instruksi eksekusi. Konfigurasi utamanya ada di tahap eksekusi server:
  ```yaml
  - name: Deploy via SSH
    uses: appleboy/ssh-action@v1.0.0
    with:
      host: ${{ secrets.SERVER_HOST }}
      username: ${{ secrets.SERVER_USER }}
      password: ${{ secrets.SERVER_PASSWORD }}
      port: 22
      script: |
        cd /opt/lost_found_dashboard
        git pull origin main
        cd deployment
        docker compose restart web
  ```
  Nilai dari `${{ secrets.SERVER_PASSWORD }}` dan lainnya diambil dari pengaturan rahasia di halaman repositori GitHub Anda.

---

## 3. Monitoring System (Grafana & Prometheus)
Sistem pemantauan ini menampilkan grafik penggunaan CPU, RAM, dan Jaringan secara *real-time*.

- **Letak Infrastruktur:** Berjalan menggunakan Docker di dalam *server* Anda.
- **URL Akses:** `http://monitor.lostn-found.web.id`
- **Cara Kerja & Konfigurasi:**
  Grafana (penampil grafik) membutuhkan sumber data yang disebut Prometheus (pengumpul data). Karena sistem Anda awalnya belum tersambung, kami melakukan injeksi konfigurasi langsung ke *database* Grafana.
  
  **Konfigurasi yang Diterapkan:**
  1. Grafana dan Prometheus sudah satu jaringan (Network) di dalam Docker, sehingga URL sumber datanya adalah: `http://prometheus:9090`.
  2. Sebuah *dashboard* khusus bernama "Node Exporter Full" (dengan ID `1860`) diimpor ke dalam Grafana.
  3. Konfigurasi JSON pada *dashboard* tersebut dirombak secara paksa agar nilai `datasource`-nya menunjuk langsung ke UID (*Unique ID*) milik Prometheus, menggantikan sistem parameter bawaan yang sering menyebabkan grafik *error* atau "No Data".

  Inti perubahannya pada kerangka JSON Grafana adalah mengubah variabel dinamis:
  ```json
  "datasource": "${DS_PROMETHEUS}"
  ```
  Menjadi *hardcoded* UID pasti:
  ```json
  "datasource": {"type": "prometheus", "uid": "efq30lnjdnnk0e"}
  ```
