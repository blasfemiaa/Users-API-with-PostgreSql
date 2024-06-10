from fastapi import FastAPI
from pydantic import BaseModel
from config import config
import psycopg2

app = FastAPI()

params = config()
conn = psycopg2.connect(**params)

class User(BaseModel):
    name : str
    surname : str
    age : int
    email : str
    country : str
    
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users_1 WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user is None:
        return {"error": "User not found"}
    else:
        return {"name": user[1], "surname": user[2], "age": user[3], "email": user[4], "country": user[5]}

@app.post("/users/create/")
async def create_user(user: User):
    cur = conn.cursor()
    cur.execute("INSERT INTO users_1 (name, surname, age, email, country) VALUES (%s, %s, %s, %s, %s) returning user_id", (user.name, user.surname, user.age, user.email, user.country))
    new_user = cur.fetchone()[0]
    conn.commit()
    cur.close()
    if new_user is None:
        return {"user not created, review your data"}
    else:
        return { new_user, "user created successfully"}
    
@app.put("/users/update/{user_id}")
async def update_user(user_id: int, user: User):
    cur = conn.cursor()
    cur.execute("UPDATE users_1 SET name = %s, surname = %s, age = %s, email = %s, country = %s where user_id = %s", (user.name, user.surname, user.age, user.email, user.country, user_id))
    conn.commit()
    cur.close()
    return { user_id ,"user updated successfully"}

@app.delete("/users/delete/{user_id}")
async def delete_user(user_id: int):
    cur = conn.cursor()
    cur.execute("DELETE FROM users_1 WHERE user_id = %s", (user_id,))
    conn.commit()
    cur.close()
    return {"user has been deleted", user_id}
    
