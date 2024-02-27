from flask import Flask
from pytileTester import main as PyTile
import asyncio

app = Flask(__name__)

@app.route('/')
def hello():

    loop = asyncio.new_event_loop()
    location = loop.run_until_complete(PyTile())
    loop.close()
    return f'<h1>Hello from Flask! The dog is at: {location}</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)