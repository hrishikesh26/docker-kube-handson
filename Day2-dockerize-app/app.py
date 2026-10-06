from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
todos = []  # in-memory: resets when the app restarts

PAGE = """
<!doctype html>
<title>To-Do</title>
<h1>To-Do</h1>
<form method="post" action="/add">
  <input name="task" placeholder="New task" required autofocus>
  <button>Add</button>
</form>
<ul>
  {% for t in todos %}
  <li>{{ t }}
    <form method="post" action="/delete/{{ loop.index0 }}" style="display:inline">
      <button>x</button>
    </form>
  </li>
  {% endfor %}
</ul>
"""


@app.get("/")
def index():
    return render_template_string(PAGE, todos=todos)


@app.post("/add")
def add():
    todos.append(request.form["task"])
    return redirect("/")


@app.post("/delete/<int:i>")
def delete(i):
    if 0 <= i < len(todos):
        todos.pop(i)
    return redirect("/")


if __name__ == "__main__":
    # 0.0.0.0 so it's reachable from outside a Docker container later
    app.run(host="0.0.0.0", port=5000)
