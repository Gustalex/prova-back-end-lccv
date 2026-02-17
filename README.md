## CONFIGURAÇÃO DE AMBIENTE

### Configurar o  **.env**
- O  arquivo .env.example já está disponibilizado no código e basta passar a configurção do banco postgres nos respectivos campos


### Introdução sobre o Makefile

- O projeto dispõe de um Makefile que facilita o desenvolvimento existindo 3 comandos :
    - make build (builda o projeto subindo os containers docker da api e do banco)
    - make run (roda os containers)
    - make console (permite a execução de comando do python dentro do container)
    - make hard-rebuild (faz uma limpeza profunda do docker e rebuilda o projeto)

## COMO RODAR O PROJETO
### Com o .env já configurado 
- **Buildar o projeto** 
  ```
  make build
  ```
- **A documentação dos endpoints está disponível no swagger via url:** 

  ```
  http://localhost:8000/swagger
  ```

- **Para acessar os fomulários disponíveis no django admin:** 
    - Entrar no container para executar os comandos
      ```
      make console
      ```
    - Criar o super usuário
      ```
      ./manage.py createsuperuser
      ```
    - Fazer o login com as credenciais cadastradas e testar via formulários
    - É possivel Gerenciar Colaboradores, Avaliações e modelos relacionados
    - É possivel fazer alterações em ItemAvaliacaoDesempenho dentro da página do modelo de AvaliacaoDesempenho através dos fomularios inline
    - A testagem da mudança de status via django admin pode ser efetuada a partir do select de actions na pagina de gerenciamento de Avaliações de desempenho



