from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

app = Flask(__name__)


#################################
# db 설정
#################################
BASE_DIR = os.path.dirname(__file__)
# /Users/rubykim/Desktop/personal/OZ-coding-BE14-Flask/250924 (Day 3)/실습2

INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
# /Users/rubykim/Desktop/personal/OZ-coding-BE14-Flask/250924 (Day 3)/실습2/instance

os.makedirs(INSTANCE_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(INSTANCE_DIR, "todos.db")}"
engine = create_engine(
    DATABASE_URL,
    echo=True
)
# engine = create_engine("sqlite:///instance/todos.db", echo=True)

SessionLocal = sessionmaker(bind=engine)


#################################
# 모델 정의
#################################
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)

    def __repr__(self): 
        return f"<Todo(id={self.id}, task='{self.task}')>"

Base.metadata.create_all(bind=engine)

# todos = {
#     1: "flask 공부하기",
#     2: "파이썬 공부하기",
# }



#################################
# api
#################################

# 1. 전체 목록 조회: GET
@app.route("/todos", methods=["GET"])
def get_todos():
    db = SessionLocal()
    todos = db.query(Todo).all()
    db.close()
    return jsonify([{"id": t.id, "task": t.task} for t in todos])


# 2. 특정 항목 조회: GET
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    db = SessionLocal()
    todo = db.query(Todo).get(todo_id)
    db.close()
    if not todo:
        return jsonify({"error": "할 일이 없습니다"}), 404
    return jsonify({"id": todo.id, "task": todo.task})


# 3. 항목 추가: POST
@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    db = SessionLocal()

    # 데이터 삽입
    new_todo = Todo(task=data["task"])
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo) # commit 이후로 자동 생성된 id 불러오기 위해 세팅
    db.close()
    return jsonify({"id": new_todo.id, "task": new_todo.task}), 201


# 4. 항목 수정: PUT, PATCH
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todos(todo_id):
    data = request.get_json()
    db = SessionLocal()

    # db에서 항목 찾기
    todo = db.query(Todo).get(todo_id)
    if not todo: # 못찾으면 db닫고 404 반환
        db.close()
        return jsonify({"error": "할 일이 없습니다"}), 404
    
    # 데이터가 있으면 업데이트
    todo.task = data["task"]
    db.commit()

    # 업데이트 된 정보
    updated = {"id": todo.id, "task": todo.task}
    db.close()
    return jsonify(updated)


# 5. 항목 삭제: DELETE
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todos(todo_id):
    db = SessionLocal()

    # db에서 항목 찾기
    todo = db.query(Todo).get(todo_id)
    if not todo: # 데이터가 없으면 바로 db close
        db.close()
        return jsonify({"error": "할 일을 찾을 수 없습니다"}), 404
    
    # 데이터 삭제
    db.delete(todo)
    db.commit()
    db.close()
    return jsonify({"deleted": "삭제 완료!"})


if __name__ == '__main__':
    app.run(debug=True)