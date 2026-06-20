#-------------------------------------------------------------------------------

# SQLALCHEMY --> SQLAlchemy é uma biblioteca Python usada para trabalhar com bancos de dados relacionais de forma mais fácil e organizada. 
# Ela oferece duas abordagens principais:

# 1 - SQL Expression Language: permite construir consultas SQL usando Python.
# 2 - ORM (Object-Relational Mapping): permite mapear tabelas do banco para classes Python.

# Podemos dizer:

# SQL Expression Language: usar Python para construir comandos SQL de forma programática.
        # SQL puro:

        # SELECT * FROM usuarios WHERE nome = 'Fabio';

        # SQLAlchemy Expression Language:

        # from sqlalchemy import select

        # consulta = select(Usuario).where(Usuario.nome == 'Fabio')

# ORM: usar classes e objetos Python para representar tabelas e registros do banco de dados, deixando o SQLAlchemy gerar o SQL automaticamente.

#-------------------------------------------------------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Passos a passo:

# Criar um API Flask
app = Flask(__name__)
# Criar uma instância de SQLAlchemy

app.config['SECRET_KEY'] = 'abcdefgh123' # --> É um acesso de autenticação único que vai funcionar somente na minha aplicação. Ou seja, uma senha.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' # --> Aqui definiremos onde está localizado nosso banco de dados. Como estamos instanciando localmente.
                        # Não esquecer de colocar 3 barras. Caso estivessemos conectando a um banco de dados online, estariamos passando a referência dele.

        # O SQLAlchemy usa uma URI porque ela não serve apenas para apontar para um site; ela descreve como conectar ao banco.

        # O arquivo que estamos abrindo não é um site.

        # É uma instrução dizendo:

        # usar o banco SQLite
        # abrir o arquivo blog.db

db = SQLAlchemy(app) # --> Passamos como parâmetro a aplicação flask que criamos acima.
# db se torna uma instância(objeto) que guarda todas as ferramentas do SQLAlchemy. Para entender melhor: uma instancia ou objeto é algo criado a partir de uma classe.

db:SQLAlchemy # --> Estou dizendo que essa instância será do tipo SQLAlchemy. Isso faz com que não surja erros durante o uso.

# Como me conectar a um banco de dados especifico?

# Pesquisar no Google: connection string oracle, connection string sql server ou connection "nome do banco de dados" (especificando)

# Definir a estrutura da tabela Postagem

# Toda postagem tem um AUTOR, um TITULO e um ID de POSTAGEM.
class Postagem(db.Model): # --> Usamos o db(onde guardamos as ferramentas do SQLAlchemy).Model(uma classe do SQLAlchemy) porque estamos herdando da classe Model para estruturar.   
    # Estrutura:
    # Para definir o nome de uma table(tabela), chamaremos a propriedade __tablename__ (propriedade, porque é um atributo de classe)
    __tablename__ = 'postagens'
    # Cada variável é o nome da coluna que será criada no banco de dados: id_postagem, titulo e autor.
    id_postagem = db.Column(db.Integer, primary_key = True) # --> Faz com que essa coluna se torne o principal identificador(identifica de forma única) cada registro do meu banco de dados.
    titulo = db.Column(db.String)
    # Para relacionar uma coluna de outra tabela, podemos usar uma chave estrangeira ForeignKey para identificar algo de nosso desejo.
    id_autor = db.Column(db.Integer, db.ForeignKey('autor.id_autor')) # --> Passar o nome da tabela e a coluna.

# Definir a estrutura da tabela Autor
# Todo autor tem id do autor, nome, email, senha, admin, postagens
class Autor(db.Model):
    __tablename__ = 'autor'
    
    id_autor = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship(Postagem) # --> Nome da CLASSE

# Executar o comando para criar o banco de dados:

# Para começar a interação com o banco de dados, precisamos colocar antes: with app.app_context(): e indentar todo o bloco de código dentro dessa linha de código.

def inicializar_banco():
    with app.app_context():
        db.drop_all() # --> Apaga todas as tabelas existentes
        db.create_all() # --> Cria tabelas novas
        # Criar usuário Administradores
        autor = Autor(nome = 'Fabio', email = 'fabio@gmail.com', senha = '12345', admin = True)
        db.session.add(autor) # --> session é o gerenciador de alteração
        db.session.commit() # --> gerenciando e salvando.
        print('As tabelas foram criadas !')

inicializar_banco()

# if __name__ == '__main__': # --> Significa que a função só será executada aqui neste arquivo. Name se refere ao meu arquivo "estrutura_banco_de_dados.py" e o Main diz que ele é o principal.
#     inicializar_banco()


































