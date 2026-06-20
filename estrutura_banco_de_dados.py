

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abcdefgh123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)

db:SQLAlchemy

class Postagem(db.Model):  
    __tablename__ = 'postagens'

    id_postagem = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer, db.ForeignKey('autor.id_autor'))
        
class Autor(db.Model):
    __tablename__ = 'autor'
    
    id_autor = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship(Postagem)




def inicializar_banco():
    with app.app_context():
        db.drop_all()
        db.create_all()
        autor = Autor(nome = 'Fabio', email = 'fabio@gmail.com', senha = '12345', admin = True)
        db.session.add(autor)
        db.session.commit()
        print('As tabelas foram criadas !')

inicializar_banco()


































