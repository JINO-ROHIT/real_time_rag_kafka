import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
load_dotenv()

app = App(token = os.environ.get('SLACK_OATH_TOKEN', default=''))

@app.message(".*")
def message_handler(message, say, logger):
    #print(message)
    print(message['text'])
    
    output = "hey this is june"   
    say(output)



if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get('SLACK_APP_TOKEN', default='')).start()