from fastapi import APIRouter, Depends, HTTPException, status, Response
from server.schemas import postschema, interactionschema
from server.models import postmodel, interactionmodel, usermodel
from sqlalchemy.orm import Session
from server.crud import create, delete
from server.utils import auth
from server.common import get_db


route = APIRouter(prefix='/Post', tags=['Post'])


@route.post('/CreatePost', status_code=status.HTTP_201_CREATED)
def create_post(post: postschema.CreatePost, db:Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    try:
        new_post = postmodel.Post(
                                title = post.title,
                                content = post.content, 
                                uid = current_user.id
                                )
        create(new_post, db)
        return {"Message": "Post Created"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@route.get('/ViewPosts')
def get_posts(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

    try:
        posts = db.query(postmodel.Post).filter(postmodel.Post.uid == current_user.id).all()
        return {"posts": posts}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@route.get('/Feed', response_model=postschema.ViewPosts)
def get_posts(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

    try:
        posts = db.query(postmodel.Post).filter().all()
        post_list = []
        for post in posts:
            user = db.query(usermodel.User).filter(usermodel.User.id == post.uid).first()
            username = user.username if user else None 
            comments = db.query(interactionmodel.Comment).filter(interactionmodel.Comment.pid == post.id).all()
            comment_list = []
            for comment in comments:
                comment_user = db.query(usermodel.User).filter(usermodel.User.id == comment.uid).first()
                comment_username = comment_user.username if comment_user else None
                comment_list.append({
                    "comment": comment.comm,
                    "username": comment_username
                })
            post_dict = {
                "title": post.title,
                "content": post.content,
                "like_cnt": post.like_cnt,
                "username": username, 
                "comment_cnt": post.comment_cnt,
                "comments": comment_list
            }
            post_list.append(post_dict)

        return {"posts": post_list}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@route.put('/UpdatePost')
def update_post(post: postschema.UpdatePost, db:Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

    try:
        updatepost = db.query(postmodel.Post).filter(postmodel.Post.id == post.pid, postmodel.Post.uid == current_user.id).first()
        if not updatepost:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        updatepost.title = post.title
        updatepost.content = post.content
        db.commit()
        return {"Message": "Post Updated"}
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@route.delete('/DeletePost', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post: postschema.DeletePost, db:Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    try:
        ext_post = db.query(postmodel.Post).filter(postmodel.Post.id == post.pid, postmodel.Post.uid == current_user.id).first()
        if not ext_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        delete(ext_post, db)
        return {"Message" : "Post Deleted"}
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

