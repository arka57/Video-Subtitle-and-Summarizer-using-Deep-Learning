from src1.logger import logging
from flask import Flask

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    logging.info("We are testing logging file")
    return "Hello World"

if __name__=="__main__":
    app.run(debug=True)