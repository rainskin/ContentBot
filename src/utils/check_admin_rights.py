from loader import list_of_admins, sales


def is_admin(tg_id: int):
    return list_of_admins.find_one({'id': tg_id})


def is_superadmin(tg_id: int) -> bool:
    admin = list_of_admins.find_one({'id': tg_id})
    if admin:
        return admin['main admin']


def is_salesman(name: str, sale_msg_id: int) -> bool:
    sale = sales.find_one({'sale_msg_id': sale_msg_id})
    return sale['salesman'] == name
