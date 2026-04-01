from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from datetime import datetime

@dataclass
class Produto:
    nome: str
    artista: str
    categoria: str
    ano_fabricacao: int
    fabricado_em_mari: bool
    preco: Decimal
    estoque: int
    id_produto: Optional[int] = None


@dataclass
class Cliente:
    nome: str
    email: str
    telefone: str
    cidade: str
    time_futebol: str
    anime_favorito: str
    id_cliente: Optional[int] = None


@dataclass
class Vendedor:
    nome: str
    email: str
    ativo: bool = True
    id_vendedor: Optional[int] = None

@dataclass
class Pedido:
    cliente_id: int
    vendedor_id: int
    forma_pagamento_id: int
    produto_id: int
    quantidade: int
    subtotal: Optional[Decimal] = None
    desconto: Optional[Decimal] = None
    total: Optional[Decimal] = None
    status: Optional[str] = None
    data: Optional[datetime] = None
