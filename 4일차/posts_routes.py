from flask import request, jsonify, abort
from flask_smorest import Blueprint

def create_posts_blueprint(mysql):
  posts_blp = Blueprint("Posts", __name__, description="Operations on blog posts", url_prefix="/posts")

  @posts_blp.route("/", methods=["GET", "POST"])
  def posts():
      cursor = mysql.connection.cursor()

      if request.method == "GET":
        sql = "SELECT * FROM posts"
        cursor.execute(sql)

        posts = cursor.fetchall()
        cursor.close()

        posts_list = []
        for post in posts:
            posts_list.append({
                "id": post[0],
                "title": post[1],
                "content": post[2]
            })
        return jsonify(posts_list)
      
      if request.method == "POST":
        title = request.json.get("title")
        content = request.json.get("content")
        
        if not title or not content:
           abort(400, message="Title or content are empty.")

        
        sql = "INSERT INTO posts (title, content) VALUES (%s, %s)"
        cursor.execute(sql, (title, content))
        
        mysql.connection.commit()

        return {"message": "successfully created"}, 201
      
      
  @posts_blp.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
  def post(id):
      cursor = mysql.connection.cursor()

      if request.method == "GET":
        sql = f"SELECT * FROM posts WHERE id = {id}"
        cursor.execute(sql)
        post = cursor.fetchone()

        if not post:
            abort(404, message="Post not found.")
        return jsonify({
            "id": post[0],
            "title": post[1],
            "content": post[2]
        })
     
      elif request.method == "PUT":
          title = request.json.get("title")
          content = request.json.get("content")

          if not title or not content:
              abort(400, message="title 또는 content가 없습니다.")

          sql = "SELECT * FROM posts WHERE id=%s"
          cursor.execute(sql, (id,))
          post = cursor.fetchone()

          if not post:
              abort(404, message="해당 게시글이 없습니다.")

          sql = "UPDATE posts SET title=%s, content=%s WHERE id=%s"
          cursor.execute(sql, (title, content, id))
          mysql.connection.commit()
      
      elif request.method == "DELETE":
        sql = "SELECT * FROM posts WHERE id=%s"
        cursor.execute(sql, (id,))
        post = cursor.fetchone()

        if not post:
            abort(404, message="해당 게시글이 없습니다.")

        sql = "DELETE FROM posts WHERE id=%s"
        cursor.execute(sql, (id,))
        mysql.connection.commit()

        return jsonify({"message": "Successfully deleted post"})

  return posts_blp
