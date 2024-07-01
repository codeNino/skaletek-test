from enum import Enum
import os, json
from dotenv import load_dotenv

load_dotenv()


class Environment(Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

    @property
    def is_local(self):
        return self in {Environment.LOCAL, Environment.DEVELOPMENT}

    @classmethod
    def from_string(cls, env_str: str):
        try:
            return cls[env_str.upper()]
        except KeyError:
            raise ValueError(f"Unknown environment: {env_str}")

class Config:

    ## application
    PORT = int(os.environ.get("PORT", "8000"))
    ENV : Environment = Environment.from_string(os.environ.get("ENVIRONMENT", "development"))
    ALLOWED_ORIGINS = json.loads(os.environ.get("ALLOWED_ORIGINS", '["*"]'))
    API_KEY = os.environ.get("API_KEY", "")
   