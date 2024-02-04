"""File with settings and configs for the project"""

from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5432/postgresAPI"
)  # connect string for the database
