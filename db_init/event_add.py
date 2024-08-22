import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.base import Base, AsyncSessionLocal
from bot.models.defect_model import (
    Cleaning, Setting, Defect, MechanicalFault, ProgramError,
    ModeDeviation, GasProtectionViolation, Event, CleaningType, SettingType, DefectType, ProgramErrorType,
    MechanicalFaultType, GasProtectionViolationType, ModeDeviationType, EventType
)


async def create_objects(session: AsyncSession):
    async with session.begin():
        # Создание объектов для каждой таблицы
        cleanings = [Cleaning(type=type) for type in CleaningType]
        settings = [Setting(type=type) for type in SettingType]
        defects = [Defect(type=type) for type in DefectType]
        mechanical_faults = [MechanicalFault(type=type) for type in MechanicalFaultType]
        program_errors = [ProgramError(type=type) for type in ProgramErrorType]
        mode_deviations = [ModeDeviation(type=type) for type in ModeDeviationType]
        gas_protection_violations = [GasProtectionViolation(type=type) for type in GasProtectionViolationType]

        # Добавление объектов в базу данных
        session.add_all(cleanings)
        session.add_all(settings)
        session.add_all(defects)
        session.add_all(mechanical_faults)
        session.add_all(program_errors)
        session.add_all(mode_deviations)
        session.add_all(gas_protection_violations)
        await session.flush()  # Убедитесь, что все объекты сохранены и у них есть ID

        # Создание объектов для таблицы Event
        events = [
            Event(event_type=EventType.CLEANING, cleaning_id=cleanings[0].id),
            Event(event_type=EventType.SETTING, setting_id=settings[0].id),
            Event(event_type=EventType.DEFECT, defect_id=defects[0].id),
            Event(event_type=EventType.MECHANICAL_FAULT, mechanical_fault_id=mechanical_faults[0].id),
            Event(event_type=EventType.PROGRAM_ERROR, program_error_id=program_errors[0].id),
            Event(event_type=EventType.MODE_DEVIATION, mode_deviation_id=mode_deviations[0].id),
            Event(event_type=EventType.GAS_PROTECTION_VIOLATION, gas_protection_violation_id=gas_protection_violations[0].id),
        ]

        # Добавление объектов событий в базу данных
        session.add_all(events)
        await session.commit()


async def main():
    async with AsyncSessionLocal() as session:
        await create_objects(session)


asyncio.run(main())
