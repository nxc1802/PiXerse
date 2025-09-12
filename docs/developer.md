## Developer Guide — Thiết kế cơ sở dữ liệu (Backend)

Tài liệu này mô tả thiết kế DB của PiXerse Backend, bao gồm schema, quan hệ, conventions, migration và thực hành tốt khi làm việc với SQLAlchemy + Alembic.

### 1) Tổng quan kiến trúc dữ liệu

- PostgreSQL là CSDL chính, kết nối qua `SQLAlchemy` (`app/database/base.py`).
- Models định nghĩa trong `app/models/*` và được map qua `declarative_base()`.
- Migration quản lý bằng Alembic trong `alembic/`.
- Lưu trữ tệp dùng Cloudinary, DB chỉ lưu metadata/`public_id`.

Sơ đồ logic (rút gọn):

- `projects (1) — (N) blogs`
- `projects (1) — (N) members`
- Nhiều-nhiều qua bảng liên kết:
  - `project_assets (project_id — asset_id)`
  - `blog_assets (blog_id — asset_id)`
  - `member_assets (member_id — asset_id)`

### 2) Các bảng chính

#### 2.1) projects
- `project_id` (PK, int, autoincrement)
- Các cột mô tả (tham khảo trong `app/models/project.py`)
- Ràng buộc: được tham chiếu bởi `blogs.project_id`, `members.project_id`, `project_assets.project_id`

#### 2.2) blogs
- `blog_id` (PK)
- `project_id` (FK → projects.project_id, ondelete='CASCADE')
- Nội dung/tiêu đề, thời gian tạo/cập nhật (xem `app/models/blog.py`)

#### 2.3) members
- `member_id` (PK)
- `project_id` (FK → projects.project_id, ondelete='CASCADE')
- Thông tin thành viên: tên, vai trò, mô tả (xem `app/models/member.py`)

#### 2.4) assets
- `asset_id` (PK)
- Metadata tệp: `cloudinary_public_id`, URL, kích thước, `asset_type` (enum: IMAGE, VIDEO, DOCUMENT, OTHER)
- Dùng để tham chiếu từ nhiều bảng qua các bảng liên kết (xem `app/models/asset.py`)

#### 2.5) Bảng liên kết nhiều-nhiều
- `project_assets(project_id, asset_id)`
- `blog_assets(blog_id, asset_id)`
- `member_assets(member_id, asset_id)`

Mỗi bảng đặt PK là tổ hợp 2 cột tương ứng, có FK ondelete='CASCADE'. Xem `app/models/associations.py`.

### 3) Ràng buộc và quy tắc

- Mọi FK dùng `ondelete='CASCADE'` để tự động dọn dữ liệu liên quan.
- PK dạng số nguyên tự tăng, có `index=True` ở cột định danh.
- Bảng liên kết dùng PK tổng hợp để tránh trùng lặp.
- Enum `AssetType` quy định thư mục Cloudinary và phân loại.

### 4) Indexing & hiệu năng

- Đã index các PK (`project_id`, `blog_id`, `member_id`, `asset_id`).
- Khuyến nghị thêm index nếu truy vấn nhiều theo cột ngoài PK (ví dụ: `created_at`, `project_id` ở blogs/members):

```sql
CREATE INDEX IF NOT EXISTS idx_blogs_project_id ON blogs(project_id);
CREATE INDEX IF NOT EXISTS idx_members_project_id ON members(project_id);
```

Triển khai index mới qua Alembic migration (mục 6).

### 5) Kết nối và session

- `app/database/base.py`:
  - `engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)`
  - `SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)`
  - Dependency `get_db()` cho FastAPI.

Sử dụng trong endpoint/service:

```python
from app.database.base import get_db

def handler(db):
    # db là Session; dùng db.query(...), db.add(...), db.commit()
    ...
```

Transaction khuyến nghị:
- Commit theo lô logic nhỏ; rollback khi lỗi.
- Không giữ session mở quá lâu trong tác vụ nặng I/O.

### 6) Migration với Alembic

- Cấu hình tại `alembic.ini` và `alembic/env.py`.
- Migration hiện có: `alembic/versions/c5ca601b6846_initial_migration_create_tables.py` tạo toàn bộ bảng.

Lệnh thường dùng:

```bash
# Tạo file migration mới (sau khi sửa models)
alembic revision -m "add new index"

# Áp dụng toàn bộ migration
alembic upgrade head

# Quay lui 1 bước
alembic downgrade -1
```

Thêm index bằng migration ví dụ:

```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_index('idx_blogs_project_id', 'blogs', ['project_id'], unique=False)

def downgrade():
    op.drop_index('idx_blogs_project_id', table_name='blogs')
```

### 7) Seed dữ liệu

- Script seed: `development/seed_data.py` (tham khảo để tạo dữ liệu mẫu).
- Nên dùng biến môi trường/dev DB riêng khi seed.

### 8) Biến môi trường liên quan DB

- `DATABASE_URL` (bắt buộc, dạng `postgresql://user:pass@host:port/db?sslmode=require`)
- Với Docker Compose: `POSTGRES_PASSWORD` để khởi tạo container Postgres.

Ví dụ `.env`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/pixerse_dev
POSTGRES_PASSWORD=dev-postgres-password
```

### 9) Quy ước đặt tên

- Bảng số nhiều: `projects`, `blogs`, `members`, `assets`;
- PK: `<entity>_id`;
- FK: `<ref>_id` với `ondelete='CASCADE'`;
- Bảng liên kết: `<left>_<right>` theo alphabet (vd: `blog_assets`).

### 10) Mẫu truy vấn hữu ích (SQLAlchemy ORM)

```python
# Lấy tất cả blogs thuộc 1 project
blogs = db.query(Blog).filter(Blog.project_id == project_id).all()

# Gán asset cho blog qua bảng liên kết (tuỳ model setup relationship)
blog.assets.append(asset)
db.commit()

# Xoá project sẽ cascade xoá blogs/members/liên kết
db.delete(project)
db.commit()
```

### 11) Ràng buộc dữ liệu & validation

- Validation cấp ứng dụng: Pydantic Schemas trong `app/schemas/*`.
- Validation cấu hình: `app/config.py` xác thực `DATABASE_URL`, Cloudinary keys từ môi trường.

### 12) Backup & khôi phục (gợi ý)

- Dùng `pg_dump`/`pg_restore` cho PostgreSQL.
- Thiết lập lịch backup định kỳ (production).

---

Tài liệu liên quan:
- `docs/PROJECT_SUMMARY.md` — tổng quan end-to-end
- `SECURITY.md` — hướng dẫn bảo mật và secrets
- `alembic/` — migration scripts


