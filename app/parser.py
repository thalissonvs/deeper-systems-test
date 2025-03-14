from dataclasses import asdict
import json
from datetime import datetime
from app.database import get_collection
from app.models.user import User, UserPreferences


class UserParser:
    @staticmethod
    def parse(file_path: str):
        users = []
        with open(file_path, 'r') as file:
            data = json.load(file)

        for user in data['users']:
            user_roles = UserParser._get_user_roles(user)
            created_ts = datetime.strptime(user['created_at'], '%Y-%m-%dT%H:%M:%SZ').timestamp()
            user_obj = User(
				username=user['user'],
				password=user['password'],
				roles=user_roles,
				preferences=UserPreferences(timezone=user['user_timezone']),
				active=user['is_user_active'],
				created_ts=created_ts
			)
            users.append(user_obj)
        return users

    @staticmethod
    def _get_user_roles(user: dict) -> list:
        user_roles = []
        if user['is_user_admin']:
            user_roles.append('admin')
        if user['is_user_manager']:
            user_roles.append('manager')
        if user['is_user_tester']:
            user_roles.append('tester')
        return user_roles



if __name__ == '__main__':
    parser = UserParser()
    users = parser.parse('udata.json')
    collection = get_collection('users')

    for user in users:
        collection.insert_one(asdict(user))
