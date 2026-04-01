from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


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
class FormaPagamento:
    nome: str
    exige_confirmacao: bool
    id_forma_pagamento: Optional[int] = None


@dataclass
class Compra:
    cliente_id: int
    vendedor_id: int
    forma_pagamento_id: int
    status_confirmacao: str = "dispensado"
    subtotal: Decimal = Decimal("0.00")
    percentual_desconto: Decimal = Decimal("0.00")
    valor_desconto: Decimal = Decimal("0.00")
    total: Decimal = Decimal("0.00")
    observacao: Optional[str] = None
    id_compra: Optional[int] = None


@dataclass
class ItemCompra:
    compra_id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    total_item: Decimal
    id_item: Optional[int] = None
