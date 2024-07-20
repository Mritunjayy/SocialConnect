from .. import models,  schemas, oauth2
from fastapi import FastAPI, Response, status,HTTPException, Depends, APIRouter
from ..database import get_db
from  sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import  List
from typing import Optional



router =APIRouter(
    prefix= "/posts" ,## + /id (?posts/id--> for the path operator route)
    tags=['Posts']
)



##test route for sqlalchemy
# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     # posts = db.query(models.Post)##same as----->SELECT * FROM posts
#     # print(posts)
#     return {"data":posts}
#     # return {"status":"success for now"}

my_posts= [{"title": "title of post 1","content": "content of post 1", "id":1},{"title":"favourite foods","content":"i like pizza","id":2}]


@router.get("/", response_model= List[schemas.PostOut])
# @router.get("/")
##we are getting here all the posts from every user, but what if its any kind of note-making app, then u want that every user should see only their own post....---->>return posts of user that is logged in, thats it..
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]= ""):
    # print(limit)
    # cursor.execute("""SELECT * FROM posts """)
    # posts= cursor.fetchall()
    ##-------------
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    ##trying sql joins using sqlalchemy
    # posts = db.query(models.Post)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() ##sqlalchemy default: LEFT INNER JOIN
    # print(results)

   
    # print(posts)
    # return {"post" : posts}
    return  posts


@router.get("/latest", response_model=schemas.PostResponse)## this gives us an error of path parameter, but we have not used any path parameter, this is because the route with /posts/{id} also can be matchable to this, i.e latest can also act as an id for that route: so to fix the issue we just move this up in the order, and it solves it
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    # return {"detail": post}
    return post


@router.get("/{id}", response_model= schemas.PostOut)#id here represents path parameter
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(type(id))

    # cursor.execute("""select * from posts where id = %s""",(str(id)))
    # test_post= cursor.fetchone()
    # print(test_post)
    # post= find_post(id)

    ## using orm sqlalchemy
    # post = db.query(models.Post).filter(models.Post.id == id).first()## all() will look after all post, but we know that one id can be assigned to one post only so it is a waste of time and resources
    # print(post)

    post = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first() 

    if not post:
        # response.status_code= 404
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}##<4> this is an built in exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!!!!")
    # if post.owner_id != current_user.id:
    #     # print("not a valid user bro!!")
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "not authorised user to delete")
    # return {"post_detail":f"here is the post {id}"}
    # print(post)
    # return {"post_detail":post}
    return post

# @app.get("/posts/first_post")
# def first_post():
#     return {"post_1" : "this is my 1st post of post 1"}

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"text":f"title: {payload['title']}, content: {payload['content']}"}

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(post.rating)
    # print(post)
    # print(post.model_dump())

    # return {"data": "new post"}
    # post_dict=post.model_dump()
    # post_dict['id']=randrange(0,10000000)
    # my_posts.append(post_dict)# we solve the issue by creating the id;so we create a random integer from random library

    ##for postgres from here using sql query hardcode
    # cursor.execute("""Insert into posts(title, content, published) values(%s, %s, %s) returning * """,(post.title, post.content, post.published))
    # new_post= cursor.fetchone()
    # conn.commit()

    ##using ORM sqlalchemy

    # print(post.model_dump())
    # new_post = models.Post(title= post.title, content= post.content, published= post.published)

    # print(get_current_user.id)
    # print(get_current_user.email)
    new_post= models.Post(owner_id= current_user.id, **post.model_dump())## unpacking the dictionary with (**)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # return {"data": new_post}
    return new_post

# 1> now we use pydantic lib rary to create schema
#title:str, content:str

#2> now want user to define a property, whether a post be published or not

##4> now we do not get any error ,instead we get null when any other path parameter is passed instead of the stored ones so we add a library Response

##5> delete a post

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id']== id:
            return i



##so right nnow any user which is logged in can delete his or any other user's post , but that dosen't work like that , so we build a logic of if/else to check if the person logged in trying to delete a post that is his or not, and if it is not the case, then we r returning an error...
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""delete from posts where id= %s returning * """,(str(id)))
    # deleted_post= cursor.fetchone()
    # conn.commit()


    ## deleting using orm sqlalchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # print(post_query)
    # print("##################")
    # deleting: basically for deleting a post we just delete that specified post from the array, which ID is asked, and then we remove it from the array.
    # index = find_post_index(id)

    post = post_query.first()
    print(post)
    if post == None:
    # if index==None:
        # print(post)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id; {id} does not exists") 
    if post.owner_id != current_user.id:
        # print("not a valid user bro!!")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "not authorised user to delete")
    post_query.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(index)
    # return {"message": "post was successfully deleted"}
    # print("do something yrrr please!!!!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#6> update post
@router.put("/{id}", response_model= schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(post)
    # cursor.execute("""update posts set title = %s, content = %s, published= %s where id = %s returning * """,(post.title, post.content, post.published, str(id)))
    # updated_post= cursor.fetchone()
    # conn.commit()
    # index = find_post_index(id)

    ##using orm sqlalchemy
    post_query= db.query(models.Post).filter(models.Post.id == id)
    # print(post_query)
    post_updated = post_query.first()

    if post_updated == None:
    # if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id; {id} does not exists") 
    if post_updated.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "not authorised user to update ....")
    # post_dict= post.model_dump()
    # post_dict['id']= id
    # my_posts[index]= post_dict

    # updated_post_query.update({'title':"this is updated title", 'content':'this updated content'},synchronize_session=False)
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"data": post_updated}