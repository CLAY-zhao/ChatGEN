import openai


openai.api_key = ""
openai.api_base = "http://127.0.0.1:9000/v1"

completion = openai.ChatCompletion.create(
  model="default-model",
  temperature=0.5,
  top_p=0.75,
  messages=[
    {
      "role": "user",
      "content": "你能写一篇关于环保的论文吗，不用这么长"
    }
  ]
)

respond = completion.choices

print(respond)
