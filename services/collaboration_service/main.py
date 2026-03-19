from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict

app = FastAPI(title="Radiology Collaboration Service")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, study_id: str, websocket: WebSocket):
        await websocket.accept()
        if study_id not in self.active_connections:
            self.active_connections[study_id] = []
        self.active_connections[study_id].append(websocket)

    def disconnect(self, study_id: str, websocket: WebSocket):
        self.active_connections[study_id].remove(websocket)

    async def broadcast(self, study_id: str, message: dict):
        for connection in self.active_connections.get(study_id, []):
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{study_id}")
async def websocket_endpoint(websocket: WebSocket, study_id: str):
    await manager.connect(study_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Broadcast camera position, window/level, etc.
            await manager.broadcast(study_id, data)
    except WebSocketDisconnect:
        manager.disconnect(study_id, websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
