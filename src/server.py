import os
from agno.playground import Playground

from src.orchestrator import reasoning_social_media_team

playground = Playground(teams=[reasoning_social_media_team])
app = playground.get_app()

if __name__ == "__main__":
    playground.serve(f"src.server:app", reload=True)
