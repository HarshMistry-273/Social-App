from fastapi import APIRouter, Depends, HTTPException, status
from server.schemas import interactionschema
from server.models import interactionmodel, postmodel
from sqlalchemy.orm import Session
from server.crud import create, delete
from server.utils import auth
from server.common import get_db


route = APIRouter(prefix='/Interaction', tags=['Interaction'])


@route.post('/AddORRemoveLike')
def Like(like: interactionschema.CreateLike, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

    try:
        ext_like = db.query(interactionmodel.Like).filter(interactionmodel.Like.pid == like.pid, interactionmodel.Like.uid == current_user.id).first()
        if ext_like:
            db.query(interactionmodel.Like).filter(interactionmodel.Like.pid == like.pid, interactionmodel.Like.uid == current_user.id).delete(synchronize_session=False)
            post = db.query(postmodel.Post).filter(postmodel.Post.id == like.pid).first()
            post.like_cnt -= 1
            db.commit()
            return {"Message": "Like Removed"}

        new_like = interactionmodel.Like(pid = like.pid, uid=current_user.id)
        getpost = db.query(postmodel.Post).filter(postmodel.Post.id == like.pid).first()
        getpost.like_cnt += 1
        db.commit()
        create(new_like, db)
        return {"Message": "Like Added"} 
    
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@route.post('/AddComment')
def Comment(comment: interactionschema.CreateComment, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

    try:
        new_comment = interactionmodel.Comment(pid = comment.pid, comm = comment.comm, uid=current_user.id)
        post = db.query(postmodel.Post).filter(postmodel.Post.id == comment.pid).first()
        post.comment_cnt += 1
        db.commit()
        create(new_comment, db)
        return {"Message": "Comment Added"} 

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@route.put('/UpdateComment')
def alter_comment(cmt: interactionschema.UpdateComment, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

    try:
        comment = db.query(interactionmodel.Comment).filter(interactionmodel.Comment.id == cmt.cid).first()
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

        if comment.uid != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are allowed not to alter  this comment")

        comment.comm = cmt.comm
        db.commit()

        return {"Message": "Comment changed successfully"}

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@route.delete('/DeleteComment', status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: str, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):

    try:
        comment = db.query(interactionmodel.Comment).filter(interactionmodel.Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

        if comment.uid != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this comment")

        post = db.query(postmodel.Post).filter(postmodel.Post.id == comment.pid).first()
        if post and post.comment_cnt > 0:
            post.comment_cnt -= 1
            db.commit()

        delete(comment, db)
        return {"Message": "Comment deleted successfully"}
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))