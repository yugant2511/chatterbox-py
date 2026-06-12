from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from connection_manager import ConnectionManager

router = APIRouter(tags=["chat"])
manager = ConnectionManager()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}", room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast("A user left the chat", room_id)