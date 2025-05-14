from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Dummy SQLAlchemy setup (tidak benar-benar terhubung ke database)
# Ini untuk menjaga kompatibilitas dengan kode yang ada
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Kita akan menggunakan Supabase untuk operasi database sebenarnya
# Lihat file app/supabase_client.py untuk koneksi Supabase
