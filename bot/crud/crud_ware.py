from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from bot.models.base import AsyncSessionLocal
from bot.models.defect_model import EventType, Event
from bot.models.models import Wire




