import datetime
from fastapi import Body, HTTPException, APIRouter, Depends, Path, Query, status
from typing import Optional
import core.service as service
from auth.jwt_bearer import JWTBearer
import os

router = APIRouter()

