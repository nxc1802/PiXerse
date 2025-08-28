## Tổng quan dự án PiXerse Backend

PiXerse Backend là ứng dụng FastAPI quản lý nội dung (CMS) cho Landing Page, cung cấp API CRUD cho Projects, Blogs, Members và Assets, tích hợp lưu trữ tệp với Cloudinary và cơ sở dữ liệu PostgreSQL thông qua SQLAlchemy.

- **Repo**: [PiXerse trên GitHub](https://github.com/nxc1802/PiXerse.git)
- **Ngôn ngữ/Framework**: Python 3.11+, FastAPI, SQLAlchemy, Alembic
- **Database**: PostgreSQL
- **Storage**: Cloudinary
- **Cấu hình**: `pydantic-settings` đọc từ file `.env`

### Cấu trúc thư mục chính

- `app/`
  - `api/` Routers và endpoints (`/api/v1`): `projects`, `blogs`, `members`, `assets`
  - `services/` Business logic và tích hợp Cloudinary
  - `models/` SQLAlchemy models và associations
  - `schemas/` Pydantic schemas (request/response)
  - `database/` Kết nối DB và session (`engine`, `SessionLocal`)
  - `config.py` Định nghĩa `Settings` đọc biến môi trường
- `alembic/` Migration scripts
- `docs/` Tài liệu
- `scripts/` Script tiện ích (build, deploy, security check)
- `tests/` Unit/integration tests

### Kiến trúc luồng xử lý

Client → FastAPI App → Routers (`/api/v1`) → Services → Models/DB → (Cloudinary nếu là tệp)

## Thiết lập môi trường

### Yêu cầu

- Python 3.11+
- PostgreSQL 15+
- Tài khoản Cloudinary (Cloud name, API Key, API Secret)

### Biến môi trường (.env)

Sao chép mẫu và điền giá trị thật:

```bash
cp config_template.env .env
```

Các biến chính cần có trong `.env`:

```env
# Database
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
CLOUDINARY_URL=cloudinary://your-api-key:your-api-secret@your-cloud-name

# App
APP_NAME=PiXerse Backend
DEBUG=True
API_V1_STR=/api/v1
MAX_UPLOAD_SIZE=10485760
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080","http://127.0.0.1:3000"]

# Security (tự sinh giá trị mạnh khi lên production)
SECRET_KEY=dev-secret-key-replace-in-production
JWT_SECRET_KEY=dev-jwt-secret-key-replace-in-production
```

Lưu ý: `.gitignore` đã chặn `.env` và các biến thể `.env.*`.

## Chạy ứng dụng (local)

### Cài đặt dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Chạy DB migrations (nếu cần)

```bash
alembic upgrade head
```

### Khởi động ứng dụng

```bash
python3 main.py
# hoặc
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Chạy bằng Docker

Điền `POSTGRES_PASSWORD` vào `.env` (nếu dùng docker-compose):

```env
POSTGRES_PASSWORD=your-postgres-password
```

Khởi chạy:

```bash
docker-compose up -d
```

Các dịch vụ chính:
- `api`: FastAPI app
- `db`: PostgreSQL 15 (map cổng 5432)

## Dịch vụ & Modules chính

- `app/services/cloudinary_service.py`
  - Cấu hình Cloudinary từ biến môi trường
  - Upload/Delete/GetInfo file theo `AssetType`
- `app/database/base.py`
  - Tạo `engine` từ `settings.DATABASE_URL`
  - Cấp `SessionLocal` và dependency `get_db`
- `app/models/*`
  - Models: `Project`, `Blog`, `Member`, `Asset` và các bảng liên kết
- `app/api/endpoints/*`
  - CRUD endpoints cho từng entity

## Bảo mật

- Không còn hardcoded secrets trong code
- Tất cả credentials lấy từ biến môi trường qua `app/config.py`
- `.env` và biến thể đã được ignore bởi Git
- Tài liệu bảo mật: `SECURITY.md`
- Script kiểm tra bảo mật:

```bash
python3 scripts/check_security.py
```

Script sẽ quét chuỗi nhạy cảm (DB URL có user:pass, API keys, secrets, …) và cảnh báo trước khi bạn push.

## Kiểm thử

Chạy tests:

```bash
pytest -q
```

Các test có sẵn:
- `tests/test_main.py`: kiểm tra endpoints cơ bản (`/`, `/health`)
- `tests/test_projects.py`: kiểm tra CRUD cho Projects

## Triển khai (gợi ý)

- Dùng biến môi trường thật trên môi trường deploy (CI/CD, container runtime secrets)
- Đặt `DEBUG=False` trong production
- Hạn chế CORS ở domain hợp lệ (production)
- Đảm bảo `DATABASE_URL` sử dụng SSL khi public network

## Troubleshooting

- Không đọc được cấu hình: kiểm tra `.env` có đủ biến và đúng đường dẫn
- Lỗi DB: xác thực `DATABASE_URL` (host/port/db/ssl), network, và quyền user
- Upload Cloudinary lỗi: kiểm tra `CLOUDINARY_*` và quota tài khoản
- Migration lỗi: đồng bộ models và migrations, chạy `alembic upgrade head`

---

Maintained at: [PiXerse trên GitHub](https://github.com/nxc1802/PiXerse.git)


