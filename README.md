
# Documentação do Projeto "Study Async"

## Introdução
O "Study Async" é um projeto desenvolvido para auxiliar nos estudos, utilizando Python com o framework Django, HTML e CSS. A aplicação abrange três principais componentes: Flashcards, Apostilas e Usuários. Cada um desses elementos é organizado em apps individuais, concentrando-se em funcionalidades específicas para otimizar o processo de aprendizado.

## Estrutura do Projeto
### Apps do Projeto
1. **Usuarios:**

+ Responsável pela autenticação e controle de usuários do sistema.
+ Gerencia o modelo de usuário, estendendo o modelo padrão do Django.
2. **Flashcards:**

+ Lida com a criação, visualização e gerenciamento de flashcards.
+ Permite aos usuários criar e deletar flashcards, bem como iniciar desafios para testar conhecimentos.
3. **Apostilas:**

+ Gerencia o armazenamento de apostilas, visualizações e avaliações.
+ Registra visualizações associadas a endereços IP e coleta avaliações específicas para as apostilas.
## Funcionalidades Gerais
### Flashcards:
1. **Novo Flashcard:**

+ Permite aos usuários criar novos flashcards, fornecendo informações como pergunta, resposta, categoria e dificuldade.
2. **Deletar Flashcard:**

+ Usuários podem excluir flashcards previamente criados.
3. **Iniciar Desafio:**

+ Funcionalidade que permite aos usuários criar desafios, escolhendo categoria, dificuldade e quantidade de perguntas.
4. **Listar Desafio:**

+ Apresenta uma lista de desafios criados pelo usuário, exibindo informações sobre categoria, dificuldade e status.
5. **Responder Flashcard:**

+ Usuários podem responder aos flashcards durante um desafio, indicando se acertaram ou erraram.
6. **Relatório:**

+ Fornece estatísticas sobre o desempenho do usuário em desafios, incluindo acertos, erros e análises por categoria.
### Apostilas:
1. **Upload de Apostila:**

+ Permite aos usuários enviar apostilas, associando-as ao seu perfil.
2. **Visualizações:**

+ Registra visualizações de apostilas, rastreando o endereço IP do visualizador.
4. **Avaliações:**

+ Coleta avaliações para as apostilas, utilizando escolhas pré-definidas.
## Considerações Finais
O "Study Async" oferece uma plataforma abrangente para criar, gerenciar e testar conhecimentos por meio de flashcards e apostilas. A estrutura modular do projeto facilita a expansão e a adição de novas funcionalidades. Contribuições são bem-vindas através de pull requests e relatórios de problemas via issues.

Autor: Flauziino - Desenvolvedor

Para informações adicionais ou esclarecimentos, sinta-se à vontade para entrar em contato.