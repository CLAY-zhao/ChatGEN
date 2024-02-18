# 指定本地llm模型
set_path:
	set MODEL=chatglm3-ggml.bin

openapi_serve:
	uvicorn chatglm_cpp.openai_api:app --host 127.0.0.1 --port 9000

install:
	pip install -r requirements.txt
