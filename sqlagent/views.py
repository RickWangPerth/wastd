import openai
from django.http import JsonResponse
from langchain_community.utilities import SQLDatabase
from django.conf import settings
from sqlalchemy import create_engine

# 创建数据库连接URI
db_uri = f"mssql+pyodbc://{settings.DATABASES['wamtram2']['USER']}:{settings.DATABASES['wamtram2']['PASSWORD']}@{settings.DATABASES['wamtram2']['HOST']}:{settings.DATABASES['wamtram2']['PORT']}/{settings.DATABASES['wamtram2']['NAME']}?driver={settings.DATABASES['wamtram2']['OPTIONS']['driver']}"

# 实例化SQLDatabase
db = SQLDatabase.from_uri(db_uri)

# 定义视图函数
def query_database(request):
    # 测试数据库连通性
    try:
        # 尝试获取数据库中的表名来测试连通性
        table_names = db.get_usable_table_names()
        print(f"Connected to the database successfully. Available tables: {table_names}")
    except Exception as e:
        return JsonResponse({"error": "Database connection failed!", "details": str(e)}, status=500)
    
    # query = request.GET.get("query", "List turtles with more than 3 PIT tags.")
    
    # # 创建OpenAI API客户端
    # openai.api_key = settings.OPENAI_API_KEY

    # # 定义增强的消息提示
    # messages = [
    #     {"role": "system", "content": "You are a helpful assistant that generates SQL queries based on user requests."},
    #     {"role": "user", "content": query},
    #     {"role": "assistant", "content": "Generate an SQL query to find all turtles that have more than 3 PIT tags in the TRT_RECORDED_PIT_TAGS table."},
    #     {"role": "system", "content": "The TRT_RECORDED_PIT_TAGS table stores records of PIT tags with a TURTLE_ID column representing the turtle associated with each tag."}
    # ]

    # # 使用OpenAI API生成SQL查询
    # stream = openai.ChatCompletion.create(
    #     model="gpt-4o-mini",
    #     messages=messages,
    #     stream=True,
    # )

    # # 收集API返回的SQL查询
    # response_content = ""
    # for chunk in stream:
    #     if chunk.choices[0].delta.content is not None:
    #         response_content += chunk.choices[0].delta.content

    # # 输出生成的SQL查询以便调试
    # print(f"Generated SQL Query: {response_content}")

    # # 假设响应内容是生成的SQL查询，将其执行并返回结果
    # try:
    #     result = db.run(response_content)  # 使用LangChain的SQLDatabase直接运行查询
    # except Exception as e:
    #     return JsonResponse({"error": str(e)}, status=500)

    # return JsonResponse({"result": result})
