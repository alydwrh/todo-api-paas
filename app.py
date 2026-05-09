import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///local.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route("/")
def home():
    return jsonify({
        "message": "Aplikasi To-Do List API berhasil berjalan",
        "description": "Aplikasi ini dibuat menggunakan Flask dan dideploy ke Railway",
        "endpoints": [
            "GET /",
            "GET /health",
            "GET /init-db",
            "GET /tasks",
            "POST /tasks",
            "PUT /tasks/<id>",
            "DELETE /tasks/<id>"
        ]
    })


@app.route("/health")
def health_check():
    return jsonify({
        "status": "ok",
        "message": "Aplikasi berjalan dengan baik"
    })


@app.route("/init-db")
def init_db():
    try:
        db.create_all()
        return jsonify({
            "message": "Database berhasil diinisialisasi"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Database gagal diinisialisasi",
            "detail": str(e)
        }), 500


@app.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        tasks = Task.query.all()
        result = []

        for task in tasks:
            result.append({
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            })

        return jsonify({
            "total": len(result),
            "tasks": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Gagal mengambil data task",
            "detail": str(e)
        }), 500


@app.route("/tasks", methods=["POST"])
def create_task():
    try:
        data = request.get_json()

        if not data or "title" not in data:
            return jsonify({
                "error": "Title wajib diisi"
            }), 400

        new_task = Task(title=data["title"])
        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            "message": "Task berhasil ditambahkan",
            "task": {
                "id": new_task.id,
                "title": new_task.title,
                "completed": new_task.completed
            }
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Gagal menambahkan task",
            "detail": str(e)
        }), 500


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        task = Task.query.get(task_id)

        if not task:
            return jsonify({
                "error": "Task tidak ditemukan"
            }), 404

        data = request.get_json()

        if "title" in data:
            task.title = data["title"]

        if "completed" in data:
            task.completed = data["completed"]

        db.session.commit()

        return jsonify({
            "message": "Task berhasil diperbarui",
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Gagal memperbarui task",
            "detail": str(e)
        }), 500


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)

        if not task:
            return jsonify({
                "error": "Task tidak ditemukan"
            }), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "message": "Task berhasil dihapus"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Gagal menghapus task",
            "detail": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
