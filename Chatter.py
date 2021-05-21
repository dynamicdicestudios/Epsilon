from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
import warnings, time
warnings.filterwarnings("ignore")

chatbot = ChatBot(
    'Epsilon',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            "statement_comparison_function": 'chatterbot.comparisons.LevenshteinDistance',
            'default_response': "I'm not quite sure what you mean.",
            'maximum_similarity_threshold': 0.95
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        }
    ]
)

def train():
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train(
        "chatterbot.corpus.english.greetings",
        "chatterbot.corpus.english.persona",
        "chatterbot.corpus.english.notes",
        "chatterbot.corpus.english.battery",
        "chatterbot.corpus.english.joke",
        "chatterbot.corpus.english.help",
        "chatterbot.corpus.english.time",
        "chatterbot.corpus.english.button",
        "chatterbot.corpus.english.handsfree"
    )

def chatter_response(words):
    if words.lower().startswith("learn"):
        words = words.split(" ")
        state = words[1:words.index("for")]
        prev = words[(words.index("for"))+1:words.index("corpus")]
        file = words[(words.index("corpus"))+1]

        update = open(r"C:\Users\Josiah\AppData\Local\Programs\Python\Python36\Lib\site-packages\chatterbot_corpus\data\english\{}".format("".join(file) + ".yml"), "a")

        update.write("\n- - " + " ".join(prev) + "\n")
        update.write("  - " + " ".join(state) + "\n")

        update.close()
        train()
        return "Okay I know that now."
    elif "train" in words.lower():
        train()
        return "All done training!"
    else:
        return chatbot.get_response(words)

while True:
    response = input("What would you like to say to Epsilon? ")
    print(chatter_response(response))
    
