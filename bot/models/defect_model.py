from sqlalchemy import Column, Enum, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum

from bot.models.models import UserWAAMer
from bot.core.utils import moscow_now
from bot.models.base import Base
from bot.models.models import MOSCOW_TZ


class CleaningType(enum.Enum):
    CENTRAL_NOZZLE = 'Очистка сопла центрального'
    ADDITIONAL_NOZZLE = 'Очистка сопла дополнительного'
    CHANNEL = 'Очистка канала (продувка)'


class SettingType(enum.Enum):
    UTOOL = 'UTool'
    UFRAME = 'UFRAME'
    REGISTER = 'Register'


class EventType(enum.Enum):
    CLEANING = 'Cleaning'
    SETTING = 'Setting'
    DEFECT = 'Defect'
    MECHANICAL_FAULT = 'MechanicalFault'
    PROGRAM_ERROR = 'ProgramError'
    MODE_DEVIATION = 'ModeDeviation'
    GAS_PROTECTION_VIOLATION = 'GasProtectionViolation'


class DefectType(enum.Enum):
    DEFORMATIONS = 'Деформации'
    POROSITY = 'Поры'
    UNFUSED = 'Несплавления'
    UNDERCUTS = 'Подрезы'
    CRACKS = 'Трещины'
    BURNTHROUGH = 'Прожиг'


class MechanicalFaultType(enum.Enum):
    FAULT_1 = 'Mechanical Fault 1'
    FAULT_2 = 'Mechanical Fault 2'


class ProgramErrorType(enum.Enum):
    COLLISION = 'Коллизия'
    GEOMETRY_MISMATCH = 'Несоответствие геометрии'
    PREMATURE_END = 'Преждевременное окончание УП'
    CONTROLLER_ERROR = 'Ошибка контроллера'


class ModeDeviationType(enum.Enum):
    WELDING_CONTROL = 'Контроль сварки'
    STABILITY_VIOLATION = 'Нарушение стабильности'
    ARC_IGNITION_ERROR = 'Ошибка зажигания дуги'


class GasProtectionViolationType(enum.Enum):
    LOW_GAS_PRESSURE = 'Низкое давление газа'
    LOW_GAS_FLOW = 'Низкий расход газа'


class Cleaning(Base):
    type = Column(Enum(CleaningType), nullable=False, doc='Тип очистки')


class Setting(Base):
    type = Column(Enum(SettingType), nullable=False, doc='Тип настройки')


class Defect(Base):
    type = Column(Enum(DefectType), nullable=False, doc='Тип дефекта')


class MechanicalFault(Base):
    type = Column(Enum(MechanicalFaultType), nullable=False, doc='Тип механической неисправности')


class ProgramError(Base):
    type = Column(Enum(ProgramErrorType), nullable=False, doc='Тип ошибки программы')


class ModeDeviation(Base):
    type = Column(Enum(ModeDeviationType), nullable=False, doc='Тип отклонения от режима')


class GasProtectionViolation(Base):
    type = Column(Enum(GasProtectionViolationType), nullable=False, doc='Тип нарушения газовой защиты')


class Event(Base):
    robot_id = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('userwaamer.id'), nullable=False)
    message = Column(String, nullable=True, doc='Комментарий')
    user_message = Column(String, nullable=True, doc='Комментарий')
    event_type = Column(Enum(EventType), nullable=False, doc='Тип события')
    datarime = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    cleaning_id = Column(Integer, ForeignKey('cleaning.id'), nullable=True)
    setting_id = Column(Integer, ForeignKey('setting.id'), nullable=True)
    defect_id = Column(Integer, ForeignKey('defect.id'), nullable=True)
    mechanical_fault_id = Column(Integer, ForeignKey('mechanicalfault.id'), nullable=True)
    program_error_id = Column(Integer, ForeignKey('programerror.id'), nullable=True)
    mode_deviation_id = Column(Integer, ForeignKey('modedeviation.id'), nullable=True)
    gas_protection_violation_id = Column(Integer, ForeignKey('gasprotectionviolation.id'), nullable=True)

    user = relationship('UserWAAMer')
    cleaning = relationship('Cleaning')
    setting = relationship('Setting')
    defect = relationship('Defect')
    mechanical_fault = relationship('MechanicalFault')
    program_error = relationship('ProgramError')
    mode_deviation = relationship('ModeDeviation')
    gas_protection_violation = relationship('GasProtectionViolation')

    def get_event_details(self):
        if self.event_type == EventType.CLEANING:
            return self.cleaning
        elif self.event_type == EventType.SETTING:
            return self.setting
        elif self.event_type == EventType.DEFECT:
            return self.defect
        elif self.event_type == EventType.MECHANICAL_FAULT:
            return self.mechanical_fault
        elif self.event_type == EventType.PROGRAM_ERROR:
            return self.program_error
        elif self.event_type == EventType.MODE_DEVIATION:
            return self.mode_deviation
        elif self.event_type == EventType.GAS_PROTECTION_VIOLATION:
            return self.gas_protection_violation
        return None
