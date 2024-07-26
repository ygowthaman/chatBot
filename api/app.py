from flask import (Flask, render_template, request, jsonify)
from openai import AssistantEventHandler, OpenAI
from typing_extensions import override
from icecream import ic
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import time

client = OpenAI()

app = Flask(__name__)

response = {}

functionflag = False

chat_history = [{"role": "assistant", "content": "Hello! I am the Netscout Assistant! How can I help you?"}]

@app.route('/time')
def get_current_time():
    return {'time': time.time()}