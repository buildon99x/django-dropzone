set batch_dir=%~dp0
start cmd /k "@TITLE SUPERSET Server & %batch_dir%venv\scripts\activate & python %batch_dir%src\run_server.py"
