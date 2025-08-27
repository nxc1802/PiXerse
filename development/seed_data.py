"""
Seed sample data for development and testing
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.base import SessionLocal, engine
from app.models.base import Base
from app.models.project import Project
from app.models.member import Member
from app.models.blog import Blog
from app.models.asset import Asset, AssetType


def create_sample_data():
    """Create sample data for development"""
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        print("🌱 Creating sample data...")
        
        # Create sample projects
        projects = [
            Project(
                project_name="E-commerce Platform",
                description="A modern e-commerce platform built with React and Node.js"
            ),
            Project(
                project_name="Mobile Banking App",
                description="Secure mobile banking application with biometric authentication"
            ),
            Project(
                project_name="AI Chat Assistant",
                description="AI-powered customer service chatbot using natural language processing"
            )
        ]
        
        for project in projects:
            db.add(project)
        
        db.commit()
        
        # Refresh to get IDs
        for project in projects:
            db.refresh(project)
        
        print(f"✅ Created {len(projects)} projects")
        
        # Create sample members
        members = [
            # E-commerce Platform team
            Member(
                project_id=projects[0].project_id,
                team_type="Frontend",
                role="Lead Frontend Developer",
                experience=5,
                summary="Expert in React, TypeScript, and modern frontend architecture"
            ),
            Member(
                project_id=projects[0].project_id,
                team_type="Backend",
                role="Backend Developer",
                experience=3,
                summary="Specialized in Node.js, Express, and database design"
            ),
            Member(
                project_id=projects[0].project_id,
                team_type="Design",
                role="UI/UX Designer",
                experience=4,
                summary="Creative designer focused on user experience and interface design"
            ),
            
            # Mobile Banking App team
            Member(
                project_id=projects[1].project_id,
                team_type="Mobile",
                role="Mobile Developer",
                experience=6,
                summary="Expert in React Native and iOS/Android development"
            ),
            Member(
                project_id=projects[1].project_id,
                team_type="Security",
                role="Security Engineer",
                experience=7,
                summary="Specialist in cybersecurity and secure application development"
            ),
            
            # AI Chat Assistant team
            Member(
                project_id=projects[2].project_id,
                team_type="AI/ML",
                role="ML Engineer",
                experience=4,
                summary="Machine learning engineer with expertise in NLP and deep learning"
            ),
            Member(
                project_id=projects[2].project_id,
                team_type="Backend",
                role="Python Developer",
                experience=3,
                summary="Backend developer specializing in Python, FastAPI, and AI integration"
            )
        ]
        
        for member in members:
            db.add(member)
        
        db.commit()
        print(f"✅ Created {len(members)} team members")
        
        # Create sample blogs
        blogs = [
            # E-commerce blogs
            Blog(
                project_id=projects[0].project_id,
                title="Building Scalable E-commerce Architecture",
                detail="In this post, we explore the architecture decisions that make our e-commerce platform scalable and maintainable. We discuss microservices, database design, and frontend optimization techniques."
            ),
            Blog(
                project_id=projects[0].project_id,
                title="Implementing Real-time Notifications",
                detail="Learn how we implemented real-time notifications for order updates, inventory changes, and customer communications using WebSockets and Redis."
            ),
            
            # Mobile Banking blogs
            Blog(
                project_id=projects[1].project_id,
                title="Security First: Building a Secure Banking App",
                detail="Security is paramount in financial applications. This post covers our approach to implementing end-to-end encryption, biometric authentication, and secure data storage."
            ),
            Blog(
                project_id=projects[1].project_id,
                title="React Native Performance Optimization",
                detail="Optimizing mobile app performance is crucial for user experience. We share our techniques for reducing bundle size, improving loading times, and smooth animations."
            ),
            
            # AI Chat Assistant blogs
            Blog(
                project_id=projects[2].project_id,
                title="Natural Language Processing in Customer Service",
                detail="How we built an AI chatbot that understands customer intent and provides accurate responses. From data preprocessing to model deployment in production."
            ),
            Blog(
                project_id=projects[2].project_id,
                title="Scaling AI Models with FastAPI",
                detail="Our journey of deploying machine learning models at scale using FastAPI, Docker, and cloud infrastructure. Performance optimization and monitoring included."
            )
        ]
        
        for blog in blogs:
            db.add(blog)
        
        db.commit()
        print(f"✅ Created {len(blogs)} blog posts")
        
        # Create sample assets
        assets = [
            Asset(
                filename="ecommerce_hero",
                original_filename="ecommerce-hero-image.jpg",
                cloudinary_public_id="pixerse/images/ecommerce_hero_123",
                cloudinary_url="https://res.cloudinary.com/demo/image/upload/ecommerce_hero_123.jpg",
                cloudinary_secure_url="https://res.cloudinary.com/demo/image/upload/ecommerce_hero_123.jpg",
                asset_type=AssetType.IMAGE,
                file_size=1024768,
                mime_type="image/jpeg",
                width=1920,
                height=1080
            ),
            Asset(
                filename="mobile_banking_logo",
                original_filename="banking-app-logo.png",
                cloudinary_public_id="pixerse/images/mobile_banking_logo_456",
                cloudinary_url="https://res.cloudinary.com/demo/image/upload/mobile_banking_logo_456.png",
                cloudinary_secure_url="https://res.cloudinary.com/demo/image/upload/mobile_banking_logo_456.png",
                asset_type=AssetType.IMAGE,
                file_size=256000,
                mime_type="image/png",
                width=512,
                height=512
            ),
            Asset(
                filename="ai_demo_video",
                original_filename="ai-chatbot-demo.mp4",
                cloudinary_public_id="pixerse/videos/ai_demo_video_789",
                cloudinary_url="https://res.cloudinary.com/demo/video/upload/ai_demo_video_789.mp4",
                cloudinary_secure_url="https://res.cloudinary.com/demo/video/upload/ai_demo_video_789.mp4",
                asset_type=AssetType.VIDEO,
                file_size=15728640,  # 15MB
                mime_type="video/mp4",
                width=1280,
                height=720
            ),
            Asset(
                filename="project_documentation",
                original_filename="project-requirements.pdf",
                cloudinary_public_id="pixerse/documents/project_doc_101",
                cloudinary_url="https://res.cloudinary.com/demo/raw/upload/project_doc_101.pdf",
                cloudinary_secure_url="https://res.cloudinary.com/demo/raw/upload/project_doc_101.pdf",
                asset_type=AssetType.DOCUMENT,
                file_size=2048000,
                mime_type="application/pdf"
            )
        ]
        
        for asset in assets:
            db.add(asset)
        
        db.commit()
        print(f"✅ Created {len(assets)} assets")
        
        # Associate assets with projects
        projects[0].assets.extend([assets[0], assets[3]])  # E-commerce gets hero image and docs
        projects[1].assets.append(assets[1])  # Banking gets logo
        projects[2].assets.append(assets[2])  # AI gets demo video
        
        # Associate assets with some blogs
        blogs[0].assets.append(assets[0])  # E-commerce blog gets hero image
        blogs[4].assets.append(assets[2])  # AI blog gets demo video
        
        # Associate assets with some members (profile pictures, portfolios, etc.)
        members[0].assets.append(assets[0])  # Frontend lead gets hero image (portfolio)
        members[5].assets.append(assets[2])  # ML engineer gets AI video
        
        db.commit()
        print("✅ Created asset associations")
        
        print("\n🎉 Sample data created successfully!")
        print("\nCreated data summary:")
        print(f"  📁 Projects: {len(projects)}")
        print(f"  👥 Members: {len(members)}")
        print(f"  📝 Blogs: {len(blogs)}")
        print(f"  🖼️  Assets: {len(assets)}")
        print("\n🌐 You can now access the API at: http://localhost:8000")
        print("📚 API docs available at: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def clear_data():
    """Clear all data from database"""
    db: Session = SessionLocal()
    
    try:
        print("🗑️  Clearing all data...")
        
        # Delete in reverse dependency order
        db.query(Member).delete()
        db.query(Blog).delete()
        db.query(Asset).delete()
        db.query(Project).delete()
        
        db.commit()
        print("✅ All data cleared")
        
    except Exception as e:
        print(f"❌ Error clearing data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage sample data for PiXerse Backend")
    parser.add_argument(
        "action", 
        choices=["create", "clear", "recreate"],
        help="Action to perform: create, clear, or recreate data"
    )
    
    args = parser.parse_args()
    
    if args.action == "create":
        create_sample_data()
    elif args.action == "clear":
        clear_data()
    elif args.action == "recreate":
        clear_data()
        create_sample_data()
    else:
        print("❌ Invalid action. Use: create, clear, or recreate")
