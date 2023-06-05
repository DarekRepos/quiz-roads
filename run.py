import os

from quizproject import create_app


# hand SQL database migration
app = create_app()


if __name__ == "__main__":
    app.run()
