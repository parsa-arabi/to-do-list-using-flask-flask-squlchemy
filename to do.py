from database import *

db.create_all()

path = "./static/"

# user = Users(username="username", password="password", image="logo.png")
# db.session.add(user)
# db.session.commit()

@app.route("/", methods=["POST", "GET"])
def home():
    for i in range(len(Users.query.all())):
        if Users.query.all()[i].username == request.cookies.get("user"):
            return render_template("index.html", user=request.cookies.get("user"), subject=Do.query.all(),items=len(Do.query.all()), cookie=request.cookies.get("user"), data=Users.query.all()[i])
    else:
        return redirect("/not_login")

@app.route("/not_login")
def not_login_page():
    return render_template("not_login.html")

@app.route("/edit", methods=['POST', 'GET'])
def edit():
    return render_template('edit.html')

@app.route("/edit_Do/<int:post_id>",methods=['POST','GET'])
def edit_Do(post_id):
    if request.cookies.get("user"):
        get = Do.query.get(post_id)
        if request.method == "POST":
            subject = request.form.get("subject")
            date = request.form.get("date")
            time = request.form.get("time")
            details = request.form.get("details")
            get.subject = subject
            get.date = date
            get.time = time
            get.details = details
            db.session.commit()
            flash("ویراش انجام شد", "primary")
            return redirect("/")
        else:
            return render_template("edit.html", data=get)
    else:
        return redirect("/login")

@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.cookies.get("user"):
        if request.method == "POST":
            subject = request.form.get("subject")
            date = request.form.get("date")
            time = request.form.get("time")
            details = request.form.get("details")
            flash("اضافه شد", "primary")
            x = jdatetime.date.today()
            admin = Do(subject=subject, time=time, date=date, t=x.strftime("%c"), author=Users.query.filter_by(username=request.cookies.get("user")).first(), details=details)
            db.session.add(admin)
            db.session.commit()
            return redirect("/")
        else:
            return render_template("add.html")
    else:
        return redirect("/login")

@app.route("/delete/<int:post_id>",methods=["POST", "GET"])
def delete(post_id):
    if request.cookies.get("user"):
        do = Do.query.get(post_id)
        db.session.delete(do)
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/login")

@app.route("/prof")
def first_profile():
    if request.cookies.get("user"):
        for i in range(len(Users.query.all())):
            if Users.query.all()[i].username == request.cookies.get("user"):
                return render_template("profile.html", image=Users.query.all()[i], data=Users.query.all()[i], name=Users.query.all()[i])
    else:
        flash("ابتدا باید وارد شوید", "warning")
        return redirect("/")

@app.route("/profile", methods=["POST", "GET"])
def editp():
    if request.cookies.get("user"):
        if request.method == "POST":
            image = request.files.get("file")
            username = request.form.get("username")
            passwords = request.form.get("password")
            re_password = request.form.get("re_password")
            user = Users.query.filter_by(username=request.cookies.get("user")).first()
            if passwords == re_password:
                user.password = passwords
                user.username = username
                if image:
                    image.save(os.path.join(path, "{}.png").format(request.cookies.get("user")))
                user.image = request.cookies.get("user") + ".png"
                db.session.commit()
                flash("تغیرات اعمال شد!", "info")
                response = make_response(redirect("/"))
                response.set_cookie("user", username)
                return response
        else:
            flash("رمز ها یکی نیستند!", "danger")
            return redirect("/prof")
    else:
        flash("ابتدا باید وارد شوید!", "warning")
        return redirect("/login")

@app.route("/show_details/<int:post_id>", methods=["POST", "GET"])
def show_details(post_id):
    if request.cookies.get("user"):
        do = Do.query.get(post_id)
        return render_template("details.html", user=request.cookies.get("user"), subject=do)
    else:
        return redirect("/login")

@app.route("/logout")
def logout():
    flash("خارج شدید", "danger")
    response = make_response(redirect("/login"))
    response.delete_cookie("user")
    return response

@app.route("/login",methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pas = request.form.get("password")
        found = False
        for u in range(len(Users.query.all())):
            if user == Users.query.all()[u].username and pas == Users.query.all()[u].password:
                flash("خوش آمدید", "success")
                response=make_response(redirect("/"))
                response.set_cookie("user", user)
                found = True
                return response
        if found == False:
            flash("نام یا رمز اشتباه است", "danger")
            return render_template("login.html")
    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def Register():
    if request.method == "POST":
        image = request.files.get("file")
        username = request.form.get("username")
        password = request.form.get("password")
        re_password = request.form.get("re_password")
        for i in range(len(Users.query.all())):
            if password == re_password and Users.query.all()[i].username != username:
                if image:
                    image.save(os.path.join(path, x))
                admin = Users(username=username, password=password, image=password + ".png")
                db.session.add(admin)
                db.session.commit()
                flash("عضو شدید", "success")
                return redirect("/add")
        else:
            flash("رمز و تکرار رمز هم خوانی ندارد شاید هم این نام قبلا ثبت شده", "danger")
            return render_template("Register.html")
    else:
        return render_template("Register.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9945)
