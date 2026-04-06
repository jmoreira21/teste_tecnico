# teste_tecnico
João Pedro Medeiros

Parte 1:


  Questão 1:
  Primeiramente, uma lista chamada "numeros" é criada com os valores de 1 a 6. A seguir, uma lista vazia "resultados" que irá armazenar o resultado. O for percorre cada   valor "n" na lista "numeros" e, se o número n for par ( resto da divisão de n por 2 for 0), é adicionado o dobro de n na lista "resultados". O print final sera        [4,8,12]

  
  Questão 2:
  A função esta correta. Ela soma dois numeros, sendo que "b" é um parâmetro com valor padrão de 10. Ela retornará, respectivamente, 15, 8, 6.

Parte 2:
  a) SELECT DISTINCT c.nome
    FROM clientes c
    INNER JOIN pedidos p ON c.id = p.cliente_id
    WHERE c.ativo = TRUE AND p.status = 'pago'
    ORDER BY c.nome;

  b) SELECT c.cidade, SUM(p.valor) AS total_gasto
    FROM clientes c
    INNER JOIN pedidos p ON c.id = p.cliente_id
    WHERE p.status = 'pago'
    GROUP BY c.cidade
    ORDER BY total_gasto DESC;

  c) SELECT c.id, c.nome
    FROM clientes c
    LEFT JOIN pedidos p ON c.id = p.cliente_id
    WHERE p.id IS NULL
    ORDER BY c.nome;
  
  
