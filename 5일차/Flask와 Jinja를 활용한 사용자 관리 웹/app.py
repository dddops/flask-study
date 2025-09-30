from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 임시 사용자 데이터
users = [
    {"username": "traveler", "name": "Alex"},
    {"username": "photographer", "name": "Sam"},
    {"username": "gourmet", "name": "Chris"}
]

@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/add', methods = ['GET', 'POST'] )
def add_user():
  if request.method == 'POST':
    username = request.form['username']
    name = request.form['name']
    users.append({"username": username, "name": name})
    return redirect(url_for('index'))
  # GET 요청 시에는 사용자 추가 페이지만 보여줍니다.
  return render_template('add_user.html')


# 1. GET과 POST 요청을 모두 처리하도록 변경
@app.route('/edit/<username>', methods = ['GET', 'POST'])
def edit_user(username):
  # 수정할 사용자를 찾습니다.
  user_to_edit = None
  for user in users:
    if user['username'] == username:
      user_to_edit = user
      break

  # 사용자를 찾지 못하면 메인 페이지로 리다이렉트 (오류 처리)
  if user_to_edit is None:
    return redirect(url_for('index'))

  # 2. POST 요청일 때 (폼 제출 시) 데이터 수정
  if request.method == 'POST':
    new_name = request.form['name']
    user_to_edit['name'] = new_name
    return redirect(url_for('index'))
  
  # 3. GET 요청일 때 (수정 페이지 첫 접근 시)
  return render_template('edit_user.html', user=user_to_edit)

# 4. GET 요청으로 삭제를 처리하도록 methods=['DELETE'] 제거
@app.route('/delete/<username>')
def delete_user(username):
  for user in users:
    if user['username'] == username:
      users.remove(user)
      break
  return redirect(url_for('index'))

    
# 사용자 추가, 수정, 삭제 라우트 및 함수 작성...

if __name__ == '__main__':
    app.run(debug=True)
