#runserver.py
from waitress import serve

from mysite.wsgi import application
print("Starting server...")
if __name__ == '__main__':
    serve(application, host='localhost', port='8000')