from EmailSender import send
from EmailSender import send, get_message_body
import pickle

ichi_dict = pickle.load(open('E:/ichimoku_screener/ichi_dict.p', 'rb'))
print(ichi_dict)
send(ichi_dict, get_message_body(ichi_dict))