from database import init_database, create_user, verify_user

init_database()
print("Database initialized.")

success, msg = create_user("testuser", "testpass123")
print("Create user:", success, msg)

success, result = verify_user("testuser", "testpass123")
print("Login correct password:", success, result)

success, result = verify_user("testuser", "wrongpassword")
print("Login wrong password:", success, result)

success, msg = create_user("testuser", "anotherpass")
print("Duplicate username attempt:", success, msg)