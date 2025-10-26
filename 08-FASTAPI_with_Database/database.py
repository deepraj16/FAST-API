

# import psycopg2 
# from psycopg2.extras import RealDictCursor 

# try : 
#     conn = psycopg2.connect(host='localhost',database='fastapi',user="postgres",password="root",port="5432", #second ="5433"
#                                 cursor_factory=RealDictCursor)
#     cursor = conn.cursor()

# except Exception as e : 
#     print(f"Error : {e}") 

# cursor.execute("Select * from posts")
# posts =cursor.fetchall()
# #print(posts)
# print(type(posts[0]))
# print()

# for i in posts : 
#     print(i["title"])  

data=[1,2,3,5,6,7,23]

def get_data_from_id(id :int,post:list =data) ->bool : 
    for i in post : 
        if i == id : 
            return True 
    return False

post= [23,34,45,66]
print(get_data_from_id(23))   
