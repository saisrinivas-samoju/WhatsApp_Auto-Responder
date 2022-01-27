import pyautogui as pt
from time import sleep
import pyperclip
import random

sleep(3)

position1 = pt.locateOnScreen("smiley_paperclip.png", confidence = .6)
x = position1[0]
y = position1[1]


####################### Chatbot Code ##########################
import random
import json
import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


# Get message
def get_message():
    global x, y
    position = pt.locateOnScreen("smiley_paperclip.png", confidence = .6)
    x = position[0]
    y = position[1]
    pt.moveTo(x, y, duration = .05)
    pt.moveTo(x + 100, y - 45, duration = 0.05)
    pt.tripleClick()
    pt.rightClick()
    pt.moveRel(50, -565)
    pt.click()
    whatsapp_message = pyperclip.paste()
    pt.moveRel(-50, +590)
    pt.click()
    print("Message received: " + whatsapp_message)
    return whatsapp_message


# Posts
def post_response(message):
    global x, y
    position = pt.locateOnScreen("smiley_paperclip.png", confidence = .6)
    x = position[0]
    y = position[1]
    pt.moveTo(x + 200, y + 20, duration=.05)
    pt.click()
    pt.typewrite(message, interval = 0.01)
    pt.typewrite("\n", interval = 0.01)


def process_response(sentence):
    # Using chatbot files for this autoresponder
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    prev_tag = []
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    else:
        return random.choice(["I don't understand", "Sorry! I am not trained completely yet.", "Sorry! I can't help you."])  # this is temporary.


# Check for new messages
def check_for_new_messages():
    pt.moveTo(x + 100, y - 35)
    while True:
        # Continously checks for green dot and new messages
        try:
            position = pt.locateOnScreen("green_circle.png", confidence = .7)
            if position is not None:
                pt.moveTo(position)
                pt.moveRel(-100, 0)
                pt.click()
                sleep(.1)

        except(Exception):
            print("No new other users with new messages located")

        if pt.pixelMatchesColor(int(x + 100), int(y - 35), (255, 255, 255), tolerance=10):
            print("is_white")
            processed_message = process_response(get_message())
            post_response(processed_message)
        else:
            print("No new messages yet...")
        sleep(1)         # time it takes before checking for a new message.

check_for_new_messages()
