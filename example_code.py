"""
Example code with common issues for code review practice
"""
import time
import os
import sqlite3
from flask import Flask, request

# Global variable
PASSWORD = "admin123"  # Security issue: Hardcoded password

app = Flask(__name__)

# Inefficient function with O(n²) time complexity
def find_duplicates(input_list):
    duplicates = []
    for i in range(len(input_list)):
        for j in range(i + 1, len(input_list)):
            if input_list[i] == input_list[j] and input_list[i] not in duplicates:
                duplicates.append(input_list[i])
    return duplicates

# Security issue: SQL Injection vulnerability
@app.route('/users')
def get_user():
    username = request.args.get('username')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return str(result)

# Performance issue: inefficient resource usage
def process_data(data):
    # Unnecessarily creating a new list for each operation
    data = [item for item in data]  # Unnecessary list comprehension
    data = [item.strip() for item in data]
    data = [item.lower() for item in data]
    data = [item for item in data if item]  # Could be combined with the above
    
    # Commented out code
    # old_process_method()
    # print("Debug statement")
    
    return data

# Poor error handling
def divide_numbers(a, b):
    try:
        return a / b
    except:  # Too broad exception handling
        return None  # Silent failure, no logging

if __name__ == "__main__":
    app.run(debug=True)  # Security issue: Debug mode in production