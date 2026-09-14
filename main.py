from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import auth
import llm
import models
import report
import schemas

from database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Notes Summarizer API",
    description="Save notes and generate AI summaries.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Notes Summarizer API is running"
    }


@app.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.User(
        email=user.email,
        hashed_password=auth.hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


@app.post("/login")
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not auth.verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = auth.create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/notes", response_model=schemas.NoteResponse)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    new_note = models.Note(
        title=note.title,
        content=note.content
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@app.get("/notes", response_model=list[schemas.NoteResponse])
def get_notes(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    return db.query(models.Note).all()


@app.post("/notes/{note_id}/summarize")
def summarize_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    note = db.query(models.Note).filter(
        models.Note.id == note_id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    try:
        summary = llm.summarize_note(note.content)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"AI summarization failed: {str(error)}"
        )

    note.summary = summary

    db.commit()
    db.refresh(note)

    return {
        "id": note.id,
        "title": note.title,
        "summary": note.summary
    }


@app.get("/report")
def generate_report(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    notes = db.query(models.Note).all()

    if not notes:
        raise HTTPException(
            status_code=404,
            detail="No notes found"
        )

    filename = report.create_notes_report(notes)

    return FileResponse(
        path=filename,
        media_type="application/pdf",
        filename="AI_Notes_Report.pdf"
    )