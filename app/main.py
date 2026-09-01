from pathlib import Path
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.db import Base, engine, get_db
from app.models import User, Chat, Testimonial
from app.security import verify_password, make_session, read_session
from app.social import collect_public_social_data
from app.ai import build_context, generate_testimonial, highest_similarity
from app.config import settings

Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Yearbook Testimonial Generator")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

def current_user(request: Request, db: Session):
    token = request.cookies.get("session")
    uid = read_session(token) if token else None
    return db.get(User, uid) if uid else None

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    users = db.query(User).order_by(User.full_name).all()
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"user": user, "users": users}
)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="login.html",
    context={}
    )

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email_id == email.strip().lower()).first()
    if not user or not verify_password(password, user.pass_hash):
        return RedirectResponse("/login?error=1", status_code=303)
    response = RedirectResponse("/", status_code=303)
    response.set_cookie("session", make_session(user.user_id), httponly=True, samesite="lax")
    return response

@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("session")
    return response

@app.get("/users/{user_id}", response_class=HTMLResponse)
def profile(user_id: int, request: Request, db: Session = Depends(get_db)):
    viewer = current_user(request, db)
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(404, "User not found")
    testimonials = db.query(Testimonial).filter(
        Testimonial.target_user_id == user_id
    ).order_by(Testimonial.created_at.desc()).all()
    authors = {t.testimonial_id: db.get(User, t.author_user_id) for t in testimonials}
    return templates.TemplateResponse(
    request=request,
    name="profile.html",
    context={
        "viewer": viewer,
        "target": target,
        "testimonials": testimonials,
        "authors": authors
    }
)

@app.post("/users/{target_id}/generate")
async def generate(target_id: int, request: Request, db: Session = Depends(get_db)):
    author = current_user(request, db)
    if not author:
        return RedirectResponse("/login", status_code=303)

    target = db.get(User, target_id)
    if not target:
        raise HTTPException(404, "Target user not found")
    if author.user_id == target.user_id:
        raise HTTPException(400, "Self-testimonials are disabled.")

    existing_by_author = db.query(Testimonial).filter(
        and_(
            Testimonial.author_user_id == author.user_id,
            Testimonial.target_user_id == target.user_id
        )
    ).first()
    if existing_by_author:
        return RedirectResponse(f"/users/{target_id}?already=1", status_code=303)

    chats = db.query(Chat).filter(
        or_(
            and_(Chat.user_1_from == target.user_id, Chat.user_2_to == author.user_id),
            and_(Chat.user_1_from == author.user_id, Chat.user_2_to == target.user_id),
        )
    ).order_by(Chat.id.desc()).limit(settings.MAX_CHAT_CONTEXT).all()

    social_data = await collect_public_social_data(target.social_id)
    existing = db.query(Testimonial).filter(Testimonial.target_user_id == target.user_id).all()
    existing_texts = [x.testimonial_text for x in existing]
    context = build_context(target, chats, social_data)

    candidate = None
    score = 1.0
    attempt = 0

    for attempt in range(1, settings.MAX_GENERATION_ATTEMPTS + 1):
        candidate = await generate_testimonial(context, author.full_name, existing_texts)
        score = highest_similarity(candidate, existing_texts)
        if score < settings.SIMILARITY_THRESHOLD:
            break

    if not candidate or score >= settings.SIMILARITY_THRESHOLD:
        return RedirectResponse(f"/users/{target_id}?generation_failed=1", status_code=303)

    db.add(Testimonial(
        author_user_id=author.user_id,
        target_user_id=target.user_id,
        testimonial_text=candidate,
        similarity_score=f"{score:.4f}",
        generation_attempt=attempt,
    ))
    db.commit()
    return RedirectResponse(f"/users/{target_id}?generated=1", status_code=303)

# ============================================
# ✅ MANUAL TESTIMONIAL ROUTE (CHANGE 3)
# ============================================
@app.post("/users/{target_id}/manual")
async def manual_testimonial(
    target_id: int,
    testimonial_text: str = Form(...),
    request: Request = None,
    db: Session = Depends(get_db)
):
    author = current_user(request, db)
    if not author:
        return RedirectResponse("/login", status_code=303)
    
    target = db.get(User, target_id)
    if not target:
        raise HTTPException(404, "User not found")
    
    if author.user_id == target.user_id:
        raise HTTPException(400, "Self-testimonials are disabled.")
    
    # Check if user already wrote a testimonial
    existing = db.query(Testimonial).filter(
        and_(
            Testimonial.author_user_id == author.user_id,
            Testimonial.target_user_id == target.user_id
        )
    ).first()
    
    if existing:
        return RedirectResponse(f"/users/{target_id}?already=1", status_code=303)
    
    # Manual testimonial - no AI, no similarity check
    db.add(Testimonial(
        author_user_id=author.user_id,
        target_user_id=target.user_id,
        testimonial_text=testimonial_text.strip(),
        similarity_score="manual",
        generation_attempt=1,
    ))
    db.commit()
    
    return RedirectResponse(f"/users/{target_id}?manual=1", status_code=303)
# ============================================

@app.get("/health")
def health():
    return {"status": "ok"}
#firstname.lastname@gmail.com


#open cmd then type following this 
# D:

#cd DTT\ai_yearbook_testimonial_project

#.venv\Scripts\activate.bat
# uvicorn app.main:app --reload