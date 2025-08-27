Giai đoạn 0 – Chuẩn bị
	•	Tạo repo, setup FastAPI project
	•	Thêm cấu hình Poetry/pipenv + .env
	•	Kết nối PostgreSQL (SQLAlchemy + Alembic)
	•	Cấu hình Cloudinary SDK

⸻

Giai đoạn 1 – Database Schema (PostgreSQL)
	•	Tạo bảng project
	•	Tạo bảng member
	•	Tạo bảng blog
	•	Tạo bảng asset
	•	Tạo bảng liên kết project_asset, blog_asset, member_asset
	•	Viết migration Alembic
	•	Seed dữ liệu mẫu

⸻

Giai đoạn 2 – Cloudinary
	•	Thiết lập folder structure & upload preset
	•	Viết hàm upload file → lưu metadata vào asset
	•	Viết hàm delete file + xoá record DB

⸻

Giai đoạn 3 – FastAPI Server
	•	Khởi tạo app, route /health
	•	Setup SQLAlchemy SessionLocal
	•	Setup pydantic models (request/response)

⸻

Giai đoạn 4 – API Endpoints (CRUD)
	•	Project: POST /projects, GET /projects, GET /projects/{id}, PATCH /projects/{id}, DELETE /projects/{id}
	•	Member: POST /members, GET /members, GET /members/{id}, PATCH /members/{id}, DELETE /members/{id}
	•	Blog: POST /blogs, GET /blogs, GET /blogs/{id}, PATCH /blogs/{id}, DELETE /blogs/{id}
	•	Asset: POST /assets, GET /assets, GET /assets/{id}, DELETE /assets/{id}
	•	Endpoint attach/detach asset vào project/blog/member

⸻

Giai đoạn 5 – Unit Test
	•	Thiết lập pytest + test DB (SQLite in-memory hoặc Postgre test)
	•	Unit test cho models + services (CRUD)
	•	Integration test cho endpoints (FastAPI TestClient)

⸻

Giai đoạn 6 – Docs & Tools
	•	Auto-generate OpenAPI/Swagger tại /docs
	•	Dockerfile + docker-compose (app + postgres)
	•	README hướng dẫn run/migrate/test