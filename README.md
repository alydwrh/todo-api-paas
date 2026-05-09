# To-Do List API Berbasis Flask dan Railway

Aplikasi ini merupakan aplikasi web sederhana berbasis API untuk mencatat daftar tugas. Aplikasi dikembangkan menggunakan Flask dan dideploy ke Railway sebagai platform PaaS.

## Fitur Aplikasi

- Menampilkan informasi aplikasi
- Mengecek status aplikasi melalui health check
- Menampilkan daftar tugas
- Menambahkan tugas baru
- Memperbarui tugas
- Menghapus tugas

## Endpoint

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | / | Menampilkan informasi aplikasi |
| GET | /health | Mengecek status aplikasi |
| GET | /tasks | Menampilkan semua task |
| POST | /tasks | Menambahkan task baru |
| PUT | /tasks/<id> | Memperbarui task |
| DELETE | /tasks/<id> | Menghapus task |

## Teknologi yang Digunakan

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Railway
- GitHub

## Environment Variable

- DATABASE_URL
- SECRET_KEY

## Cara Menjalankan Aplikasi Secara Lokal

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py