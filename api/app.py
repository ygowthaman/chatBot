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

thread = client.beta.threads.create(
    messages=chat_history
)


def get_image_paths(topic: str) -> str:
    ic("IMAGE PATHS CALLED")
    global functionflag
    functionflag = True
    
    images_dict = {}
    main_folder = "static/images"
    topic_folder = os.path.join(main_folder, topic)
    images = os.listdir(topic_folder)
    image_paths = [os.path.join(topic_folder, img) for img in images]
    images_dict[topic] = image_paths
    ic(images_dict)
    
    return str(images_dict)


def make_diskSpaceUsage_graph(loc: str) -> str:
    ic("DISK SPACE USAGE CALLED")
    global functionflag
    functionflag = True
    
    data = np.random.normal(0, 5, 1000)
    counts, bins, patches = plt.hist(data, bins=5, edgecolor='black', range=(0,5))

    for i in range(len(bins) - 1):
        bar_height = counts[i]
        if bar_height >= 80:
            patches[i].set_facecolor('red')
        elif bar_height >= 60:
            patches[i].set_facecolor('orange')
        else:
            patches[i].set_facecolor('yellow')
            
    plt.savefig("static/histogram.png")
    plt.close()
    print("make_diskSpaceUsage_graph() called\n" + loc)
    
    return "Done"

@app.route('/time', methods=["GET"])
def get_current_time():
    return {'time': time.time()}
  
@app.route("/chat", methods=["POST"])
def chat():
    global functionflag
    functionflag = False
    
    content = request.json["message"]
    
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )
    
    return jsonify(success=True)
  
@app.route("/stream", methods=["GET"])
def stream():
    class EventHandler(AssistantEventHandler):
        @override
        def on_event(self, event):
            if event.event == 'thread.run.requires_action':
                run_id = event.data.id
                self.handle_requires_action(event.data, run_id)
        
        def handle_requires_action(self, data, run_id):
            global response
            tool_outputs = []
                
            for tool in data.required_action.submit_tool_outputs.tool_calls:
                if tool.function.name == "get_image_paths":
                    data = json.loads(tool.function.arguments)
                    topic = data["topic"]
                    output = get_image_paths(topic)
                    tool_outputs.append({"tool_call_id": tool.id, "output": output})
                    global response
                    response = output # This is a dictionary
                    
            for tool in data.required_action.submit_tool_outputs.tool_calls:
                if tool.function.name == "make_diskSpaceUsage_graph":
                    data = json.loads(tool.function.arguments)
                    location = data["location"]
                    output = make_diskSpaceUsage_graph(location)
                    tool_outputs.append({"tool_call_id": tool.id, "output": output})
                    response = output # simply "True"
                
            self.submit_tool_outputs(tool_outputs, run_id)
        
        def submit_tool_outputs(self, tool_outputs, run_id):
            with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=EventHandler(),
            ) as stream:
                for text in stream.text_deltas:
                    pass
                
        @override
        def on_message_done(self, message) -> None:
            if not functionflag:
                global response
                response = message.content[0].text.value
    
    
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id="asst_qbKv0cuYmYjW1ydvKj24vr9V",
        event_handler=EventHandler()
    ) as stream:
        stream.until_done()
        
        
    ic(response)    
    return response
