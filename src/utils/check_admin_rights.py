from loader import list_of_admins


def is_admin(tg_id: int):
    return list_of_admins.find_one({'id': tg_id})


def is_superadmin(tg_id: int) -> bool:
    admin = list_of_admins.find_one({'id': tg_id})
    if admin:
        return admin['main admin']
