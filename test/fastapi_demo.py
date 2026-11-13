import uvicorn
from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

# 访问 http://127.0.0.1:8000/items/5?q=somequery
# item_id: 路径参数 (自动转为 int)
# q: 查询参数 (可选，默认 None)
@app.get("/item/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# 接收? skip=? & limit = ?
@app.get("/item/")
def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# 使用 Header 和 Cookie 类型注解获取请求头和 Cookie 数据。
# POST 请求接收 JSON 数据
# 展示如何定义数据结构，FastAPI 会自动进行类型检查和错误提示。
from pydantic import BaseModel

# 定义数据模型
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.post("/items/")
def create_item(item: Item):
    # item 已经是验证过的 Item 对象
    # 如果客户端传来的 price 是字符串 "abc"，FastAPI 会自动报错
    return {"item_name": item.name, "item_price": item.price}

from fastapi import Header, Cookie
from fastapi import FastAPI


@app.get("/items/")
def read_item(user_agent: str = Header(None), session_token: str = Cookie(None)):
    return {"User-Agent": user_agent, "Session-Token": session_token}

# 路由处理函数返回一个 Pydantic 模型实例，FastAPI 将自动将其转换为 JSON 格式，并作为响应发送给客户端：
@app.post("/items/return")
def create_item(item: Item):
    return item

#使用 RedirectResponse 实现重定向，将客户端重定向到 /items/ 路由。
from fastapi.responses import RedirectResponse

@app.get("/redirect")
def redirect():
    return RedirectResponse(url="/items/")

#使用 HTTPException 抛出异常，返回自定义的状态码和详细信息。
#以下实例在 item_id 为 42 会返回 404 状态码：
from fastapi import HTTPException
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 42:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}

from fastapi.responses import FileResponse

@app.get("/download/excel")
def download_excel():
    excel_path = "./data/report.xlsx"
    # 返回文件并指定下载文件名
    return FileResponse(
        path=excel_path,
        filename="月度报表.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

from fastapi.responses import HTMLResponse
@app.get("/hello")
def hello(name: str = "游客"):
    html_content = f"""
    <html>
        <body>
            <h1>你好，{name}！</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

from fastapi.responses import PlainTextResponse

@app.get("/text")
def get_text():
    return PlainTextResponse(content="这是纯文本响应", status_code=200)

@app.get("/old-path")
def redirect_old_path():
    # 重定向到 /new-path，状态码 307 表示临时重定向
    return RedirectResponse(url="/new-path", status_code=307)

@app.get("/new-path")
def new_path():
    return {"message": "这是新接口"}

from fastapi.responses import StreamingResponse
import asyncio

async def generate_stream():
    # 模拟流式输出（逐字返回）
    words = ["你", "好", "，", "这", "是", "流", "式", "响", "应"]
    for word in words:
        await asyncio.sleep(0.5)
        yield word.encode("utf-8")  # 流式输出需返回字节流

@app.get("/stream")
async def stream_response():
    return StreamingResponse(generate_stream(), media_type="text/plain")


# 文件上传模块

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)