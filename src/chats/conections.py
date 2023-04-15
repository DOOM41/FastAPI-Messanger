from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections_by_chat_id: dict[int:list] = {}

    async def connect(self, websocket: WebSocket, chat_id):
        await websocket.accept()
        try:
            self.active_connections_by_chat_id[chat_id].append(websocket)
        except:
            self.active_connections_by_chat_id[chat_id] = [websocket]

    def disconnect(self, websocket: WebSocket, chat_id):
        self.active_connections_by_chat_id[chat_id].remove(websocket)
        
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_message_by_chats(self, data, chat_id):
        if self.active_connections_by_chat_id[chat_id]:
            for web in self.active_connections_by_chat_id[chat_id]:
                await web.send_json(data)


manager = ConnectionManager()
