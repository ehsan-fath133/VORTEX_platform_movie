from flask import Flask, request, jsonify, send_from_directory, session
from pathlib import Path
import json, uuid, re, hashlib, secrets

BASE=Path(__file__).resolve().parent
DATA=BASE/"data"
MOVIES=DATA/"movies"; POSTERS=DATA/"posters"; SUBTITLES=DATA/"subtitles"
DB=DATA/"movies.json"; USERS=DATA/"users.json"; COMMENTS=DATA/"comments.json"; RATINGS=DATA/"ratings.json"
for p in (MOVIES,POSTERS,SUBTITLES): p.mkdir(parents=True,exist_ok=True)
for f in (DB,USERS,COMMENTS,RATINGS):
    if not f.exists(): f.write_text("[]",encoding="utf-8")

app=Flask(__name__,static_folder="static")
app.secret_key="NOVAFLIX_LOCAL_SECRET_CHANGE_ME"
app.config["MAX_CONTENT_LENGTH"]=50*1024*1024*1024

# فقط این حساب اجازه مدیریت دارد. ایمیل واقعی خودت را اینجا قرار بده.
OWNER_EMAIL="fathabadiehsan92@gmail.com"

def read(p):
    try:return json.loads(p.read_text(encoding="utf-8"))
    except:return []
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding="utf-8")
def hp(x): return hashlib.sha256(x.encode()).hexdigest()
def safe(x): return re.sub(r"[^A-Za-z0-9._-]+","_",Path(x or "file").name) or "file"
def user():
    uid=session.get("uid")
    return next((u for u in read(USERS) if u["id"]==uid),None)
def owner():
    u=user()
    return bool(u and u.get("email","").lower()==OWNER_EMAIL.lower())


@app.errorhandler(413)
def too_large(e): return jsonify(ok=False,error="فایل خیلی بزرگ است. محدودیت 50GB است."),413
@app.errorhandler(Exception)
def api_error(e):
    if request.path.startswith("/api/"): return jsonify(ok=False,error=str(e)),500
    return "Server error: "+str(e),500

@app.get("/")
def home(): return send_from_directory(app.static_folder,"index.html")
@app.get("/watch.html")
def watch(): return send_from_directory(app.static_folder,"watch.html")
@app.get("/admin.html")
def admin():
    if not owner():
        return "Not Found", 404
    return send_from_directory(app.static_folder, "admin.html")


@app.get("/api/me")
def me():
    u=user()
    if not u:return jsonify(logged_in=False)
    return jsonify(logged_in=True,user={"id":u["id"],"name":u["name"],"email":u["email"],"verified":u.get("verified",False),"admin":owner()})

@app.post("/api/register")
def register():
    d=request.get_json(silent=True) or {}
    name=d.get("name","").strip(); email=d.get("email","").strip().lower(); password=d.get("password","")
    if not name or not email or len(password)<6:return jsonify(ok=False,error="نام، ایمیل و رمز حداقل ۶ کاراکتری لازم است."),400
    users=read(USERS)
    if any(u["email"].lower()==email for u in users):return jsonify(ok=False,error="این ایمیل قبلاً ثبت شده است."),409
    u={"id":uuid.uuid4().hex,"name":name,"email":email,"password":hp(password),"verified":email==OWNER_EMAIL.lower()}
    users.append(u);write(USERS,users);session["uid"]=u["id"]
    return jsonify(ok=True,user={"name":name,"email":email,"verified":u["verified"],"admin":u["verified"] and owner()})

@app.post("/api/login")
def login():
    d=request.get_json(silent=True) or {}; email=d.get("email","").strip().lower(); password=d.get("password","")
    u=next((x for x in read(USERS) if x["email"].lower()==email and x["password"]==hp(password)),None)
    if not u:return jsonify(ok=False,error="ایمیل یا رمز عبور اشتباه است."),401
    session["uid"]=u["id"]
    return jsonify(ok=True,user={"name":u["name"],"email":u["email"],"verified":u.get("verified",False),"admin":owner()})

@app.post("/api/logout")
def logout(): session.clear(); return jsonify(ok=True)

@app.get("/api/movies")
def movies():
    ms=read(DB); comments=read(COMMENTS); ratings=read(RATINGS)
    for m in ms:
        rs=[r["score"] for r in ratings if r["movie_id"]==m["id"]]
        m["rating"]=round(sum(rs)/len(rs),1) if rs else 0
        m["likes"]=len([r for r in ratings if r["movie_id"]==m["id"] and r["score"]>=4])
        m["comments"]=len([c for c in comments if c["movie_id"]==m["id"]])
    return jsonify(ms)

@app.post("/api/movies")
def add_movie():
    if not owner(): return jsonify(ok=False,error="فقط صاحب حساب اجازه افزودن فیلم دارد."),403
    name=request.form.get("name","").strip(); desc=request.form.get("description","").strip()
    category=request.form.get("category","سایر").strip() or "سایر"
    creator=request.form.get("creator","").strip() or "NOVAFLIX"
    poster=request.files.get("poster"); video=request.files.get("video"); sub=request.files.get("subtitle")
    if not name or not poster or not video:return jsonify(ok=False,error="نام، پوستر و فیلم الزامی است."),400
    mid=uuid.uuid4().hex; pn=mid+"_"+safe(poster.filename); vn=mid+"_"+safe(video.filename)
    poster.save(POSTERS/pn);video.save(MOVIES/vn)
    su=None
    if sub and sub.filename:
        sn=mid+"_"+safe(sub.filename);sub.save(SUBTITLES/sn);su="/media/subtitles/"+sn
    m={"id":mid,"name":name,"description":desc,"category":category,"creator":creator,
       "poster":"/media/posters/"+pn,"video":"/media/movies/"+vn,"subtitle":su}
    ms=read(DB);ms.append(m);write(DB,ms);return jsonify(ok=True,movie=m),201

@app.delete("/api/movies/<mid>")
def delete_movie(mid):
    if not owner(): return jsonify(ok=False,error="دسترسی غیرمجاز."),403
    ms=read(DB);m=next((x for x in ms if x["id"]==mid),None)
    if not m:return jsonify(ok=False,error="فیلم پیدا نشد."),404
    for url in (m.get("poster"),m.get("video"),m.get("subtitle")):
        if url and url.startswith("/media/"):
            a=url[7:].split("/",1)
            if len(a)==2:(DATA/a[0]/a[1]).unlink(missing_ok=True)
    write(DB,[x for x in ms if x["id"]!=mid]);write(COMMENTS,[c for c in read(COMMENTS) if c["movie_id"]!=mid]);write(RATINGS,[r for r in read(RATINGS) if r["movie_id"]!=mid])
    return jsonify(ok=True)

@app.post("/api/movies/<mid>/rating")
def rating(mid):
    u=user()
    if not u:return jsonify(ok=False,error="برای ثبت نمره وارد حساب شو."),401
    score=int((request.get_json(silent=True) or {}).get("score",0))
    if score<1 or score>5:return jsonify(ok=False,error="نمره باید بین ۱ تا ۵ باشد."),400
    ms=read(DB)
    if not any(m["id"]==mid for m in ms):return jsonify(ok=False,error="فیلم پیدا نشد."),404
    rs=[r for r in read(RATINGS) if not(r["movie_id"]==mid and r["user_id"]==u["id"])]
    rs.append({"movie_id":mid,"user_id":u["id"],"score":score});write(RATINGS,rs)
    return jsonify(ok=True)

@app.get("/api/movies/<mid>/comments")
def get_comments(mid):
    users=read(USERS); out=[]
    for c in read(COMMENTS):
        if c["movie_id"]==mid:
            u=next((x for x in users if x["id"]==c["user_id"]),None)
            out.append({**c,"name":u["name"] if u else "کاربر","verified":bool(u and u.get("verified"))})
    return jsonify(out)

@app.post("/api/movies/<mid>/comments")
def add_comment(mid):
    u=user()
    if not u:return jsonify(ok=False,error="برای نظر دادن وارد حساب شو."),401
    text=(request.get_json(silent=True) or {}).get("text","").strip()
    if not text or len(text)>1000:return jsonify(ok=False,error="نظر خالی یا خیلی طولانی است."),400
    cs=read(COMMENTS);cs.append({"id":uuid.uuid4().hex,"movie_id":mid,"user_id":u["id"],"text":text});write(COMMENTS,cs)
    return jsonify(ok=True)

@app.get("/media/<folder>/<filename>")
def media(folder,filename):
    if folder not in ("movies","posters","subtitles"):return "Not found",404
    return send_from_directory(DATA/folder,filename)

if __name__=="__main__":
    app.run(host="127.0.0.1",port=6565,debug=False)
