#!/usr/bin/env python3
"""
Script kiểm tra bảo mật để đảm bảo không có secrets bị hardcode trong code
Chạy script này trước khi commit code
"""

import os
import re
import sys
from pathlib import Path

# Patterns to detect potential secrets
SECRET_PATTERNS = [
    # Database URLs with credentials
    r'postgresql://[^:]+:[^@]+@[^/]+',
    r'mysql://[^:]+:[^@]+@[^/]+',
    
    # API Keys and Secrets
    r'["\'][A-Za-z0-9]{20,}["\']',  # Long alphanumeric strings
    r'api_key\s*=\s*["\'][^"\']+["\']',
    r'api_secret\s*=\s*["\'][^"\']+["\']',
    r'secret_key\s*=\s*["\'][^"\']+["\']',
    r'password\s*=\s*["\'][^"\']+["\']',
    
    # Cloudinary URLs
    r'cloudinary://[^:]+:[^@]+@[^/]+',
    
    # Common secret patterns
    r'["\'][A-Z0-9]{32,}["\']',  # All caps secrets
    r'["\'][a-z0-9]{40,}["\']',  # Long lowercase secrets
]

# Files to exclude from checking
EXCLUDE_PATTERNS = [
    r'\.git/',
    r'__pycache__/',
    r'\.pyc$',
    r'\.env\.example$',
    r'config_template\.env$',
    r'SECURITY\.md$',
    r'scripts/check_security\.py$',
    r'\.md$',  # Markdown files often contain examples
]

# Whitelist patterns (known safe patterns)
WHITELIST_PATTERNS = [
    r'your-.*',  # Template placeholders
    r'example.*',  # Example values
    r'localhost',  # Local development
    r'127\.0\.0\.1',  # Local IP
    r'test.*',  # Test values
    r'demo.*',  # Demo values
    r'placeholder.*',  # Placeholder values
]

def should_exclude_file(file_path):
    """Check if file should be excluded from security scan"""
    file_str = str(file_path)
    return any(re.search(pattern, file_str) for pattern in EXCLUDE_PATTERNS)

def is_whitelisted(content):
    """Check if content matches whitelist patterns"""
    return any(re.search(pattern, content, re.IGNORECASE) for pattern in WHITELIST_PATTERNS)

def scan_file(file_path):
    """Scan a single file for potential secrets"""
    violations = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern in SECRET_PATTERNS:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    matched_text = match.group()
                    if not is_whitelisted(matched_text):
                        violations.append({
                            'file': file_path,
                            'line': i,
                            'pattern': pattern,
                            'match': matched_text[:50] + '...' if len(matched_text) > 50 else matched_text,
                            'full_line': line.strip()
                        })
    except Exception as e:
        print(f"Lỗi khi đọc file {file_path}: {e}")
    
    return violations

def scan_directory(directory):
    """Scan all files in directory for secrets"""
    all_violations = []
    
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            file_path = Path(root) / file
            
            if should_exclude_file(file_path):
                continue
                
            violations = scan_file(file_path)
            all_violations.extend(violations)
    
    return all_violations

def main():
    """Main function"""
    print("🔍 Đang kiểm tra bảo mật dự án...")
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    
    # Scan for violations
    violations = scan_directory(project_root)
    
    if violations:
        print(f"\n❌ Tìm thấy {len(violations)} vi phạm bảo mật tiềm ẩn:")
        print("=" * 80)
        
        for violation in violations:
            print(f"\nFile: {violation['file']}")
            print(f"Dòng {violation['line']}: {violation['full_line']}")
            print(f"Phát hiện: {violation['match']}")
            print("-" * 40)
        
        print(f"\n⚠️  Hãy kiểm tra và loại bỏ các secrets bị hardcode!")
        print("💡 Hướng dẫn:")
        print("   1. Di chuyển secrets vào file .env")
        print("   2. Sử dụng biến môi trường trong code")
        print("   3. Đảm bảo .env được ignore trong .gitignore")
        
        sys.exit(1)
    else:
        print("✅ Không tìm thấy vi phạm bảo mật!")
        print("🚀 Dự án an toàn để push lên GitHub!")
        sys.exit(0)

if __name__ == "__main__":
    main()
