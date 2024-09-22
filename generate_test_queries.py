import random

def generate_normal_query():
    tables = ['users', 'products', 'orders', 'customers', 'employees']
    conditions = ['id', 'name', 'email', 'price', 'date', 'status']
    operators = ['=', '>', '<', '>=', '<=', 'LIKE', 'IN', 'BETWEEN']
    
    table = random.choice(tables)
    condition = random.choice(conditions)
    operator = random.choice(operators)
    
    if operator in ['=', '>', '<', '>=', '<=']:
        value = random.randint(1, 1000)
        return f"SELECT * FROM {table} WHERE {condition} {operator} {value}"
    elif operator == 'LIKE':
        return f"SELECT * FROM {table} WHERE {condition} LIKE '%{random.choice(['a','b','c','d','e'])}%'"
    elif operator == 'IN':
        values = ', '.join([str(random.randint(1, 10)) for _ in range(3)])
        return f"SELECT * FROM {table} WHERE {condition} IN ({values})"
    else:  # BETWEEN
        val1, val2 = sorted([random.randint(1, 1000), random.randint(1, 1000)])
        return f"SELECT * FROM {table} WHERE {condition} BETWEEN {val1} AND {val2}"

def generate_injection_query():
    base_queries = [
        "SELECT * FROM users WHERE username = 'admin' OR 1=1--",
        "SELECT * FROM users WHERE username = '' UNION SELECT * FROM credit_cards--",
        "'; DROP TABLE users;--",
        "' OR '1'='1",
        "admin' --",
        "1; UPDATE users SET password='hacked' WHERE username='admin'--",
        "1 UNION SELECT null, username, password FROM users--",
        "1; INSERT INTO users (username, password) VALUES ('hacker', 'password')--",
        "' OR username LIKE '%admin%",
        "' AND 1=0 UNION SELECT username, password FROM users--"
    ]
    return random.choice(base_queries)

# Tạo file với 1000 truy vấn
with open('test_queries.sql', 'w') as f:
    for _ in range(1000):
        if random.random() < 0.8:  # 80% truy vấn bình thường
            query = generate_normal_query()
        else:  # 20% truy vấn có khả năng là SQL injection
            query = generate_injection_query()
        f.write(query + '\n')

print("File test_queries.sql đã được tạo với 1000 truy vấn.")