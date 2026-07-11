"""
Database Migration Script for AI/ML Features
Run this to add new tables for the advanced features
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
import json
from datetime import date, datetime


# Database configuration
DATABASE_URL = "sqlite:///./hms.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def run_migration():
    """Run the migration to add AI/ML tables"""
    print("=" * 60)
    print("🏥 Hospital Management System - AI/ML Migration")
    print("=" * 60)
    
    # Import Base and models
    from app.database import Base
    from app.models import models
    
    try:
        # Import AI models
        from app.models.ai_models import (
            DiseasePrediction, DoctorRating, DoctorRecommendation,
            ResourcePrediction, ResourceUsage, ChatSession, ChatMessage,
            SmartAppointmentSlot, HealthRecord, Permission, RolePermission,
            AuditLog, TelemedicineSession, EPrescription, AnalyticsSnapshot
        )
        print("✅ AI Model imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Check existing tables
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print(f"\n📋 Existing tables: {existing_tables}")
    
    # Define new tables
    new_tables = [
        "disease_predictions",
        "doctor_ratings",
        "doctor_recommendations",
        "resource_predictions",
        "resource_usage",
        "chat_sessions",
        "chat_messages",
        "smart_appointment_slots",
        "health_records",
        "permissions",
        "role_permissions",
        "audit_logs",
        "telemedicine_sessions",
        "e_prescriptions",
        "analytics_snapshots"
    ]
    
    # Create tables
    print("\n🔄 Creating new tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    # Verify new tables
    inspector = inspect(engine)
    updated_tables = inspector.get_table_names()
    
    created = []
    for table in new_tables:
        if table in updated_tables:
            created.append(table)
    
    print(f"\n✅ Created {len(created)} new tables:")
    for table in created:
        print(f"   - {table}")
    
    # Initialize default data
    print("\n🔄 Initializing default data...")
    initialize_default_data()
    
    print("\n" + "=" * 60)
    print("✅ Migration completed successfully!")
    print("=" * 60)
    return True


def initialize_default_data():
    """Initialize default permissions and other required data"""
    db = SessionLocal()
    
    try:
        from app.models.ai_models import Permission, RolePermission
        
        # Check if permissions already exist
        existing_perms = db.query(Permission).count()
        if existing_perms > 0:
            print("   Permissions already initialized")
            return
        
        # Define permissions
        permissions = [
            # Patient permissions
            ("view_patients", "View patient list and details", "patients"),
            ("create_patients", "Create new patients", "patients"),
            ("edit_patients", "Edit patient information", "patients"),
            ("delete_patients", "Delete patients", "patients"),
            ("view_patient_records", "View patient medical records", "patients"),
            
            # Doctor permissions
            ("view_doctors", "View doctor list", "doctors"),
            ("create_doctors", "Add new doctors", "doctors"),
            ("edit_doctors", "Edit doctor information", "doctors"),
            
            # Appointment permissions
            ("view_appointments", "View appointments", "appointments"),
            ("create_appointments", "Create appointments", "appointments"),
            ("edit_appointments", "Edit appointments", "appointments"),
            ("cancel_appointments", "Cancel appointments", "appointments"),
            
            # Billing permissions
            ("view_bills", "View bills and invoices", "billing"),
            ("create_bills", "Create new bills", "billing"),
            ("edit_bills", "Edit bills", "billing"),
            ("process_payments", "Process payments", "billing"),
            
            # Pharmacy permissions
            ("view_medicines", "View medicine inventory", "pharmacy"),
            ("create_medicines", "Add medicines", "pharmacy"),
            ("edit_medicines", "Edit medicine details", "pharmacy"),
            ("dispense_medicines", "Dispense medicines", "pharmacy"),
            
            # Lab permissions
            ("view_lab_tests", "View lab tests", "laboratory"),
            ("create_lab_tests", "Request lab tests", "laboratory"),
            ("edit_lab_results", "Edit lab results", "laboratory"),
            
            # EHR permissions
            ("view_ehr", "View electronic health records", "ehr"),
            ("create_ehr", "Create health records", "ehr"),
            ("upload_documents", "Upload documents", "ehr"),
            
            # Admin permissions
            ("manage_users", "Manage user accounts", "admin"),
            ("manage_roles", "Manage roles and permissions", "admin"),
            ("view_audit_logs", "View audit logs", "admin"),
            ("system_settings", "Modify system settings", "admin"),
            
            # AI/ML permissions
            ("use_ai_predictions", "Use AI predictions", "ai"),
            ("train_models", "Train ML models", "ai"),
            ("view_analytics", "View analytics dashboard", "analytics"),
            
            # Telemedicine permissions
            ("create_video_sessions", "Create video sessions", "telemedicine"),
            ("join_video_sessions", "Join video sessions", "telemedicine"),
            ("create_e_prescriptions", "Create e-prescriptions", "telemedicine"),
        ]
        
        # Add permissions
        for name, description, module in permissions:
            perm = Permission(name=name, description=description, module=module)
            db.add(perm)
        
        db.commit()
        print(f"   ✅ Added {len(permissions)} permissions")
        
        # Add role-permission mappings
        role_perms = {
            "admin": [p[0] for p in permissions],  # All permissions
            "doctor": [
                "view_patients", "edit_patients", "view_patient_records",
                "view_doctors",
                "view_appointments", "create_appointments", "edit_appointments", "cancel_appointments",
                "view_bills", "create_bills",
                "view_medicines",
                "view_lab_tests", "create_lab_tests", "edit_lab_results",
                "view_ehr", "create_ehr", "upload_documents",
                "use_ai_predictions", "view_analytics",
                "create_video_sessions", "join_video_sessions", "create_e_prescriptions"
            ],
            "nurse": [
                "view_patients", "edit_patients", "view_patient_records",
                "view_doctors", "view_appointments", "view_lab_tests",
                "view_ehr", "upload_documents", "use_ai_predictions"
            ],
            "lab_staff": [
                "view_patients", "view_patient_records",
                "view_lab_tests", "create_lab_tests", "edit_lab_results",
                "view_ehr"
            ],
            "pharmacist": [
                "view_patients",
                "view_medicines", "create_medicines", "edit_medicines", "dispense_medicines",
                "view_ehr"
            ],
            "receptionist": [
                "view_patients", "create_patients", "edit_patients",
                "view_doctors",
                "view_appointments", "create_appointments", "edit_appointments", "cancel_appointments",
                "view_bills", "create_bills"
            ],
            "patient": [
                "view_patient_records", "view_appointments", "view_bills", "view_ehr",
                "join_video_sessions"
            ]
        }
        
        # Get permission IDs
        perm_ids = {p.name: p.id for p in db.query(Permission).all()}
        
        # Add role permissions
        count = 0
        for role, perms in role_perms.items():
            for perm_name in perms:
                if perm_name in perm_ids:
                    rp = RolePermission(role=role, permission_id=perm_ids[perm_name])
                    db.add(rp)
                    count += 1
        
        db.commit()
        print(f"   ✅ Added {count} role-permission mappings")
        
    except Exception as e:
        print(f"   ❌ Error initializing data: {e}")
        db.rollback()
    finally:
        db.close()


def train_initial_models():
    """Train initial ML models"""
    print("\n🔄 Training ML models...")
    
    try:
        from app.ml.multi_disease_predictor import disease_predictor
        disease_predictor.train_model()
        print("   ✅ Multi-disease predictor trained")
    except Exception as e:
        print(f"   ⚠️ Could not train disease predictor: {e}")
    
    try:
        from app.ml.resource_predictor import resource_predictor
        # Generate initial synthetic data
        resource_predictor.predict_all_resources(7)
        resource_predictor.save_model()
        print("   ✅ Resource predictor initialized")
    except Exception as e:
        print(f"   ⚠️ Could not initialize resource predictor: {e}")


if __name__ == "__main__":
    success = run_migration()
    
    if success and "--train" in sys.argv:
        train_initial_models()
    
    if success:
        print("\n🎉 Your Hospital Management System is now AI-ready!")
        print("   Start the server with: uvicorn app.main:app --reload")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
