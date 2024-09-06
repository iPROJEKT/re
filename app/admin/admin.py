from fastapi import Request
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from bot.models.admin import User
from bot.models.base import get_async_session, engine
from fastapi.security import OAuth2PasswordBearer

from bot.models.models import Nozzle, Mudguard, Diffuser, Intestine, Rolls, Tip, Gaz, Wire

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form_data = await request.form()
        username = form_data.get('username')
        password = form_data.get('password')

        async with get_async_session() as session:
            admin_user = await session.execute(
                select(User).filter(User.username == username)
            )
            admin_user = admin_user.scalar_one_or_none()

            if admin_user and self.verify_password(password, admin_user.hashed_password):
                request.session.update({"token": self.create_token(admin_user.id)})
                return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        # Здесь добавьте логику проверки токена, если требуется
        return True

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return plain_password == hashed_password

    def create_token(self, user_id: int) -> str:
        return f"token-{user_id}"


def get_admin():
    from app.core.core import app
    authentication_backend = AdminAuth(secret_key="your-secret-key")
    admin = Admin(app, engine, authentication_backend=authentication_backend)

    class UserAdmin(ModelView, model=User):
        column_list = [User.id, User.username]

    class WireAdmin(ModelView, model=Wire):
        column_list = [Wire.wire_mark, Wire.wire_diameter]
        column_details_exclude_list = ['wire.robots']
        page_size = 50

    class GazAdmin(ModelView, model=Gaz):
        column_list = [Gaz.gaz_name, Gaz.gaz_type_obj]

    class TipAdmin(ModelView, model=Tip):
        column_list = [Tip.tip_diameter, Tip.tip_type]

    class RollsAdmin(ModelView, model=Rolls):
        column_list = [Rolls.rolls_cutout_type, Rolls.rolls_color, Rolls.rolls_ware_dim]

    class IntestineAdmin(ModelView, model=Intestine):
        column_list = [Intestine.intestine_color, Intestine.intestine_diameter, Intestine.intestine_length]

    class DiffuserAdmin(ModelView, model=Diffuser):
        column_list = [Diffuser.diffuser_thread]

    class MudguardAdmin(ModelView, model=Mudguard):
        column_list = [Mudguard.mudguard_material]

    class NozzleAdmin(ModelView, model=Nozzle):
        column_list = [Nozzle.nozzle_form]

    admin.add_view(GazAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(WireAdmin)
    admin.add_view(TipAdmin)
    admin.add_view(RollsAdmin)
    admin.add_view(IntestineAdmin)
    admin.add_view(DiffuserAdmin)
    admin.add_view(MudguardAdmin)
    admin.add_view(NozzleAdmin)

    return admin


admin = get_admin()
