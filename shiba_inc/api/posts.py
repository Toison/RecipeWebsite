"""REST API for posts."""
from cgitb import reset
from multiprocessing import connection
import flask
from flask import session, url_for, jsonify, \
    request, abort
import arrow
from isort import file
from itsdangerous import json
import shiba_inc
import uuid
import pathlib

@shiba_inc.app.route('/api/v1/index/', methods=["GET", "POST"])
def get_index_recipes():
    connection = shiba_inc.model.get_db()
    if request.method == 'POST':
        likestr =  f"WHERE LOWER(posts.recipename) LIKE \"%{request.json['query']:s}%\" "
        
        tags = request.json['query'].split(' ')
        postids = set()
        first = True
        for tag in tags:
            # print(f'checking for {tag}')
            if tag == '':
                continue
            tag_posts = connection.execute(
                "SELECT DISTINCT tags.postid "
                "FROM tagnames "
                "JOIN tags ON tags.tagid = tagnames.tagid "
                f"WHERE LOWER(tagnames.name) LIKE \"{tag:s}%\" "
                "ORDER BY tags.postid DESC "
            ).fetchall()
            
            # print(f'found {len(tag_posts)}')
            # print(tag_posts)
            if len(tag_posts) == 0:
                continue

            if first:
                for x in tag_posts:
                    postids.add(str(x['postid']))
            else:
                n = set()
                for x in tag_posts:
                    if str(x['postid']) in postids:
                        n.add(str(x['postid']))
                postids = n  
            first = False
        # print(postids)
        # print(tag_posts)
        likestr += f"OR posts.postid IN ({','.join(list(postids))}) "
    else:
        likestr = ""

    my_post = connection.execute(
        "SELECT users.username, users.fullname, users.filename, posts.postid, posts.recipename, posts.created "
        "FROM posts "
        "JOIN users ON users.username = posts.owner "
        + likestr +
        "ORDER BY posts.postid DESC "
        "LIMIT 10 "
    ).fetchall()
    
    if len(my_post) == 0:
        context = {
            "recipes": [],
            "in_session": "username" in session
        }
        return jsonify(**context)
    
    for post in my_post:
        post['created'] = arrow.get(post['created']).humanize()
        
        post['filename'] = f"/uploads/{post['filename']}"
        
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
        post['rating'] = rating
        
        is_liking = False
        if "username" in session:
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
                    "WHERE postid = ?",
                    (post['postid'],)
        ).fetchall()
        post['likenum'] = len(like_info)
    
        tag_info = connection.execute(
                    "SELECT * "
                    "FROM tags "
                    "WHERE postid = ?",
                    (post['postid'],)
        ).fetchall()
        tag_list = []
        for tag in tag_info:
            tag_name = connection.execute(
                    "SELECT name "
                    "FROM tagnames "
                    "WHERE tagid = ?",
                    (tag['tagid'],)
            ).fetchone()
            tag_list.append(tag_name['name'])
        post['tag_list'] = tag_list
    # print(my_post)
    
    context = {
        "recipes": my_post,
        "in_session": "username" in session
    }
    
    return jsonify(**context)
    

@shiba_inc.app.route(
    '/api/v1/p/<int:postid_url_slug>/', methods=["GET"])
def get_post(postid_url_slug):
    """Get comments for post."""
    connection = shiba_inc.model.get_db()

    # check if postid is out of range
    my_post = connection.execute(
        "SELECT * "
        "FROM posts "
        "WHERE postid = ?", (postid_url_slug,)
    ).fetchall()

    if len(my_post) == 0:
        abort(404)

    context = {
        "owner": my_post[0]['owner'],
        "url": flask.request.path
    }

    return jsonify(**context)

@shiba_inc.app.route(
    '/api/v1/p/<int:postid_url_slug>/hdr', methods=["GET"])
def get_post_hdr(postid_url_slug):
    """Get comments for post."""
    connection = shiba_inc.model.get_db()

    # check if postid is out of range
    post_info = connection.execute(
        "SELECT * "
        "FROM posts "
        "WHERE postid = ?", (postid_url_slug,)
    ).fetchall()

    if len(post_info) == 0:
        abort(404)

    owner = connection.execute(
        "SELECT *"
        "FROM users "
        "WHERE username = ?", (post_info[0]['owner'],)
    ).fetchone()

    rating_info = connection.execute(
        "SELECT ratevalue "
        "FROM comments "
        "WHERE postid = ?", (postid_url_slug,)
    ).fetchall()
    
    rating = 0.0
    for entry in rating_info:
        rating += entry['ratevalue']
    if len(rating_info) != 0:
        rating = rating/ float(len(rating_info))

    is_following = False
    
    if "username" in session:
        check_following = connection.execute(
                "SELECT * "
                "FROM following "
                "WHERE follower = ? AND followee = ?",
                (session["username"], owner['username'])
        ).fetchall()

        is_following = (len(check_following) > 0)
        
    is_liking = False
    if "username" in session:
        check_following = connection.execute(
                "SELECT * "
                "FROM likes "
                "WHERE liker = ? AND postid = ?",
                (session["username"], postid_url_slug)
        ).fetchall()

        is_liking = (len(check_following) > 0)

    like_info = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE postid = ?",
        (postid_url_slug,)
    ).fetchall()
    num_likes = len(like_info)
    
    tag_info = connection.execute(
        "SELECT tagnames.name "
        "FROM tags "
        "JOIN tagnames ON tags.tagid = tagnames.tagid WHERE tags.postid = ?",
        (postid_url_slug,)
    ).fetchall()
    
    tag_list = []
    for tag in tag_info:
        tag_list.append(tag['name'])
    
    context = {
        "recipeName": post_info[0]['recipename'],
        "ownerusername": owner['username'],
        "ownerfullname": owner['fullname'],
        "following": is_following,
        "time": arrow.get(post_info[0]['created']).humanize(),
        "icon": f"/uploads/{owner['filename']}",
        "rating": rating,
        "in_session": "username" in session,
        "is_self": (session["username"] == owner["username"]) if ("username" in session) else False,
        "is_liking": is_liking,
        "num_likes": num_likes,
        "tag_list": tag_list,
    }

    return jsonify(**context)

@shiba_inc.app.route(
    '/api/v1/p/<int:postid_url_slug>/stp', methods=["GET"])
def get_post_stp(postid_url_slug):
    """Get comments for post."""
    connection = shiba_inc.model.get_db()

    # check if postid is out of range
    step_info = connection.execute(
        "SELECT stepnum, imgpath, text "
        "FROM steps "
        "WHERE postid = ?", (postid_url_slug,)
    ).fetchall()
        
    for step in step_info:
        step['imgpath'] = f"/uploads/{step['imgpath']}"
        

    context = {
        "stepList": step_info
    }

    return jsonify(**context)

@shiba_inc.app.route(
    '/api/v1/p/<int:postid_url_slug>/cmt', methods=["GET"])
def get_post_cmt(postid_url_slug):
    """Get comments for post."""
    connection = shiba_inc.model.get_db()

    # check if postid is out of range
    comment_info = connection.execute(
        "SELECT users.username, users.fullname, users.filename, comments.commentid, comments.text, comments.ratevalue, comments.created "
        "FROM comments "
        "JOIN users ON users.username = comments.commenter AND comments.postid = ?", (postid_url_slug,)
    ).fetchall()
    
    print(comment_info)
    
    for comment in comment_info:
        comment['created'] = arrow.get(comment['created']).humanize()
        comment['filename'] = f"/uploads/{comment['filename']}"
        
    context = {
        "commentList": comment_info,
        "in_session": "username" in session,
    }

    return jsonify(**context)

@shiba_inc.app.route(
    '/api/v1/p/<int:postid_url_slug>/cmt', methods=["POST"])
def post_post_comments(postid_url_slug):
    """Post comments for posts."""
    if "username" in session:
        connection = shiba_inc.model.get_db()
        text = request.json['text']
        rating = request.json['rating']
        if text == '':
            abort(400)
        cur_id = connection.execute("SELECT MAX(commentid) "
                                    "FROM comments").fetchone()
        cur_id = cur_id['MAX(commentid)']
        if cur_id is None:
            cur_id = 1
        else:
            cur_id += 1
            
        connection.execute("INSERT INTO comments "
                           "(commentid, commenter, postid, text, ratevalue) "
                           "VALUES (?, ?, ?, ?, ?)",
                           (cur_id, session['username'],
                            postid_url_slug, text, rating,))

        comment_info = connection.execute(
            "SELECT users.username, users.fullname, users.filename, comments.commentid, comments.text, comments.ratevalue, comments.created "
            "FROM comments "
            "JOIN users ON users.username = comments.commenter AND comments.commentid = (?)", (cur_id,)
        ).fetchone()

        comment_info['created'] = arrow.get(comment_info['created']).humanize()
        comment_info['filename'] = f"/uploads/{comment_info['filename']}"

        context = {
            "comment_update": comment_info,
        }

        return jsonify(**context), 201
    abort(403)
    return None

@shiba_inc.app.route('/api/v1/u/<userid_url_slug>/follow', methods=["Post"])
def follow(userid_url_slug):
    if "username" in session:
        connection = shiba_inc.model.get_db()
        op = request.json['op']
        
        check_following = connection.execute(
            "SELECT * "
            "FROM following "
            "WHERE follower = ? AND followee = ?",
            (session["username"], userid_url_slug)
        ).fetchall()
        
        is_following = (len(check_following) > 0)
        
        if op == "follow" and not is_following:
            connection.execute(
                "INSERT INTO following(follower, followee) "
                "VALUES(?, ?)", (session["username"], userid_url_slug)
            )
            context = {
            "is_following": True
            }
            return jsonify(**context), 201
        elif op == "unfollow" and is_following:
            connection.execute(
                "DELETE FROM following "
                "WHERE follower = ? AND followee = ?",
                (session["username"], userid_url_slug)
            )
            context = {
            "is_following": False
            }
            return jsonify(**context), 201
        else:
            abort(400)
             
    abort(403)

@shiba_inc.app.route('/api/v1/p/<postid_url_slug>/like', methods=["Post"])
def like(postid_url_slug):
    print('here')
    if "username" not in session:
        abort(403)
    connection = shiba_inc.model.get_db()
    op = request.json['op']
    
    check_liking = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE liker = ? AND postid = ?",
        (session["username"], postid_url_slug)
    ).fetchall()
        
    is_liking = (len(check_liking) > 0)
    
    if op == "like" and not is_liking:
        connection.execute(
            "INSERT INTO likes(liker, postid) "
            "VALUES(?, ?)", (session["username"], postid_url_slug)
        )
        context = {
            "is_liking": True
        }
        return jsonify(**context), 201
    elif op == "unlike" and is_liking:
        connection.execute(
            "DELETE FROM likes "
            "WHERE liker = ? AND postid = ?",
            (session["username"], postid_url_slug)
        )
        context = {
            "is_liking": False
        }
        return jsonify(**context), 201
    else:
        return "Bad Request", 400

@shiba_inc.app.route('/api/v1/get-tags/', methods=["GET"])
def get_tags():
    connection = shiba_inc.model.get_db()
    geotags = connection.execute(
        "SELECT * "
        "FROM tagnames "
        "WHERE category = ?", ("geo",)
    ).fetchall()
    
    ingtags = connection.execute(
        "SELECT * "
        "FROM tagnames "
        "WHERE category = ?", ("ing",)
    ).fetchall()
        
    tastags = connection.execute(
        "SELECT * "
        "FROM tagnames "
        "WHERE category = ?", ("tas",)
    ).fetchall()
            
    reqtags = connection.execute(
        "SELECT * "
        "FROM tagnames "
        "WHERE category = ?", ("req",)
    ).fetchall()
    
    for tag in geotags:
        tag['picked'] = False
    for tag in ingtags:
        tag['picked'] = False
    for tag in tastags:
        tag['picked'] = False
    for tag in reqtags:
        tag['picked'] = False
    
    context = {
        "geotags": geotags,
        "ingtags": ingtags,
        "tastags": tastags,
        "reqtags": reqtags,
    }
    return jsonify(**context), 201
    

@shiba_inc.app.route('/api/v1/add-post', methods=["Post"])
def add_post():
    if "username" not in session:
        abort(403)
    
    connection = shiba_inc.model.get_db()
    postName = request.json['text']
    cur_postid = request.json['pid']
    tags = request.json['tagList']
    
    post_info = connection.execute(
        "SELECT * "
        "FROM posts "
        "WHERE postid = ?", (cur_postid,)
    ).fetchall()
    
    if len(post_info) != 0:
        connection.execute(
            "UPDATE posts "
            "SET recipename = ? WHERE postid = ?", (postName, cur_postid,)
        )
        
        connection.execute(
            "DELETE FROM tags "
            "WHERE postid = ?", (cur_postid,)
        )
        
        for tagid in tags:
            connection.execute("INSERT INTO tags "
                            "(postid, tagid) "
                            "VALUES (?, ?)",
                            (cur_postid, tagid,))
    else:
        cur_postid = connection.execute(
                    "SELECT MAX(postid) "
                    "FROM posts").fetchone()
        cur_postid = cur_postid['MAX(postid)']
        print(cur_postid)
        if cur_postid is None:
            cur_postid = 1
        else:
            cur_postid += 1

        connection.execute("INSERT INTO posts "
                        "(postid, recipename, owner) "
                        "VALUES (?, ?, ?)",
                        (cur_postid, postName,
                        session['username']))
        
        for tagid in tags:
            connection.execute("INSERT INTO tags "
                            "(postid, tagid) "
                            "VALUES (?, ?)",
                            (cur_postid, tagid,))
    
    context = {
        "pid": cur_postid,
    }
    
    return jsonify(**context)    

@shiba_inc.app.route('/api/v1/upload-file/', methods=["Post"])
def new_post():
    print(request.files)
    file = request.files['file']
    filename = file.filename
    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex,
        suffix=pathlib.Path(filename).suffix
    )
    path = shiba_inc.app.config["UPLOAD_FOLDER"] / uuid_basename
    file.save(path)
    
    context = {
        "filename": uuid_basename,
        "img_path": f"/uploads/{uuid_basename}"
    }
    
    return jsonify(**context)

@shiba_inc.app.route('/api/v1/p/<postid_url_slug>/add-step/', methods=["Post"])
def add_step(postid_url_slug):
    if "username" not in session:
        abort(403)
    connection = shiba_inc.model.get_db()
    print(request.json)
    stepnum = request.json['stepnum']
    steptext = request.json['text']
    stepimg = request.json['filename']

    step_info = connection.execute(
        "SELECT * "
        "FROM steps "
        "WHERE postid = ? AND stepnum = ?", (postid_url_slug, stepnum,)
    ).fetchall()
    
    if len(step_info) != 0:
        # delete_img(step_info[0]['imgpath'])
        connection.execute(
            "UPDATE steps "
            "SET text = ?, imgpath = ? WHERE postid = ? AND stepnum = ?", (steptext, stepimg, postid_url_slug, stepnum,)
        )
    else:
        connection.execute(
            "INSERT INTO steps "
            "(postid, stepnum, text, imgpath) "
            "VALUES (?, ?, ?, ?)",
            (postid_url_slug, stepnum, steptext, stepimg,)
        )
    return "OK"

@shiba_inc.app.route('/api/v1/p/<postid_url_slug>/delete-post/', methods=["Post"])
def delete_step(postid_url_slug):
    connection = shiba_inc.model.get_db()
    steps = connection.execute(
        "SELECT * "
        "FROM steps "
        "WHERE postid = ?", (postid_url_slug,)
    ).fetchall()

    for step in steps: 
        delete_img(step['imgpath'])
    
    connection.execute(
        "DELETE FROM posts "
        "WHERE postid = ?", (postid_url_slug,)
    )

    return "OK"
    
def delete_img(filename):
    img_path = pathlib.Path(
        shiba_inc.app.config["UPLOAD_FOLDER"] / filename)
    img_path.unlink()

