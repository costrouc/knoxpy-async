import aiohttp
from aiohttp import web


async def index(request):
    name = request.match_info.get('name', Anonymous)
    return web.Response(text="Hello %s from aiohttp server" % name)


async def index_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.MsgType.text:
            print('Recieved:', msg.data)
            ws.send_str("Server Echo, {}".format(msg.data))
        elif msg.type == web.MsgType.binary:
            ws.send_bytes(msg.data)
        elif msg.type == web.MsgType.close:
            break

    return ws


def setup_routes(app, root=""):
    app.router.add_get('/ws', index_websocket)
    app.router.add_static('/static', 'static')
    app.router.add_get('/{name}', index)


def init_app():
    app = web.Application()
    setup_routes(app)
    return app


if __name__ == "__main__":
    app = init_app()
    web.run_app(app, host='localhost', port=8080)
