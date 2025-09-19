import os, enum, re, jwt

# typing
from typing import List, Optional, Annotated


# fastapi
from fastapi import (
    APIRouter, FastAPI, Depends, HTTPException, 
    Query, status, UploadFile, File
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# passlib
from passlib.hash import bcrypt

# pydantic
from pydantic import (
    BaseModel, EmailStr, StringConstraints, field_validator
)

# dotenv import
from dotenv import load_dotenv

# datetime imports
from datetime import datetime, timezone, time, timedelta

# sqlalchemy imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, validates, sessionmaker
from sqlalchemy.sql import func

from sqlalchemy import (
    Column, Integer, BigInteger, SmallInteger, Float, Boolean,
    String, Enum, DateTime, ForeignKey, UniqueConstraint, CheckConstraint,
    Time, Text, create_engine
)

# core
from core.dependency import get_current_user
from core.jwt import create_access_token, decode_access_token
from core.security import hash_password, verify_password

# routes
from routes import (
    auth
)
