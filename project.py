# -*- coding: utf-8 -*-

import random
import re
import tkinter as tk
from tkinter import scrolledtext


context = None
user_name = None


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text

def match_keywords(user_input, keywords):
    for word in keywords:
        if word in user_input:
            return True
    return False


responses = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"],
        "answers": [
            "Hello! 😊",
            "Hi there! 😄",
            "Hey! 👋"
        ]
    },
    "daily": {
        "keywords": [
            "how are you", "what are you doing", "how's it going", "what's up",
            "how are you doing", "what's new", "how's everything", "what's going on", "how's your day"
            ],
        "answers": [
            "I'm doing great! 😊",
            "Just chatting with you 😄",
            "Always here to help 💙"
        ]
    },
    "emotion_happy": {
        "keywords": ["happy", "good", "great", "excited", "fantastic", "amazing", "awesome", "wonderful", "joyful", "cheerful"],
        "answers": [
            "That's amazing! 😍",
            "I'm really happy for you!",
            "Keep smiling! 😄"
        ]
    },
    "emotion_sad": {
        "keywords": [
            "sad", "down", "upset", "depressed", "lonely", 
            "heartbroken", "miserable", "unhappy", "blue", "gloomy"
            ],
        "answers": [
            "I'm here for you 💙",
            "Things will get better 🌸",
            "You're stronger than you think 💪"
        ]
    },
    "bored": {
        "keywords": [
            "bored", "nothing to do", "boredom", "bored out of my mind",
            "so bored", "bored as hell", "bored to death", "bored stiff", "bored to tears"
            ],
        "answers": [
            "Want me to suggest something fun? 🎯",
            "Let’s find something interesting! 😄"
        ]
    },
    "stress": { 
        "keywords": [
            "stress", "tired", "depressed","anxious", "overwhelmed", "burnout", "stressed",
            "exhausted", "worried", "nervous", "frustrated", "sad", "down", "unhappy",
            "overloaded", "pressure", "tense", "upset", "worried", "anxiety"
            ],
            "answers": [
                "Take a deep breath. You got this.", "Try to relax and take a break.", "Rest is important!"
            ] 
    },
    "study": {
        "keywords": [
            "study", "exam", "homework", "project", "assignment",
            "test", "quiz", "research", "paper", "presentation", "coursework", "revision"
        ],
        "answers": [
            "Study in small sessions 📚",
            "Make a simple plan ✏️",
            "You can do it! 💪"
        ]
    },
    "yes": { 
        "keywords": [
            "yes", "yeah", "yep", "sure", "of course", "definitely", "absolutely", "yup"
            ],
        "answers": [
            "Great! 😄", "Awesome! 🎉", "Nice! 👍" 
            ] 
    },
    "thanks": {
        "keywords": [
            "thanks", "thank you", "thx", "thank", "ty", "thanks a lot", "thank you very much",
            "thanks so much", "thank you so much", "thanks a bunch", "thank you kindly"
            ],
        "answers": [
            "You're welcome 😊",
            "Anytime! 😄"
        ]
    },
    "ok": {
        "keywords": ["ok", "okay", "alright"],
        "answers": [
            "Alright! 😊",
            "Got it 👍"
        ]
    },
    "no": { 
        "keywords": [
            "no", "nope", "nah", "not really", "don't", "do not", 
            "never", "no way", "not at all", "negative", "nay", "no thanks", "not sure"
            ],
        "answers": [ 
            "Alright 😊", 
            "No problem 👍",
            "Okay!" 
        ] 
    },
}


def chatbot_response(user_input):
    global context, user_name
    clean_input = preprocess(user_input)

    # Exit
    if clean_input in ["bye", "goodbye"]:
        return f"Goodbye {user_name if user_name else ''}! 👋"


    if context == "ask_name":
        user_name = user_input.strip().capitalize()
        context = None
        return f"Nice to meet you {user_name}! 😊 How are you today?"


    if context == "ask_activity":
        context = None

        if "study" in clean_input:
            return "That's great! Keep going 📚"
        elif "nothing" in clean_input:
            return "Sometimes doing nothing is relaxing 😄"
        elif "work" in clean_input:
            return "Nice! Stay productive 💼"
        else:
            return "Sounds interesting! Tell me more 😊"


    if context == "bored_suggestion":
        if "yes" in clean_input:
            context = None
            return "You can watch a movie 🎬, read a book 📖, or learn Python 😎"
        elif "no" in clean_input:
            context = None
            return "No worries 😊 Maybe just relax!"


    for intent in responses:
        if match_keywords(clean_input, responses[intent]["keywords"]):

            if intent == "greeting":
                if not user_name:
                    context = "ask_name"
                    return random.choice(responses[intent]["answers"]) + " What's your name?"
                else:
                    return f"{random.choice(responses[intent]['answers'])} {user_name}!"

            if intent == "daily":
                context = "ask_activity"
                return random.choice(responses[intent]["answers"]) + " What about you?"

            if intent == "bored":
                context = "bored_suggestion"

            return random.choice(responses[intent]["answers"])


    if "life" in clean_input:
        return "Life can be complicated sometimes… but you're doing your best 💙"
    if "future" in clean_input:
        return "The future is full of opportunities ✨ What do you want to achieve?"
    if "alone" in clean_input:
        return "You're not alone, I'm here with you 💙"

    return "Hmm 🤔 I didn't understand. Can you tell me more?"


def save_chat(user, bot):
    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(f"You: {user}\n")
        file.write(f"Bot: {bot}\n")


def send_message(event=None):
    user_text = entry.get()

    if user_text.strip() == "":
        return

    chat_window.insert(tk.END, "You: " + user_text + "\n")

    bot_reply = chatbot_response(user_text)
    chat_window.insert(tk.END, "Bot: " + bot_reply + "\n\n")

    save_chat(user_text, bot_reply)

    chat_window.yview(tk.END)

    entry.delete(0, tk.END)


window = tk.Tk()
window.title("Smart Chatbot 🤖")

chat_window = scrolledtext.ScrolledText(window, width=50, height=20, font=("Arial", 12))
chat_window.pack()

entry = tk.Entry(window, width=40, font=("Arial", 12))
entry.pack()

send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

window.bind('<Return>', lambda event: send_message())


window.mainloop()