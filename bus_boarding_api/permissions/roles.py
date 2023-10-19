from enum import Enum
from bus_boarding_api.permissions.models_permissions import *


class Role(str, Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    BUS_ADMIN = "BUS_ADMIN"
    USER = "USER"

    @classmethod
    def get_roles(cls):
        values = []
        for member in cls:
            values.append(f"{member.value}")
        return values


ROLE_PERMISSIONS = {
    Role.ADMINISTRATOR: [
        [
            User.permissions.CREATE,
            User.permissions.READ,
            User.permissions.UPDATE,
            User.permissions.DELETE
        ],
        [
            Bus.permissions.CREATE,
            Bus.permissions.READ,
            Bus.permissions.UPDATE,
            Bus.permissions.DELETE
        ],
        [
            BusAdmin.permissions.CREATE,
            BusAdmin.permissions.READ,
            BusAdmin.permissions.UPDATE,
            BusAdmin.permissions.DELETE
        ],
        [
            BusStop.permissions.CREATE,
            BusStop.permissions.READ,
            BusStop.permissions.UPDATE,
            BusStop.permissions.DELETE
        ],
        [
            BoardingRecord.permissions.CREATE,
            BoardingRecord.permissions.READ,
            BoardingRecord.permissions.UPDATE,
            BoardingRecord.permissions.DELETE
        ]
    ],

    Role.BUS_ADMIN: [
        [
            BoardingRecord.permissions.CREATE,
            BoardingRecord.permissions.READ,
            BoardingRecord.permissions.UPDATE
        ]
    ],

    Role.USER: [
        [
            Bus.permissions.READ
        ],
        [
            BusStop.permissions.READ
        ],
        [
            BoardingRecord.permissions.READ
        ]
    ]
}


def get_role_permissions(role: Role):
    permissions = set()
    for permissions_group in ROLE_PERMISSIONS[role]:
        for permission in permissions_group:
            permissions.add(str(permission))
    return list(permissions)
