import pytz

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from bot.core.utils import moscow_now
from bot.models.base import Base


MOSCOW_TZ = pytz.timezone('Europe/Moscow')


class UserWAAMer(Base):
    """Model describing the user (Пользователь)

    Attributes:
    - telegram_user_id (int): Телеграм ID пользователя.
    - name (str): Имя пользователя.
    - surname (str): Фамилия пользователя (может быть пустым).
    - number_robot (int): Номер установки, с которой связан пользователь.
    - is_admin (bool): Флаг, указывающий на статус администратора.
    - change (relationship): Связь с моделью изменений (Change).
    """
    telegram_user_id = Column(Integer, unique=True, nullable=False, doc='Телеграм ID')
    name = Column(String, unique=False, nullable=False, doc='Имя')
    surname = Column(String, unique=False, nullable=True, doc='Фамилия')
    number_robot = Column(Integer, unique=False, nullable=False, default=0, doc='Номер установки')
    is_admin = Column(Boolean, default=False, doc='Опероуполномоченый')
    change = relationship('Change')


class Wire(Base):
    """Model describing the wire (Проволока)

    Attributes:
    - wire_mark (str): Марка проволоки.
    - wire_diameter (float): Диаметр проволоки.
    - robots (relationship): Связь с моделью роботов (Robot), использующих эту проволоку.
    """
    wire_mark = Column(String, nullable=False, doc='Марка проволоки')
    wire_diameter = Column(Float, nullable=False, doc='Диаметр проволоки')
    robots = relationship('Robot', back_populates='robot_wire')


class Gaz(Base):
    """Model describing the gaz (Газ)

    Attributes:
    - gaz_name (str): Марка газа.
    - gaz_type_obj (str): Тип контейнера (баллон/криобак).
    - robots (relationship): Связь с моделью роботов (Robot), использующих этот газ.
    """
    gaz_name = Column(String, nullable=True, doc='Марка газа')
    gaz_type_obj = Column(String, nullable=True, doc='Балон/Креобак')
    robots = relationship('Robot', back_populates='robot_gaz', foreign_keys='Robot.robot_gaz_id')


class Tip(Base):
    """Model describing the tip (Наконечник)

    Attributes:
    - tip_diameter (float): Диаметр наконечника.
    - tip_type (str): Тип наконечника (например, Cu / Cu-Cr-Zr).
    - robots (relationship): Связь с моделью роботов (Robot), использующих этот наконечник.
    """
    tip_diameter = Column(Float, nullable=False, doc='Диаметр наконечника')
    tip_type = Column(String, nullable=False, doc='Cu / Cu-Cr-Zr')
    robots = relationship('Robot', back_populates='robot_tip')


class Rolls(Base):
    """Model describing the rolls (Ролики)

    Attributes:
    - rolls_cutout_type (str): Тип выреза роликов.
    - rolls_color (str): Цвет роликов.
    - rolls_ware_dim (str): Диаметр проволоки для этих роликов.
    - robots (relationship): Связь с моделью роботов (Robot), использующих эти ролики.
    """
    rolls_cutout_type = Column(String, nullable=False, doc='Тип выреза')
    rolls_color = Column(String, nullable=False, doc='Цвет роликов')
    rolls_ware_dim = Column(String, nullable=False, doc='Диаметр проволки для роликов')
    robots = relationship('Robot', back_populates='robot_rolls')


class Intestine(Base):
    """Model describing the intestine (Кишка)

    Attributes:
    - intestine_color (str): Цвет кишки.
    - intestine_diameter (str): Диаметр кишки.
    - intestine_length (float): Длина кишки.
    - robots (relationship): Связь с моделью роботов (Robot), использующих эту кишку.
    """
    intestine_color = Column(String, nullable=False, doc='Цвет кишки')
    intestine_diameter = Column(String, nullable=False, doc='Диаметр кишки')
    intestine_length = Column(Float, nullable=False, doc='Длина кишки')
    robots = relationship('Robot', back_populates='robot_intestine')


class Diffuser(Base):
    """Model describing the diffuser (Диффузор)

    Attributes:
    - diffuser_thread (str): Резьба деффузора.
    - robots (relationship): Связь с моделью роботов (Robot), использующих этот деффузор.
    """
    diffuser_thread = Column(String, nullable=False, doc='Резьба диффузора')
    robots = relationship('Robot', back_populates='robot_diffuser')


class Mudguard(Base):
    """Model describing the mudguard (Брызговик)

    Attributes:
    - mudguard_material (str): Материал брызговика.
    - robots (relationship): Связь с моделью роботов (Robot), использующих этот брызговик.
    """
    mudguard_material = Column(String, nullable=False, doc='Материал брызговика')
    robots = relationship('Robot', back_populates='robot_mudguard')


class Nozzle(Base):
    """Model describing the nozzle (Сопло)

    Attributes:
    - nozzle_form (str): Форма сопла.
    - robots (relationship): Связь с моделью роботов (Robot), использующих это сопло.
    """
    nozzle_form = Column(String, nullable=False, doc='Форма сопла')
    robots = relationship('Robot', back_populates='robot_nozzle')


class Robot(Base):
    """Model describing the robot (Робот)

    Attributes:
    - robot_number (int): Номер ячейки робота.
    - robot_wire_id (int): Внешний ключ на проволоку (Wire).
    - robot_last_update_wire (datetime): Дата последнего обновления проволоки.
    - robot_gaz_id (int): Внешний ключ на основной газ (Gaz).
    - robot_last_update_gaz (datetime): Дата последнего обновления основного газа.
    - robot_add_gaz_id (int): Внешний ключ на дополнительный газ (Gaz).
    - robot_last_update_add_gaz (datetime): Дата последнего обновления дополнительного газа.
    - robot_tip_id (int): Внешний ключ на наконечник (Tip).
    - robot_last_update_tip (datetime): Дата последнего обновления наконечника.
    - robot_rolls_id (int): Внешний ключ на ролики (Rolls).
    - robot_last_update_rolls (datetime): Дата последнего обновления роликов.
    - robot_intestine_id (int): Внешний ключ на кишку (Intestine).
    - robot_last_update_intestine (datetime): Дата последнего обновления кишки.
    - robot_diffuser_id (int): Внешний ключ на диффузор (Diffuser).
    - robot_last_update_diffuser (datetime): Дата последнего обновления диффузора.
    - robot_mudguard_id (int): Внешний ключ на брызговик (Mudguard).
    - robot_last_update_mudguard (datetime): Дата последнего обновления брызговика.
    - robot_nozzle_id (int): Внешний ключ на сопло (Nozzle).
    - robot_last_update_nozzle (datetime): Дата последнего обновления сопла.

    Relationships:
    - robot_wire (relationship): Связь с моделью Wire.
    - robot_gaz (relationship): Связь с моделью Gaz для основного газа.
    - robot_add_gaz (relationship): Связь с моделью Gaz для дополнительного газа.
    - robot_tip (relationship): Связь с моделью Tip.
    - robot_rolls (relationship): Связь с моделью Rolls.
    - robot_intestine (relationship): Связь с моделью Intestine.
    - robot_diffuser (relationship): Связь с моделью Diffuser.
    - robot_mudguard (relationship): Связь с моделью Mudguard.
    - robot_nozzle (relationship): Связь с моделью Nozzle.
    """
    robot_number = Column(Integer, doc='Номер ячейки')
    robot_wire_id = Column(Integer, ForeignKey('wire.id'), nullable=False, doc='Проволка')
    robot_last_update_wire = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    robot_gaz_id = Column(Integer, ForeignKey('gaz.id'), nullable=False, doc='Газ')
    robot_last_update_gaz = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    robot_add_gaz_id = Column(Integer, ForeignKey('gaz.id'), nullable=True, doc='Дополнительный газ')
    robot_last_update_add_gaz = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    robot_tip_id = Column(Integer, ForeignKey('tip.id'), nullable=False, doc='Наконечник')
    robot_last_update_tip = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    robot_rolls_id = Column(Integer, ForeignKey('rolls.id'), nullable=False, doc='Ролики')
    robot_last_update_rolls = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    robot_intestine_id = Column(Integer, ForeignKey('intestine.id'), nullable=False, doc='Кишка')
    robot_last_update_intestine = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    robot_diffuser_id = Column(Integer, ForeignKey('diffuser.id'), doc='Диффузор')
    robot_last_update_diffuser = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    robot_mudguard_id = Column(Integer, ForeignKey('mudguard.id'), doc='Брызговик')
    robot_last_update_mudguard = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    robot_nozzle_id = Column(Integer, ForeignKey('nozzle.id'), doc='Сопло')
    robot_last_update_nozzle = Column(DateTime, default=moscow_now(MOSCOW_TZ))

    robot_clear_nozzle = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    robot_clear_add_nozzle = Column(DateTime, default=moscow_now(MOSCOW_TZ))
    robot_clear_intestine = Column(DateTime, default=moscow_now(MOSCOW_TZ))

    robot_wire = relationship('Wire', back_populates='robots')
    robot_gaz = relationship('Gaz', foreign_keys=[robot_gaz_id], back_populates='robots')
    robot_add_gaz = relationship('Gaz', foreign_keys=[robot_add_gaz_id])
    robot_tip = relationship('Tip', back_populates='robots')
    robot_rolls = relationship('Rolls', back_populates='robots')
    robot_intestine = relationship('Intestine', back_populates='robots')
    robot_diffuser = relationship('Diffuser', back_populates='robots')
    robot_mudguard = relationship('Mudguard', back_populates='robots')
    robot_nozzle = relationship('Nozzle', back_populates='robots')


class Change(Base):
    """Model describing the change"""
    changes_who = Column(Integer, ForeignKey('userwaamer.id'), doc='Кто поменял')
    changes_what = Column(String, nullable=False, doc='Тип заменты')
    changes_model_id = Column(Integer, doc='На что поменял ID')
    changes_time = Column(DateTime, default=moscow_now(MOSCOW_TZ), doc='Во сколько поменял')
    changes_robot = Column(Integer, doc='Робот')
