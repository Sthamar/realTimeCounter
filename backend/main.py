from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.counter = 0
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    async def disconnect(self, websocket:WebSocket):
        self.active_connections.remove(websocket)
        
    async def broadcast(self, message:str):
        for connection in self.active_connections:
            await connection.send_text(message)
            
manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            manager.counter += 1
            await manager.broadcast(f"counter updated: {manager.counter}")
    except WebSocketDisconnect:
         await manager.disconnect(websocket)        
        