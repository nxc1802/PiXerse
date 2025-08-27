# Hướng Dẫn Bảo Mật - PiXerse Backend

## 🔐 Cấu Hình Môi Trường An Toàn

### 1. Thiết Lập File Môi Trường

1. **Sao chép file template:**
   ```bash
   cp config_template.env .env
   ```

2. **Chỉnh sửa file .env với các giá trị thật:**
   - **KHÔNG BAO GIỜ** commit file `.env` vào Git
   - **LUÔN LUÔN** sử dụng giá trị placeholder trong `config_template.env`

### 2. Biến Môi Trường Bắt Buộc

#### Database Configuration
```env
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require
```

#### Cloudinary Configuration  
```env
CLOUDINARY_CLOUD_NAME=your-actual-cloud-name
CLOUDINARY_API_KEY=your-actual-api-key
CLOUDINARY_API_SECRET=your-actual-api-secret
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

#### Security Keys
```env
SECRET_KEY=your-secret-key-at-least-32-characters-long
JWT_SECRET_KEY=your-jwt-secret-key-different-from-secret-key
```

#### Docker Database
```env
POSTGRES_PASSWORD=your-secure-postgres-password
```

### 3. Tạo Secret Keys An Toàn

#### Tạo SECRET_KEY:
```python
import secrets
print(secrets.token_urlsafe(32))
```

#### Hoặc sử dụng OpenSSL:
```bash
openssl rand -base64 32
```

### 4. Checklist Trước Khi Deploy

- [ ] Tất cả secrets đã được loại bỏ khỏi code
- [ ] File `.env` không được commit vào Git
- [ ] File `.gitignore` đã include `.env*`
- [ ] Tất cả biến môi trường đã được set trong production
- [ ] Database credentials sử dụng SSL
- [ ] Secret keys đủ mạnh (ít nhất 32 ký tự)

### 5. Môi Trường Development vs Production

#### Development:
- Sử dụng database local hoặc development
- Debug mode = True
- CORS origins bao gồm localhost

#### Production:
- Sử dụng database production với SSL
- Debug mode = False  
- CORS origins chỉ bao gồm domain chính thức
- Sử dụng HTTPS cho tất cả endpoints

### 6. Các File Không Được Commit

```
.env
.env.local
.env.production
.env.development
```

### 7. Lỗi Thường Gặp

1. **ModuleNotFoundError**: Đảm bảo tất cả dependencies trong `requirements.txt`
2. **Database Connection Error**: Kiểm tra DATABASE_URL và network access
3. **Cloudinary Upload Error**: Kiểm tra API keys và quota

### 8. Báo Cáo Lỗi Bảo Mật

Nếu phát hiện lỗi bảo mật, vui lòng báo cáo riêng tư qua email thay vì tạo public issue.

---

⚠️ **LƯU Ý**: File này chứa hướng dẫn bảo mật. Đảm bảo tất cả thành viên team đọc và tuân thủ.
