#-------------------------------------------------------------------------------

# Flask --> É um framework que nos permite criar API's.
# Framework --> É uma estrutura pronta que nos disponibiliza ferramentas e organização para facilitar o desenvolvimento
# de aplicações.

# Para começar a usufruir dessa ferramenta, primeiramente, devemos importar tais funcionalidades:

# jsonify --> Serve para converter dados/objetos Python em JSON e esses dados são enviados para o cliente/pessoa que acessar.

# request --> Serve para solicitar alguma informação da API.

from flask import Flask, jsonify, request, make_response

# Passo a passo:

'''
# 1- Definir o objetivo da API:
   ex: Iremos montar uma api de blog, onde eu poderei consultar, editar, criar e excluir postagens em
   um blog usando a API

2- Qual será o URL base do api?
    ex: Quando você cria uma aplicação local ela terá um url tipo http://localhost:5000/, porém quando
    você for subir isso para nuvem, você terá que comprar ou usar um dominio como url base, vamos
    imaginar um exemplo de devaprender.com/api/

3 - Quais são os endpoints?
    ex: Se seu requisito é de poder consultar, editar, criar e excluir, você terá que disponibilizar
    os endpoints para essas questões
        >/postagens/

4 - Quais recursos serão disponibilizados pelo API: informação sobre postagens

5 - Quais verbos http serão disponibilizados?

GET

POST

PUT

DELETE

6 - Quais são os URL completos para cada um?
http://localhost:5000/postagens
'''

#-------------------------------------------------------------------------------

# Para iniciar uma aplicação/servidor/site Flask faremos o seguinte:

from estrutura_banco_de_dados import Postagem, Autor, app, db, inicializar_banco

# app = Flask(__name__) # --> Este __name__ diz que criará um aplicativo com o nome que está sendo utilizado no nosso arquivo, que no caso é Fals.py.
# (Não usaremos esse, pois já importamos do nosso modulo estrutura_banco_de_dados)

# postagens = [
#     {
#         'titulo': 'Minha aplicação',
#         'autor': 'Fabio',
#     },
#     {
#         'titulo': 'Frango',
#         'autor': 'Fabin',
#     },
#     {
#         'titulo': 'Arroz',
#         'autor': 'Fabão'
#     }
# ]

# Rota padrão
# @app.route('/') # --> / quer dizer que estamos na rota padrão
# def obter_postagens():
#     return jsonify(postagens)

# # GET com ID

# # Para que possamos obter alguma informação baseada no indice ou algum outro parâmetro, devemos passa-lo no app.route, que é a rota/caminho que irá percorrer
# # para encontrar a informação desejada.

# @app.route('/postagens/<int:indice>', methods = ['GET']) # --> Na rota, definiremos o caminho que, nesse caso, é postagens(variavel que carrega a lista de dicionários) adicionar uma /, colocar
# def obter_postagens_indice(indice):                      # <> e dentro dele especificar que o indice que será passado vai ser convertido no tipo inteiro: <int:indice> -> Importante sempre colocar junto.
#     return jsonify(postagens[indice])                    # Após isso, para obtermos a informação desejada, basta adicionar "methods = ['GET']", mostrando que queremos obter informação da nossa API.
# #               ⬆️
# # Definiremos uma função que leva um parâmetro/variavel com o mesmo nome que definimos na rota, que é "indice", e retornaremos sempre convertendo com o jsonify(variavel[indice]).

# # Obs.: /postagens/<int:indice>   # "indice" é uma variavel da URL e serve para capturar o número da URL
# #             postagens[indice]   # usa esse número para acessar a lista

# #-------------------------------------------------------------------------------

# # Criar uma postagem - POST com ID

# @app.route('/postagens', methods = ['POST']) # --> Na rota "/postagens" quero dizer que quando solicitarem/requisitarem algo em /postagens, executar as funções abaixo:
# def nova_postagem():

#     postagem = request.get_json() # --> request é o que o cliente(que sou eu) solicitou na requisição e o get_json pega o JSON enviado e transforma/converte em um objeto Python para que eu consiga adicionar a
#                                   # minha variavel "postagens" dentro do Python.

#     postagens.append(postagem) # --> estou adicionando algo através do .append (sempre ao final da lista).

#     return jsonify(postagens), 200 # --> retornarei e converterei o que está armazenado na variavel "postagens" para JSON.

# #-------------------------------------------------------------------------------

# # Alterar informação existente - PUT

# @app.route('/postagens/<int:indice>', methods = ['PUT']) # --> <int:indice> significa que o numero passado será inteiro e será armazenado na viravel indice.
# def alterar_postagem(indice): # --> Coloco a variável indice para que nela seja armazenado o número inteiro e para que façamos alguma operação.
#     postagem_alterada = request.get_json() # --> request é a requisição que o cliente faz e o get_json pega essa requisição e converte em objeto python
#                                            # para que possamos usa-lo normalmente dentro do nosso interpretador de código(VsCode)
#     postagens[indice].update(postagem_alterada) # -->  Na variavel postagens com base no indice que iremos passar, atualize os dados com base no que foi armazenado
#                                                 # na variavel postagem_alterada

#     # Obs.: postagens é como a estante de livros inteiras. Já postagens[indice] é como um livro especifico. Como queremos alterar só um ou dois elementos, então
#     # precisaremos utilizar [indice]

#     return jsonify(postagens[indice]), 200 # --> retorna a conversão da variavel postagens em JSON.

# #-------------------------------------------------------------------------------

# # Excluir uma informação/recurso existente - DELETE

# @app.route('/postagens/<int:indice>', methods = ['DELETE'])
# def deletar_recurso(indice):
#    try:
#     if postagens[indice] is not None:
#         del postagens[indice]
#         return jsonify(f'Foi excluído a postagem com índice: {postagens[indice]}'), 200
#    except:
#         return jsonify('Não foi possível encontrar uma postagem com o índice solicitado'), 404

#-------------------------------------------------------------------------------

# Criação da API Autor

# from flask import Flask, jsonify, request, make_response

# from estrutura_banco_de_dados import Postagem, Autor, app, db
import json
import jwt # → biblioteca para criar e validar tokens.
from datetime import datetime, timedelta, timezone
from functools import wraps

def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # verificar se um token foi enviado
        if 'x-acess-token' in request.headers: # --> "Se existir um header(cabeçalho) chamado 'x-acess-token' dentro dos headers da requisição, execute o bloco abaixo."
            token = request.headers['x-acess-token'] # --> "Pegue o valor associado à chave 'x-acess-token' e armazene-o na variável token."
            # request.headers → usado para acessar qualquer cabeçalho enviado na requisição, incluindo tokens JWT.
        if not token: # --> Significados: "Se não existir/tiver um token/valor...", "Se o(a) token/variavel estiver vazio(a)...", "Se o token/valor for falso..."
            return jsonify({'mensagem': 'Token não foi incluído.'}, 401)
        # Se temos um token, validar consultando o banco de dados.
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
   dados_login = request.authorization # --> Será utilizado para pegar a autenticação/credenciais necessárias de usuário e senha do cliente para acessar determinada rota.
   if not dados_login or not dados_login.username or not dados_login.password:
       return make_response('Login Inválido', 401, {'WWW-Authenticate': 'Basic realm = "Login Obrigatório"'})
   usuario = Autor.query.filter_by(nome = dados_login.username).first() # --> Para verificar se o usuario e senha existe no nosso banco de dados.
   if not usuario: # --> Verifica se o resultado foi: None/Nenhum. Por que usar: Para impedir login de usuários inexistentes.
       return make_response('Login Inválido', 401, {'WWW-Authenticate': 'Basic realm = "Login Obrigatório"'})
   if dados_login.password == usuario.senha: # --> Vai comparar se a senha digitada na autenticação/login é a mesma do banco de dados. Diz: se a senha do login for a mesma do banco de dados, execute:
       token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.now(timezone.utc) + timedelta(minutes = 30)}, app.config['SECRET_KEY'])
       return jsonify({'token': token})
   return make_response('Login Inválido', 401, {'WWW-Authenticate': 'Basic realm = "Login Obrigatório"'})

# A variável "usuario" recebe todos os registros/colunas e seus dados que definimos da tabela autor, como:

# id_autor	  nome	      email	           senha
#    1	      Fabio	  fabio@gmail.com	   12345

#-------------------------------------------------------------------------------

# <jwt.encode gera um token aleatório e o decode valida o token.>

# token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.now(timezone.utc) + timedelta(minutes = 30)}, app.config['SECRET_KEY'])

# Significado geral: "Crie um JWT contendo o ID do autor e uma data de expiração de 30 minutos a partir de agora, assine esse token usando a chave secreta da aplicação e armazene o resultado na 
# variável token."

# Parte por parte:

# 'id_autor': usuario.id_autor --> Crie uma chave 'id_autor' que receberá o valor de usuario.id_autor

# 'exp': datetime.now(timezone.utc) + timedelta(minutes = 30) --> Me retorna a data e hora atual(datetime.now) com horario universal(timezone.utc). Define quanto tempo o token irá ser válido/funcionar, 
# que é 30 minutos.

# app.config['SECRET_KEY'] --> Usado para carimbar/assinar o token. Fazendo assim, com que não possa alterar o id_autor livremente e finja ser outro usuário.

#-------------------------------------------------------------------------------

# Sobre o filter_by:

# Autor.query --> query irá consultar todos os registros da tabela Autor.

# Ex.:

# id_autor	nome
# 1	        Fabio
# 2	        Maria
# 3	        João

# filter --> Filtra/elimina o que não queremos e nos retorna o desejado, que é Fábio, por exemplo.

# Por que chama "filtrar"?

# Porque estamos pegando um conjunto grande de registros e eliminando os que não atendem à condição.

# O first() pega a primeira ficha encontrada.

#-------------------------------------------------------------------------------

# make_response --> é uma resposta HTTP personalizada que enviaremos ao cliente informando uma mensagem, status code e enviando informação ao navegador.

# Sobre o terceiro argumento do make_response: {'WWW-Authenticate': 'Basic realm = "Login Obrigatório"'}

# Cabeçalho HTTP: WWW-Authenticate

# Informa ao navegador que é necessária autenticação Basic. O Basic significa: "Esta rota espera autenticação Basic (usuário e senha)."
                                                                               # O realm é apenas uma descrição da área protegida.
                                                                         
# O navegador entende:

# "Esta página exige autenticação Basic. Vou pedir usuário e senha ao usuário."

# Por que usar?

# Para avisar ao cliente que ele precisa fornecer usuário e senha válidos.

#-------------------------------------------------------------------------------

@app.route('/autores') # --> Usuário acessa o EndPoint 'autores'
@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all() # --> Da classe autor, consulte(selecione) todos os registros e armazene na variavel "autores"
    lista_autores = [] # --> Lista vazia ao qual iremos adicionar o(s) dicionário(s) de autores.
    for autor in autores: # --> Para acessar cada autor dentro de autores:
        autor_atual = {} # --> Criando um dicionário para armazenar um autor com id, nome e email.
        autor_atual['id_autor'] = autor.id_autor # --> esse ['id_autor'] significa a chave do dicionário. 'autor.id_autor' é acessando o atributo da classe: é como se eu estivesse falando 'self.id_autor' acessado fora da classe
        autor_atual['nome'] = autor.nome # --> esse ['nome'] significa a chave do dicionário. 'autor.nome' é acessando o atributo da classe: é como se eu estivesse falando 'self.nome' acessado fora da classe
        autor_atual['email'] = autor.email # --> esse ['email'] significa a chave do dicionário. 'autor.email' é acessando o atributo da classe: é como se eu estivesse falando 'self.email' acessado fora da classe
        lista_autores.append(autor_atual) # --> Pega tudo o que foi armazenado em "autor_atual" e adiciona na lista chamada "lista_autores" e dando origem à uma lista de dicionario ou dicionarios.

    return jsonify({'autores': lista_autores}) # --> Vai criar uma chave chamada "autores" que armazena a lista de dicionários vindas da lista_autores e converte em JSON.

#-------------------------------------------------------------------------------

@app.route('/autores/<int:id_autor>', methods = ['GET'])
# <int> diz que a URL(caminho) espera um número inteiro e 'id_autor' será a variavel que armazenará o valor passado.
@token_obrigatorio
def obter_id_autor(autor, id_autor):
    autor = Autor.query.filter_by(id_autor = id_autor).first() # --> Consulte na tabela Autor, filtre os registros cuja coluna id_autor seja igual ao índice passado na rota seja o mesmo e me retorne o primeiro registro encontrado.
    # filter_by(id_autor(atributo/coluna da classe) = id_autor(variavel que armazena a rota da URL[link]))
    if not autor: # --> Se autor não tiver valor, retorne:
        return jsonify(f'Autor não encontrado')
    autor_atual = {} # --> Criando um dicionário para armazenar um autor com id, nome e email.
    autor_atual['id_autor'] = autor.id_autor # --> Cria uma chave "id_autor" que armazena o que for passado como valor do atributo do objeto autor, que carrega os atributos da classe.
    autor_atual['nome'] = autor.nome # --> Cria uma chave "nome" que armazena o que for passado como valor do atributo do objeto autor, que carrega os atributos da classe.
    autor_atual['email'] = autor.email # --> Cria uma chave "email" que armazena o que for passado como valor do atributo do objeto autor, que carrega os atributos da classe.

    # return jsonify(f'Você buscou o autor: {autor_atual}') # --> Resultado: "Você buscou o autor: {'id_autor': 1, 'nome': 'Fabio', 'email': 'fabio@gmail.com'}"

    # Caso eu queira retornar um dicionário, basta fazermos assim:

    return jsonify({'autor': autor_atual}) # --> Resultado: {
                                                            #   "autor": {
                                                            #         "email": "fabio@gmail.com",
                                                            #         "id_autor": 1,
                                                            #         "nome": "Fabio"
                                                            #     }
                                                            # }

#-------------------------------------------------------------------------------

@app.route('/autores', methods = ['POST'])
@token_obrigatorio
def adicionar_autor(autor):
    novo_autor = request.get_json() # --> Pega a requisição do cliente em JSON e converte em objeto Python(dicionário) # {
                                                                                                                        #     'nome': 'Fabio',
                                                                                                                        #     'senha': '12345',
                                                                                                                        #     'email': 'fabio@gmail.com'
                                                                                                                        # }
                    
    autor = Autor(nome=novo_autor['nome'], senha=novo_autor['senha'], email=novo_autor['email']) # --> nome, senha e email da esquerda são os atributos da classe Autor ao qual receberão os valores
                                                                                                 # armazenados na variavel "novo_autor". Os da direita são as chaves do dicionário.      

# Podemos ler: "Crie um objeto Autor e preencha o atributo nome com o valor da chave 'nome' do dicionário novo_autor, o atributo senha com o valor da chave 'senha' e o atributo email com o valor da chave 'email'.
# Depois, armazene esse objeto na variável autor."

    db.session.add(autor) # -->"Eu quero inserir esse autor no banco."
                                # Mas ele ainda não executa o INSERT.
 
    db.session.commit() # --> Confirma as alterações no banco.
                            # Executará o insert(vai colocar no banco de dados)

    return jsonify({'mensagem': 'Usuário criado com sucesso'}, 200) # --> Cria uma chave que exibirá essa mensagem.

#-------------------------------------------------------------------------------

@app.route('/autores/<int:id_autor>', methods = ['PUT'])
# Preciso passar obrigatoriamente um número inteiro <int:id_autor> pois quero saber QUAL será alterado.
@token_obrigatorio
def alterar_autor(autor, id_autor): # --> variável da URL que receberá o valor
   
    alterar_usuario = request.get_json() # --> Irá pegar a requisição em JSON, converterá para objeto python(dicionário) e armazenará da variavel que chamei de "alterar_usuario"
   
    autor = Autor.query.filter_by(id_autor = id_autor).first() # --> Consulte na tabela Autor, filtre os registros cuja coluna id_autor seja igual ao índice passado na rota seja o mesmo e me retorne o primeiro registro encontrado.
    # filter_by(id_autor(atributo/coluna da classe) = id_autor(variavel que armazena a rota da URL[link])).//\\ Ou podemos dizer da definição acima: procure um autor com o mesmo id passado na rota. 
    
    # .first(): # --> é obrigatorio usar para que retorne o valor solicitado.
    # "Execute a consulta e me devolva o primeiro resultado encontrado."

    if not autor: # ou if autor == None: // --> 
        return jsonify({'Mensagem': 'Este usuário não foi encontrado.'})
    
    # Por que usar try?

    # Porque talvez o JSON não tenha a chave "nome". Isso evita/impede que a aplicação quebre/pare de rodar.
    
    try:
        autor.nome = alterar_usuario['nome'] # --> Atributo "nome" da classe receberá o valor da chave 'nome' que está armazenado na variavel "alterar_usuario"
    except:
        pass
    try:
        autor.email = alterar_usuario['email'] # --> Atributo "email" da classe receberá o valor da chave 'email' que está armazenado na variavel "alterar_usuario"
    except:
        pass
    try:
        autor.senha = alterar_usuario['senha'] # --> Atributo "senha" da classe receberá o valor da chave 'senha' que está armazenado na variavel "alterar_usuario"
    except:
        pass

    db.session.commit() # --> Salva permanentemente a alteração.

    return jsonify({'Mensagem': 'Usuário alterado com sucesso !'}, 200)         

#-------------------------------------------------------------------------------

@app.route('/autores/<int:id_autor>', methods = ['DELETE'])
@token_obrigatorio
def deletar_autor(autor, id_autor):
   autor_existente = Autor.query.filter_by(id_autor = id_autor).first() # --> Na tabela autor, consulte os registros, filtre-os cuja coluna id_autor seja a mesma do id passado na rota(URL) e me retorne o primeiro
                                                                                                                                                                                                  # valor encontrado
   if not autor_existente: # --> Se "autor_existente" não tiver valor, execute:
        return jsonify({'Mensagem': 'Autor não encontrado.'})
   
   db.session.delete(autor_existente) # --> Quero apagar o autor encontrado.
   db.session.commit() # Salva o apagamento do autor.

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

app.run(port = 5000, host = 'localhost', debug = True) # --> "Inicie o servidor Flask na porta 5000, permitindo acesso apenas pelo meu computador e ativando o modo de desenvolvimento."

# OBS. GERAL: Toda rota Flask precisa estar associada a uma função.

# debug --> Ativa recursos de desenvolvimento e exibe erros detalhados.

# Com debug=True, o navegador exibe uma página detalhada mostrando:

# O erro ocorrido.
# Em qual arquivo.
# Em qual linha.

#-------------------------------------------------------------------------------

# Para não dar erro na hora de tentar acessar uma rota, primeiramente colocaremos o login e a senha em localhost/5000/login, copiar o token gerado, ir em headers no postman, vai em key e coloca -> x-acess-token
# e depois coloca o token gerado ao lado.

# HTTP (sigla para Hypertext Transfer Protocol, ou Protocolo de Transferência de Hipertexto) é o protocolo fundamental da internet. É um conjunto de regras que 
# permite que o seu navegador (cliente) se comunique com o servidor onde um site está hospedado, solicitando e recebendo as páginas web que você deseja visualizar
