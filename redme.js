graph LR
  %% процеси
  P1([P1])
  P2([P2])

  %% ресурси (круглі)
  R1((R1))
  R2((R2))

  %% P1 тримає R1 і просить R2
  P1 -- holds --> R1
  P1 -- requests --> R2

  %% P2 тримає R2 і просить R1
  P2 -- holds --> R2
  P2 -- requests --> R1

  classDef proc fill:#f9f,stroke:#333,stroke-width:1px;
  classDef res fill:#fffbcc,stroke:#333,stroke-width:1px;
  class P1,P2 proc;
  class R1,R2 res;

  %% підказка (не обов'язково для рендерера)
  subgraph NOTE[ ]
    direction TB
    note1[(«Цикл» P1 → R2 → P2 → R1 → P1 — це дедлок)]
  end
