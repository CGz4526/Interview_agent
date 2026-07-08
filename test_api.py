import requests

BASE_URL = "http://localhost:8000"

def test_health():
    print("=== 测试健康检查 ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()
    return response.status_code == 200

def test_register():
    print("=== 测试用户注册 ===")
    data = {
        "username": "interviewer",
        "email": "test@test.com",
        "password": "12345678"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应: {response.json()}")
    except:
        print(f"响应: {response.text}")
    print()
    return response.status_code == 200

def test_login():
    print("=== 测试用户登录 ===")
    data = {
        "username": "interviewer",
        "password": "12345678"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", data=data)
    print(f"状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"响应: {result}")
        return result.get("access_token")
    except:
        print(f"响应: {response.text}")
    print()
    return None

def test_upload_questions(token):
    print("=== 测试上传面试题 ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "text": "面试官问了几个问题：1. Redis的持久化机制是什么？RDB和AOF有什么区别？2. 谈谈你项目中的秒杀系统是怎么设计的？如何解决高并发问题？3. Java中HashMap的实现原理是什么？为什么线程不安全？"
    }
    response = requests.post(f"{BASE_URL}/api/questions/upload", json=data, headers=headers)
    print(f"状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"响应: {result}")
        return result
    except:
        print(f"响应: {response.text}")
    print()
    return None

def test_create_project(token):
    print("=== 测试创建项目 ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "电商秒杀系统",
        "description": "基于Spring Boot开发的高并发秒杀系统，使用Redis做缓存，MySQL做主数据库，RabbitMQ做异步消息处理。支持百万级QPS，采用分布式锁防止超卖。",
        "tech_stack": ["java", "spring", "redis", "mysql", "rabbitmq"],
        "project_type": "seckill",
        "domain_tags": ["seckill", "ecommerce"]
    }
    response = requests.post(f"{BASE_URL}/api/projects/", json=data, headers=headers)
    print(f"状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"响应: {result}")
        return result.get("id")
    except:
        print(f"响应: {response.text}")
    print()
    return None

def test_generate_exam(token, project_id):
    print("=== 测试生成试卷 ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "mode": "project",
        "project_id": project_id,
        "count": 5
    }
    response = requests.post(f"{BASE_URL}/api/exams/generate", json=data, headers=headers)
    print(f"状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"响应: {result}")
        return result
    except:
        print(f"响应: {response.text}")
    print()
    return None

def test_start_review(token):
    print("=== 测试开始复习 ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "count": 5
    }
    response = requests.post(f"{BASE_URL}/api/review/start", json=data, headers=headers)
    print(f"状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"响应: {result}")
        return result
    except:
        print(f"响应: {response.text}")
    print()
    return None

def test_llm_generate_questions(token):
    print("=== 测试AI生成题目 ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/llm/generate-questions?topic=Redis&count=3", headers=headers)
    print(f"状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"响应: {result}")
        return result
    except:
        print(f"响应: {response.text}")
    print()
    return None

def test_llm_generate_answer(token, question_id):
    print("=== 测试AI生成答案 ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/llm/generate-answer/{question_id}", headers=headers)
    print(f"状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"响应: {result}")
        return result
    except:
        print(f"响应: {response.text}")
    print()
    return None

def test_llm_analyze_project(token, project_id):
    print("=== 测试AI分析项目 ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/llm/analyze-project/{project_id}", headers=headers)
    print(f"状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"响应: {result}")
        return result
    except:
        print(f"响应: {response.text}")
    print()
    return None

if __name__ == "__main__":
    print("=" * 50)
    print("GT_agent 后端API测试")
    print("=" * 50)
    print()
    
    test_health()
    test_register()
    token = test_login()
    
    if token:
        questions = test_upload_questions(token)
        project_id = test_create_project(token)
        
        if project_id:
            test_generate_exam(token, project_id)
        
        test_start_review(token)
        
        print("\n" + "=" * 50)
        print("LLM功能测试")
        print("=" * 50)
        llm_questions = test_llm_generate_questions(token)
        
        if llm_questions and len(llm_questions) > 0:
            test_llm_generate_answer(token, llm_questions[0]["id"])
        
        if project_id:
            test_llm_analyze_project(token, project_id)
    
    print("=" * 50)
    print("测试完成")
    print("=" * 50)