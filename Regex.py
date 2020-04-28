from nltk.chat.util import Chat, reflections

pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today?",]
    ],
     [
        r"what is your name ?",
        ["My name is Epsilon!", "My name is Epsilon! Who are you?",]
    ],
    [
        r"how are you (.*)?",
        ["I am doing well.", "I'm doing well. How about you?",]
    ],
    [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind",]
    ],
    [
        r"i(?i) (am|'m) doing (good|well|fine|okay)",
        ["Nice to hear that","Alright",]
    ],
    [
        r"(hi|hey|hello|what's up)(?i)",
        ["Hello", "Hey there",]
    ],
    [
        r"(.*) age?",
        ["I'm a bit over a year old, believe it or not!",]
        
    ],
    [
        r" w(?i)ho created you?",
        ["Josiah created me!"]
    ],
    [
        r"how is weather in (.*)?",
        ["Weather in %1 is awesome like always","Too hot man here in %1","Too cold man here in %1","Never even heard about %1"]
    ],
    [
        r"i work in (.*)?",
        ["%1 is an Amazing company, I have heard about it. But they are in huge loss these days.",]
    ],
[
        r"(.*)raining in (.*)",
        ["No rain since last week here in %2","Damn its raining too much here in %2"]
    ],
    [
        r"how (.*) health(.*)",
        ["I'm a computer program, so I'm always healthy ",]
    ],
    [
        r"(.*) (sports|game) ?",
        ["I'm a very big fan of Football",]
    ],
]

chat = Chat(pairs, reflections)
chat.converse()
