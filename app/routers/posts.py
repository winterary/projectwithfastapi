from multiprocessing import synchronize
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from .. import models, schemas, oauth2
from ..database import  get_db
from typing import List, Optional

router = APIRouter(
    prefix = "/posts",
    tags = ["posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user : int = 
                 Depends(oauth2.get_current_user),limit : int = 10, skip : int = 0, search : Optional[str] = "" ):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # post = db.execute(select(models.Post).where(models.Post.title.contains(search)).limit(limit).offset(skip)).scalars().all()

    
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
    #     models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).all()
    # print(results)

    posts = db.execute(
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id).where(
        models.Post.title.contains(search)
        ).limit(limit)
        .offset(skip)
        ).all()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    return posts
    

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = 
                 Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """, 
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,db:Session = Depends(get_db), current_user : int = 
                 Depends(oauth2.get_current_user)):

    # cursor.execute(""" SELECT * FROM posts WHERE ID = %s  """, (id,)) 
    # post = cursor.fetchone()

    posts = db.get(models.Post, id)

    post = db.execute(
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id).where(models.Post.id == id)).first()
    

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    return (post)

@router.delete("/{id}")
def delete_post(id: int, db:Session = Depends(get_db), current_user : int = 
                 Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.get(models.Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id : {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 
                            " Not authorized to perform requested action")

    
    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int =
                 Depends(oauth2.get_current_user), ):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, (id)))  
    # updated_post = cursor.fetchone()   

    # conn.commit()   
    post = db.get(models.Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,         
                            detail = f"post with id : {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = 
                            " Not authorized to perform requested action")

    
    updated_data = updated_post.model_dump()
    for key, value in updated_data.items():
        setattr(post,key,value)
    db.commit()
    db.refresh(post)
     
    return post


   


