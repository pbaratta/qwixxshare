import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import random

class QwixxGameConsumer(WebsocketConsumer):
    " Gateway on the server for one particular game player "

    def connect(self):
        " with a WebSocket connection, start listening on the channel_layer "

        self.game_name = self.scope['url_route']['kwargs']['game_name']  # TODO filter characters
        self.game_group_name = f'game_{self.game_name}'

        # add this consumer to channel layer
        # print(f"joining group {self.game_group_name}")
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        " with WebSocket termination, remove from channel_layer "
        # print(f"leaving group {self.game_group_name}")
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        " receive browser input (a roll) and transmit to other players "

        data = json.loads(text_data)
        # print(f"recieved data {data}")
        if data.get('event') == 'roll_ask':
            # player asked to roll, let's do it
            sides = 6
            num_dice = data['num_dice']
            num_dice = min(100, num_dice)  # don't go crazy here

            roll = tuple(random.randint(1, sides) for _ in range(num_dice))
            # print(f"...rolled {roll}")

            # send the roll data on the channel_layer
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    'type': 'roll_broadcast',
                    'user_source': data['user_source'],  # TODO xss protect
                    'sides': sides,
                    'num_dice': num_dice,
                    'roll': roll,
                }
            )

    # Receive message from room group
    def roll_broadcast(self, event):
        " somebody just rolled, we need to send it to the client "

        # print(f"roll_broadcast({event})")

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'event': 'roll_broadcast',
            'user_source': event['user_source'],
            'sides': event['sides'],
            'num_dice': event['num_dice'],
            'roll': event['roll'],
        }))
