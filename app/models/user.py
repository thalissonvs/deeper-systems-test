from dataclasses import dataclass

@dataclass
class User:
	username: str
	password: str
	roles: list
	preferences: 'UserPreferences'
	active: bool
	created_ts: float

@dataclass
class UserPreferences:
	timezone: str