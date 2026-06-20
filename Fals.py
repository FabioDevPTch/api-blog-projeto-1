# Criação da API Autor

from flask import Flask, jsonify, request, make_response
from estrutura_banco_de_dados import Postagem, Autor, app, db
import json
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps

#-------------------------------------------------------------------------------

# Token
def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-acess-token' in request.headers:
            token = request.headers['x-acess-token']
        if not token:
            return jsonify({'mensagem': 'Token não foi incluído.'}, 401)
        try:
            resultado = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            autor = Autor.query.filter_by(id_autor = resultado['id_autor']).first()
        except:
            return jsonify({'Mensagem': 'Token é inválido'}, 401)
        return f(autor, *args, **kwargs)
    return decorated
        
#-------------------------------------------------------------------------------

# Rota login:
@app.route('/login')
def login():
   dados_login = request.authorization
   if not dados_login or not dados_login.username or not dados_login.password:
       return make_response('Login Inválido', 401, {'WWW-Authenticate': 'Basic realm = "Login Obrigatório"'})
   usuario = Autor.query.filter_by(nome = dados_login.username).first()
   if not usuario:
       return make_response('Login Inválido', 401, {'WWW-Authenticate': 'Basic realm = "Login Obrigatório"'})
   if dados_login.password == usuario.senha:
       token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.now(timezone.utc) + timedelta(minutes = 30)}, app.config['SECRET_KEY'])
       return jsonify({'token': token})
   return make_response('Login Inválido', 401, {'WWW-Authenticate': 'Basic realm = "Login Obrigatório"'})

#-------------------------------------------------------------------------------

@app.route('/autores')
@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all()
    lista_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome'] = autor.nome
        lista_autores.append(autor_atual)
    return jsonify({'autores': lista_autores})

#-------------------------------------------------------------------------------

@app.route('/autores/<int:id_autor>', methods = ['GET'])
@token_obrigatorio
def obter_id_autor(autor, id_autor):
    autor = Autor.query.filter_by(id_autor = id_autor).first()
    if not autor:
        return jsonify(f'Autor não encontrado')
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome'] = autor.nome
    autor_atual['email'] = autor.email



    return jsonify({'autor': autor_atual})

#-------------------------------------------------------------------------------

@app.route('/autores', methods = ['POST'])
@token_obrigatorio
def adicionar_autor(autor):
    novo_autor = request.get_json()
   
    autor = Autor(nome=novo_autor['nome'], senha=novo_autor['senha'], email=novo_autor['email']) 

    db.session.add(autor)
 
    db.session.commit()

    return jsonify({'mensagem': 'Usuário criado com sucesso'}, 200)

#-------------------------------------------------------------------------------

@app.route('/autores/<int:id_autor>', methods = ['PUT'])
@token_obrigatorio
def alterar_autor(autor, id_autor):
   
    alterar_usuario = request.get_json()
   
    autor = Autor.query.filter_by(id_autor = id_autor).first()

    if not autor: # ou if autor == None: // --> 
        return jsonify({'Mensagem': 'Este usuário não foi encontrado.'})
    
    try:
        autor.nome = alterar_usuario['nome']
    except:
        pass
    try:
        autor.email = alterar_usuario['email']
    except:
        pass
    try:
        autor.senha = alterar_usuario['senha']
    except:
        pass

    db.session.commit()

    return jsonify({'Mensagem': 'Usuário alterado com sucesso !'}, 200)         

#-------------------------------------------------------------------------------

@app.route('/autores/<int:id_autor>', methods = ['DELETE'])
@token_obrigatorio
def deletar_autor(autor, id_autor):
   autor_existente = Autor.query.filter_by(id_autor = id_autor).first()
   
   if not autor_existente:
        return jsonify({'Mensagem': 'Autor não encontrado.'})
   
   db.session.delete(autor_existente)
   db.session.commit()

   return jsonify({'Mensagem': 'Autor excluído com sucesso !'})

#-------------------------------------------------------------------------------

# Criação da API Postagem:

@app.route('/postagens', methods = ['GET'])
@token_obrigatorio
def obter_postagens(autor):
    postagens = Postagem.query.all()

    list_postagens = []
    for postagem in postagens:
        postagem_atual = {}
        postagem_atual['titulo'] = postagem.titulo
        postagem_atual['id_autor'] = postagem.id_autor
        list_postagens.append(postagem_atual)
    return jsonify({'postagens': list_postagens})

#-------------------------------------------------------------------------------

@app.route('/postagens', methods = ['POST'])
@token_obrigatorio
def nova_postagem(autor):
    nova_postagem = request.get_json()
    postagem = Postagem(
        titulo=nova_postagem['titulo'], id_autor=nova_postagem['id_autor'])

    db.session.add(postagem)
    db.session.commit()

    return jsonify({'mensagem': 'Postagem criada com sucesso'})

#-------------------------------------------------------------------------------

@app.route('/postagens/<int:id_postagem>', methods = ['PUT'])
@token_obrigatorio
def alterar_postagem(autor, id_postagem):
    postagem_alterada = request.get_json()
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    try:
        postagem.titulo = postagem_alterada['titulo']
    except:
        pass
    try:
        postagem.id_autor = postagem_alterada['id_autor']
    except:
        pass

    db.session.commit()
    return jsonify({'mensagem': 'Postagem alterada com sucessso'})

#-------------------------------------------------------------------------------

@app.route('/postagens/<int:id_postagem>', methods = ['DELETE'])
@token_obrigatorio
def excluir_postagem(autor, id_postagem):
    postagem_a_ser_excluida = Postagem.query.filter_by(
        id_postagem=id_postagem).first()
    if not postagem_a_ser_excluida:
        return jsonify({'mensagem': 'Não foi encontrado uma postagem com este id'})
    db.session.delete(postagem_a_ser_excluida)
    db.session.commit()

    return jsonify({'mensagem': 'Postagem excluída com sucesso!'})

#-------------------------------------------------------------------------------

app.run(port = 5000, host = 'localhost', debug = True) 

#-------------------------------------------------------------------------------

