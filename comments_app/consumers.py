import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'comments_group'
        # user con
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # user discon
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # event to all connected users
    async def new_comment(self, event):
        message = event['message']
        comment_id = event.get('comment_id')

        await self.send(text_data=json.dumps({
            'type': 'new_comment',
            'message': message,
            'comment_id': comment_id
        }))