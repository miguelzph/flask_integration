# Integração plataforma de pagamentos

- Link da aplicação: <a href="https://hashtag-hotmart-api.onrender.com/" title="Clique e acesse agora!" target="_blank">Link no Render</a>
- O Readme será bem sucinto, apenas com algumas observações.
### Banco de dados
1. O banco de dados da tabela de usuários está em um sqlite. 
    - Por isso, quando a aplicação reiniciar novos usuário cadastrados serão perdidos.
2. Já os dados, da requisição e de ações tomadas por causa dessa requisição, estão em duas tabelas do DynamoDB (Banco de dados NoSQL da Amazon).
    - Com isso os dados serão mantidos.

### Página de ações
1. Novas ações podem demorar até 5 minutos para aparecer na página de ações.
    - A forma que consegui fazer paginação refazia a query de todos os valores a cada mudança de página.
    - Para evitar isso, coloquei a função em cache usando a lru_cache guardando no máximo 1 resultado, e usando o datetime com final de minutos como auxiliar (uma nova ação de até 5 minutos pode não aparecer, mas já foi inserida corretamente na tabela do DynamoDB. E aparecerá quando qualquer usuário entrar na página após os minutos com fim 0 ou 5).
    - A pesquisa realizada através da barra de pesquisa é uma query menor e mais eficiente, então ela não tem cache, e por isso não se aplica esse caso da ação existir na tabela, mas não aparecer no resultado.


  
