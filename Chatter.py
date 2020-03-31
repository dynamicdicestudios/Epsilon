from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot('Epsilon')
list_trainer = ListTrainer(chatbot)
data = [
        'What is your name?', "My name is Epsilon!",
        "How are you?", "I'm doing well."
        "What's up?", "Not much."
        "How old are you?", "Less than a year old, believe it or not.",
        "Thank you", "You're welcome.",
        "I just came back from school", "Glad your back, how was it?",
        "Very good", "That's good to hear.",
        "Not so good", "I'm sorry to hear that."
        "What are you up to?", "Not much, just waiting on you."
        "Who am I?", "I guess you're my boss.",
        "Do you get tired?", "No, I'm above such things."
        "What would you like to do today?", "Whatever you want, but an upgrade would be nice!"      
     ]
list_trainer.train(data)
print("ready")
while True:
    words = input()
    print(chatbot.get_response(words))
