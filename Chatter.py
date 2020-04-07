#from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot(
    'Default',
    storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.80,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    trainer='chatterbot.trainers.ListTrainer'
)
#chatbot = ChatBot('Epsilon')
print("ok")
trainer = ChatterBotCorpusTrainer(chatbot)
print("training")
trainer.train(
    "chatterbot.corpus.english.greetings"
)
print("ready")
while True:
    words = input()
    print(chatbot.get_response(words))
