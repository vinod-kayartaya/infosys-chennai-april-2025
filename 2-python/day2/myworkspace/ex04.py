username = input('Enter your username: ')
password = input('Enter your password: ')

sql = f"select * from users where username='{username}' and password='{password}'"

print(sql)