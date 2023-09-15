"""
shiba_inc index (main) view.
URLs include:
/
"""
import uuid
import flask
import hashlib
import arrow
import pathlib
from flask import redirect, url_for, render_template
from flask import request, session, abort, send_from_directory
import shiba_inc

@shiba_inc.app.route('/', methods=["GET"])
def show_index():
    context = {}
    return flask.render_template("index.html", **context)

@shiba_inc.app.route("/p/<post_url_slug>", methods=["GET"])
def show_post(post_url_slug):
    context = {
        'postid': post_url_slug
    }
    return render_template("recipe.html", **context)

@shiba_inc.app.route("/u/<user_url_slug>/", methods=["GET"])
def user(user_url_slug):
    """User function."""
    if "username" in session:
        connection = shiba_inc.model.get_db()

        userInfo = connection.execute(
            "SELECT *"
            "FROM users "
            "WHERE username = ?", (user_url_slug,)
        ).fetchall()

        if len(userInfo) == 0:
            abort(404)

        fullname = userInfo[0]['fullname']
        profile_img = f"/uploads/{userInfo[0]['filename']}"
        create_time = arrow.get(userInfo[0]['created']).format('MMMM YYYY')

        check_following = connection.execute(
            "SELECT * "
            "FROM following "
            "WHERE follower = ? AND followee = ?",
            (session["username"], user_url_slug)
        ).fetchall()

        is_following = (len(check_following) > 0)

        created_posts = connection.execute(
            "SELECT * "
            "FROM posts "
            "WHERE owner = ?", (user_url_slug,)
        ).fetchall()

        liked_posts = connection.execute(
            "SELECT postid "
            "FROM likes "
            "WHERE liker = ?", (user_url_slug,)
        ).fetchall()

        for post in created_posts:
            post['created'] = arrow.get(post['created']).humanize()
            
            lastImg = connection.execute(
                "SELECT imgpath "
                "FROM steps "
                "WHERE postid = ? ORDER BY stepnum DESC LIMIT 1", (post['postid'],)
            ).fetchone()
            post['recipeImg'] = f"/uploads/{lastImg['imgpath']}"
            
            rating_info = connection.execute(
                "SELECT ratevalue "
                "FROM comments "
                "WHERE postid = ?", (post['postid'],)
            ).fetchall()
            rating = 0.0
            for entry in rating_info:
                rating += entry['ratevalue']
            if len(rating_info) != 0:
                rating = rating/ float(len(rating_info))
            post['rating'] = round(rating, 1)

            is_liking = False
            check_following = connection.execute(
                    "SELECT * "
                    "FROM likes "
                    "WHERE liker = ? AND postid = ?",
                    (session["username"], post['postid'])
            ).fetchall()
            is_liking = (len(check_following) > 0)
            post['is_liking'] = is_liking

            like_info = connection.execute(
                "SELECT * "
                "FROM likes "
                "WHERE postid = ?", (post['postid'],)
            ).fetchall()
            post['likenum'] = len(like_info)
        
        for post in liked_posts:
            post_info = connection.execute(
                "SELECT * "
                "FROM posts "
                "WHERE postid = ? ", (post['postid'],)
            ).fetchone()

            user_info = connection.execute(
                "SELECT username, fullname, filename "
                "FROM users "
                "WHERE username = ? ", (post_info['owner'],)
            ).fetchone()

            post['filename'] = f"/uploads/{user_info['filename']}"
            post['fullname'] = user_info['fullname']
            post['username'] = user_info['username']

            post['created'] = arrow.get(post_info['created']).humanize()

            lastImg = connection.execute(
                "SELECT imgpath "
                "FROM steps "
                "WHERE postid = ? ORDER BY stepnum DESC LIMIT 1", (post['postid'],)
            ).fetchone()
            post['recipeImg'] = f"/uploads/{lastImg['imgpath']}"
            
            rating_info = connection.execute(
                "SELECT ratevalue "
                "FROM comments "
                "WHERE postid = ?", (post['postid'],)
            ).fetchall()
            rating = 0.0
            for entry in rating_info:
                rating += entry['ratevalue']
            if len(rating_info) != 0:
                rating = rating/ float(len(rating_info))
            post['rating'] = round(rating, 1)

            like_info = connection.execute(
                "SELECT * "
                "FROM likes "
                "WHERE postid = ?", (post['postid'],)
            ).fetchall()
            post['likenum'] = len(like_info)

        # posts = len(posts_info)

        num_following = connection.execute(
            "SELECT COUNT(*) "
            "FROM following "
            "WHERE follower = ?", (user_url_slug,)
        ).fetchone()['COUNT(*)']

        num_follower = connection.execute(
            "SELECT COUNT(*) "
            "FROM following "
            "WHERE followee = ?", (user_url_slug,)
        ).fetchone()['COUNT(*)']

        context = {
            "user": user_url_slug,
            "isfollowing": is_following,
            "profile_img": profile_img,
            # "posts": posts,
            "following": num_following,
            "follower": num_follower,
            "fullname": fullname,
            "create_time": create_time,
            "createdPosts": created_posts,
            "likedPosts": liked_posts
        }

        return render_template("user.html", **context)
    return redirect(url_for("login"))

@shiba_inc.app.route('/newpost/', methods=['GET'])
def new_post_page():
    if 'username' not in session:
        abort(403)
    
    context = {}
    
    return render_template("newpost.html", **context)

@shiba_inc.app.route("/following/", methods=["POST"])
def follow_user():
    """Follow function."""
    connection = shiba_inc.model.get_db()

    if 'operation' not in request.form:
        abort(400)
    task = request.form["operation"]
    usr2 = request.form["username"]
    following_check = connection.execute(
        "SELECT COUNT(follower) "
        "FROM following "
        "WHERE follower = ? AND followee = ?", (session["username"], usr2)
    ).fetchone()['COUNT(follower)']

    if task == "follow":

        if following_check > 0:
            abort(409)
        else:
            connection.execute(
                "INSERT INTO following(follower, followee) "
                "VALUES(?, ?)", (session["username"], usr2)
            )

    elif task == 'unfollow':

        if following_check == 0:
            abort(409)
        else:
            connection.execute(
                "DELETE FROM following "
                "WHERE follower = ? AND followee = ?",
                (session["username"], usr2)
            )

    redirect_url = request.args.get('target')
    if redirect_url is None:
        redirect_url = '/'

    return redirect(redirect_url)

@shiba_inc.app.route(
    '/follow/<username>/', methods=["GET"])
def get_follow_lists(username):
    if "username" not in session:
        return redirect(url_for("login"))

    connection = shiba_inc.model.get_db()

    ### get following lists
    following_lists_temp = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE follower = ?", (username,)
    ).fetchall()

    following_lists = []
    following_lists_avatar_src = []
    for user in following_lists_temp:
        following_name = user["followee"]
        following_lists.append(following_name)

        userInfo = connection.execute(
            "SELECT *"
            "FROM users "
            "WHERE username = ?", (following_name,)
        ).fetchall()
        profile_img = f"/uploads/{userInfo[0]['filename']}"
        following_lists_avatar_src.append(profile_img)
    # print("following_lists is ", following_lists);



    ### get follower lists
    follower_lists_temp = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE followee = ?", (username,)
    ).fetchall()

    # print("follower_lists_temp is ", follower_lists_temp);
    follower_lists = []
    follower_lists_avatar_src = []
    for user in follower_lists_temp:
        follower_name = user["follower"]
        follower_lists.append(follower_name)

        userInfo = connection.execute(
            "SELECT *"
            "FROM users "
            "WHERE username = ?", (follower_name,)
        ).fetchall()

        profile_img = f"/uploads/{userInfo[0]['filename']}"
        follower_lists_avatar_src.append(profile_img)
    # print("follower_lists is ", follower_lists)


    ## return content
    context = {
        "following": following_lists,
        "following_lists_avatar_src": following_lists_avatar_src,

        "follower": follower_lists,
        "follower_lists_avatar_src": follower_lists_avatar_src,
    }

    # return jsonify(**context)
    return render_template("follow.html", **context)


@shiba_inc.app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    """Read and return uploaded file on server."""
    # if 'username' not in session:
    #     abort(403)

    # check if file exists
    temp_file = pathlib.Path(shiba_inc.app.config["UPLOAD_FOLDER"] / filename)
    if not temp_file.is_file():
        abort(404)

    return send_from_directory(shiba_inc.app.config["UPLOAD_FOLDER"],
                               filename, as_attachment=True)

@shiba_inc.app.route("/accounts/login/", methods=["GET"])
def login():
    """Login function."""
    if "username" in session:
        return redirect(url_for("show_index"))
    return render_template("login.html")

@shiba_inc.app.route("/accounts/logout/", methods=["GET", "POST"])
def logout():
    """Logout function."""
    if "username" in session:
        session.clear()
        return redirect(url_for("login"))
    return redirect(url_for("login"))

@shiba_inc.app.route("/accounts/create/", methods=["GET"])
def create():
    """Create function."""
    if "username" in session:
        return redirect(url_for('edit'))
    return render_template("create.html")

@shiba_inc.app.route("/accounts/", methods=["POST"])
def accounts():
    """Accounts function."""
    connection = shiba_inc.model.get_db()

    if 'operation' not in request.form:
        abort(400)
    task = request.form["operation"]
    if task == "login":
        login_helper(connection)

    elif task == "create":
        create_helper(connection)

    elif task == 'edit_account':
        edit_helper(connection)

    elif task == 'update_password':
        update_pwd_helper(connection)

    elif task == 'delete':
        delete_helper(connection)

    redirect_url = request.args.get('target')
    if redirect_url is None:
        redirect_url = '/'

    return redirect(redirect_url)

@shiba_inc.app.route("/accounts/edit/", methods=['GET'])
def edit():
    """Edit function."""
    if "username" in session:
        connection = shiba_inc.model.get_db()
        info = connection.execute(
            "SELECT *"
            "FROM users "
            "WHERE username = ?", (session['username'],)
        ).fetchall()

        context = {'img_file': info[0]['filename'],
                   'fullname': info[0]['fullname'],
                   'email': info[0]['email']}

        return render_template('edit.html', **context)
    return redirect(url_for("login"))

@shiba_inc.app.route("/accounts/password/", methods=['GET'])
def password():
    """Change Password."""
    if "username" in session:
        return render_template('password.html')
    return redirect(url_for("login"))

def login_helper(connection):
    """User login helper."""
    for k in ['username', 'password']:
        if k not in request.form:
            abort(400)

    username = request.form["username"]
    input_password = request.form["password"]

    keys = ['username', 'password']
    for k in keys:
        if k not in request.form:
            abort(400)

    for k in keys:
        if len(request.form[k]) == 0:
            abort(400)

    info = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ?", (username,)
    ).fetchall()

    if len(info) == 0:
        abort(403)

    password_db_string = info[0]['password']
    if not verify_pwd(input_password, password_db_string):
        abort(403)

    # start session here:
    session["username"] = username
    
def create_helper(connection):
    """User creation helper."""
    if 'file' not in request.files or \
            request.files['file'].filename == '':
        abort(400)
    else:
        uuid_basename = file_rename_upload('file')

    keys = ['fullname', 'username', 'email', 'password']
    for k in keys:
        if k not in request.form:
            abort(400)

    fullname = request.form["fullname"]
    username = request.form["username"]
    email = request.form["email"]
    new_password = request.form["password"]

    for k in keys:
        if len(request.form[k]) == 0:
            abort(400)

    password_db_string = encrypt_pwd(new_password)
    cur = connection.execute(
        "SELECT COUNT(username) "
        "FROM users "
        "WHERE username = ?", (username,)
    )

    if cur.fetchall()[0]['COUNT(username)'] > 0:
        abort(409)

    connection.execute(
        "INSERT INTO users(username, fullname,"
        "email, filename, password)"
        "VALUES (?, ?, ?, ?, ?)", (username, fullname, email,
                                   uuid_basename, password_db_string)
    )

    session["username"] = username

def delete_helper(connection):
    """Delete account helper."""
    if 'username' not in session:
        abort(403)

    posts = connection.execute(
        "SELECT filename "
        "FROM posts "
        "WHERE owner = ?", (session['username'],)
    ).fetchall()

    # remove posts from session['username']
    for post_temp in posts:
        post_name = post_temp['filename']
        post_path = pathlib.Path(
            shiba_inc.app.config["UPLOAD_FOLDER"] / post_name)
        post_path.unlink()

    icon = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ?", (session['username'],)
    ).fetchall()

    icon_path = icon[0]['filename']
    icon_path = pathlib.Path(
        shiba_inc.app.config["UPLOAD_FOLDER"] / icon_path)
    icon_path.unlink()

    connection.execute("DELETE FROM users "
                       "WHERE username = ?", (session['username'],))

    session.clear()

def edit_helper(connection):
    """Edit account helper."""
    if 'username' not in session:
        abort(403)

    for k in ['fullname', 'email']:
        if k not in request.form:
            abort(400)
        if len(request.form[k]) == 0:
            abort(400)

    username = session['username']
    fullname = request.form["fullname"]
    email = request.form["email"]

    file_flag = request.files['file'].filename != ''

    if file_flag:
        # fetch original file and remove it
        orig_filename = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ?", (username,)
        ).fetchall()
        orig_filename = orig_filename[0]['filename']
        orig_filepath = pathlib.Path(
            shiba_inc.app.config["UPLOAD_FOLDER"] / orig_filename)

        orig_filepath.unlink()

        uuid_basename = file_rename_upload('file')
        connection.execute("UPDATE users "
                           "SET fullname = ?, "
                           "email = ?, filename = ?"
                           "WHERE username = ?",
                           (fullname, email, uuid_basename, username))
    else:
        connection.execute("UPDATE users "
                           "SET fullname = ?, email = ?"
                           "WHERE username = ?",
                           (fullname, email, username))

def update_pwd_helper(connection):
    """Update password helper."""
    if 'username' not in session:
        abort(403)

    # check if all keys exist
    for i in ['password', 'new_password1', 'new_password2']:
        if i not in request.form:
            abort(400)

    old_pwd = request.form['password']
    new_pwd1 = request.form['new_password1']
    new_pwd2 = request.form['new_password2']

    # check not empty string
    for i in [old_pwd, new_pwd1, new_pwd2]:
        if len(i) == 0:
            abort(400)

    if new_pwd1 != new_pwd2:
        abort(401)

    # verify old password
    encrypted_pwd = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ?", (session['username'],)
    ).fetchall()
    encrypted_pwd = encrypted_pwd[0]['password']
    if not verify_pwd(old_pwd, encrypted_pwd):
        abort(403)

    # encrypt new password and insert to DB
    new_enc_pwd = encrypt_pwd(new_pwd1)
    connection.execute("UPDATE users "
                       "SET password = ?"
                       "WHERE username = ?",
                       (new_enc_pwd, session['username']))


def file_rename_upload(file_name):
    """Get UUID in form, save, and return UUID."""
    fileobj = flask.request.files[file_name]
    filename = fileobj.filename
    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex,
        suffix=pathlib.Path(filename).suffix
    )

    path = shiba_inc.app.config["UPLOAD_FOLDER"] / uuid_basename
    fileobj.save(path)
    return uuid_basename


def verify_pwd(input_pwd, encpt_pwd):
    """Verify input and match password."""
    pwlist = encpt_pwd.split("$")
    algorithm = pwlist[0]
    salt = pwlist[1]
    password_hash_from_db = pwlist[2]

    hash_obj = hashlib.new(algorithm)
    password_salted = salt + input_pwd
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()

    return password_hash == password_hash_from_db


def encrypt_pwd(input_pwd):
    """Encrypt the input password using sha512."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + input_pwd
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string
