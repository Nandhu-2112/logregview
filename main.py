from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class RegisterItem(BaseModel):
    name: str
    phno: str
    email: str
    password: str
@app.post("/register")
def register(i: RegisterItem):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="office",
        port=3309
    )
    mypost = mydb.cursor()
    mypost.execute(
        "INSERT INTO usersdb (name, phno, email, password) VALUES ('" +
        i.name + "', '" + i.phno + "', '" + i.email + "', '" + i.password + "')"
    )
    mydb.commit()
    mydb.close()
    return {"message": "Registered successfully"}

class LoginItem(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(i: LoginItem):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="office",
        port=3309
    )
    mypost = mydb.cursor()
    mypost.execute(
        "SELECT * FROM usersdb WHERE email='" + i.email + "' AND password='" + i.password + "'"
    )
    result = mypost.fetchone()
    mydb.close()
    if result:
        return {"message": "Success"}
    else:
        return {"message": "Invalid"}

@app.get("/table")
def view():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="office",
        port=3309
    )
    mypost = mydb.cursor(dictionary=True)
    mypost.execute("SELECT * FROM usersdb")
    result = mypost.fetchall()
    mydb.close()
    return result
class UpdateItem(BaseModel):
    name: str

@app.put("/update/{user_id}")
def update(i: UpdateItem, user_id: int):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="office",
        port=3309
    )
    mypost = mydb.cursor()
    mypost.execute(
        "UPDATE usersdb SET name='" + i.name + "' WHERE id=" + str(user_id)
    )
    mydb.commit()
    mydb.close()
    return {"message": "Updated"}

@app.delete("/del/{user_id}")
def delete(user_id: int):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="office",
        port=3309
    )
    mypost = mydb.cursor()
    mypost.execute("DELETE FROM usersdb WHERE id=" + str(user_id))
    mydb.commit()
    mydb.close()
    return {"message": "Deleted succesfully"}

