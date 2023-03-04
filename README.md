# Como rodar o projeto na máquina

Para rodar o projeto, é necessário instalar o linux na máquina, pois utilizei uma biblioteca (RedisJSON) na qual não encontrei instalação para o Windows. Se você usa Windows, basta instalar o WSL2 que instala um subsistema linux no Windows seguindo o tutorial: https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview

## Instalação do MYSQL

Depois é necessário instalar o MYSQL:

`sudo apt update`

`sudo apt install mysql-server`

Para iniciar o MYSQL:

`sudo /etc/init.d/mysql start`

Primeiro vamos setar a senha do usuário root:

`sudo mysql -u root`

Agora rode a seguinte query para setar uma senha (por exemplo, admin123):

`ALTER USER 'root'@'localhost' IDENTIFIED BY 'admin123';`

Agora entre como usuário root utilizando sua senha:

`sudo mysql -u root -p`

Crie um usuário chamado local_user, dê os privilégios e crie o banco de dados:

`CREATE USER 'local_user'@'localhost' IDENTIFIED BY 'admin123';`

`GRANT ALL PRIVILEGES ON * . * TO 'local_user'@'localhost';`

`CREATE DATABASE casa_leite;`


## Crie um ambiente virtual

Após isso, clone o repositório e crie um ambiente virtual utilizando os comandos:

`python3 -m venv venv`

`source venv/bin/activate`

Agora instale a biblioteca libmysqlclient-dev:

`sudo apt-get install libmysqlclient-dev`

Instale as dependências:

`pip install -r requirements.txt`

## Instale o Redis JSON

`sudo add-apt-repository ppa:redislabs/redis`

`sudo apt-get update`

`sudo apt-get install redis`

`sudo apt-get install -y clang`

Clone o seguinte repositório: https://github.com/RedisJSON/RedisJSON

Entre nele (por exemplo, cd RedisJSON) e rode:

`cargo build --release`

`sudo redis-server --loadmodule ./target/release/librejson.so`

## Conclusão

Sempre que for começar a mexer no projeto:

Rodar servidor MySQL:
- sudo /etc/init.d/mysql start

Rodar redis:
- cd RedisJSON
- sudo redis-server --loadmodule ./target/release/librejson.so

Entrar no ambiente virtual e rodar:

`flask run`
