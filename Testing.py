import nltk, tflearn, tensorflow, random, json, pickle, sys, unicodedata
import numpy as np
from nltk.stem.lancaster import LancasterStemmer

# a table structure to hold the different punctuation used
tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P'))

# method to remove punctuations from sentences.
def remove_punctuation(text):
    return str(text).translate(tbl)

# initialize the stemmer
stemmer = LancasterStemmer()

# variable to hold the Json data read from the file
data = None
# read the json file and load the training data
with open('intents.json') as json_data:
    data = json.load(json_data)
    print(data)
    
try:
    with open("data.pickle", "rb") as f:
        words, categories, training, output = pickle.load(f)
except:       
    # get a list of all categories to train for
    categories = []
    words = []
    # a list of tuples with words in the sentence and category name
    docs = []
    for intents in data["intents"]:
        for pattern in intents["patterns"]:
            # remove any punctuation from the sentence
            pattern = remove_punctuation(pattern)
            print(pattern)
            # extract words from each sentence and append to the word list
            w = nltk.word_tokenize(pattern)
            print("tokenized words: ", w)
            words.extend(w)
            docs.append((w, intents))
        
        categories.append(intents["tag"])
    # stem and lower each word and remove duplicates
    words = [stemmer.stem(w.lower()) for w in words]
    words = sorted(list(set(words)))
    #print(categories)

    # create our training data
    training = []
    output = []
    # create an empty array for our output
    output_empty = [0] * len(categories)
    for doc in docs:
        # initialize our bag of words(bow) for each document in the list
        bow = []
        # list of tokenized words for the pattern
        token_words = doc[0]
        # stem each word
        token_words = [stemmer.stem(word.lower()) for word in token_words]
        # create our bag of words array
        for w in words:
            bow.append(1) if w in token_words else bow.append(0)
        output_row = list(output_empty)
        output_row[categories.index(doc[1]["tag"])] = 1
        # our training set will contain a the bag of words model and the output row that tells
        # which catefory that bow belongs to.
        training.append(bow)
        output.append(output_row)

    # shuffle our features and turn into np.array as tensorflow  takes in numpy array
    random.shuffle(training)
    random.shuffle(output)

    training = np.array(training)
    output = np.array(output)
    # trainX contains the Bag of words and train_y contains the label/ category
    #train_x = list(training[:, 0])
    #train_y = list(training[:, 1])

    with open("data.pickle", "wb") as f:
        pickle.dump((words, categories, training, output), f)

# reset underlying graph data
tensorflow.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)
# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

try:
    model.load("model.tflearn")
except:
    # Start training (apply gradient descent algorithm)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save('model.tflearn')

def get_tf_record(sentence):
    global words
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    # bag of words
    bow = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bow[i] = 1
    return(np.array(bow))

def model_response(query):
    results = model.predict([get_tf_record(query)])[0]
    results_index = np.argmax(results)
    tag = categories[results_index]
    
    if results[results_index] > 0.6:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        return [tag, random.choice(responses)]
    else:
        return "Sorry, I'm not sure what you mean."

while True:
    query = input()
    print(model_response(query))
