# GENERADO DESDE ESPECIFICACION. NO EDITAR A MANO.
# Capability: demanda
# Cambio de origen: e2-ciclo-vida-demanda
# Si algo esta mal aqui, esta mal en la spec. Corrige la spec y regenera.
"""Modelos del dominio de Abaco.

Sin dependencias externas: el nucleo se ejecuta y se testea sin levantar nada.

Nota de alcance deliberada: aqui NO hay coste de personal, ni centro de coste,
ni banda salarial, ni tarifa. Quedaron fuera al pasar la herramienta a datos
reales, porque la retribucion es el dato mas sensible del expediente de un
empleado y sacarlo elimina de golpe la mayor parte del riesgo. Su papel
estructural lo ocupa la categoria profesional.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional


class EstadoDemanda(str, Enum):
    SOLICITADA = "solicitada"
    APROBADA = "aprobada"
    BUSCANDO = "buscando"
    CANDIDATO_PROPUESTO = "candidato_propuesto"
    ACEPTADA = "aceptada"
    ASIGNADA = "asignada"
    CERRADA = "cerrada"
    CANCELADA = "cancelada"


class TipoDisponibilidad(str, Enum):
    DISPONIBLE = "disponible"
    ASIGNADO = "asignado"
    VACACIONES = "vacaciones"
    FORMACION = "formacion"
    FESTIVO = "festivo"
    BAJA = "baja"
    BANQUILLO = "banquillo"


class Modalidad(str, Enum):
    PORCENTUAL = "porcentual"
    HORARIA = "horaria"


@dataclass(frozen=True)
class Categoria:
    """Categoria profesional. Entidad configurable y versionada por vigencia.

    No es un enum en el codigo a proposito: el catalogo cambia con el tiempo y
    hay que saber que version aplicaba en cada momento.
    """
    codigo: str
    nombre: str
    orden_seniority: int
    utilizacion_objetivo: Decimal
    capacidad_facturable_esperada: Decimal
    vigente_desde: date
    vigente_hasta: Optional[date] = None

    def vigente_en(self, momento: date) -> bool:
        if momento < self.vigente_desde:
            return False
        return self.vigente_hasta is None or momento <= self.vigente_hasta

    def cumple(self, pedida: "Categoria") -> bool:
        """Una categoria cubre a otra si iguala o supera su orden de seniority."""
        return self.orden_seniority >= pedida.orden_seniority


@dataclass(frozen=True)
class CatalogoCategorias:
    version: str
    vigente_desde: date
    categorias: dict

    def categoria(self, codigo: str) -> Categoria:
        if codigo not in self.categorias:
            raise KeyError("categoria %s no existe en el catalogo %s"
                           % (codigo, self.version))
        return self.categorias[codigo]


@dataclass(frozen=True)
class Skill:
    codigo: str
    nivel: int          # 1 a 5
    ultimo_uso: Optional[date] = None


@dataclass(frozen=True)
class CategoriaVigencia:
    """Categoria de una persona durante un intervalo. Una promocion cierra la
    vigencia anterior y abre una nueva. Nunca se reescribe la anterior."""
    codigo_categoria: str
    desde: date
    hasta: Optional[date] = None

    def vigente_en(self, momento: date) -> bool:
        if momento < self.desde:
            return False
        return self.hasta is None or momento <= self.hasta


@dataclass
class Persona:
    persona_id: str
    nombre: str
    pais: str
    oficina: str
    fecha_alta: date
    fecha_baja: Optional[date] = None
    historico_categoria: list = field(default_factory=list)
    skills: list = field(default_factory=list)

    def categoria_en(self, momento: date) -> Optional[str]:
        """SPEC-001/CA-05: la categoria de una persona en un momento dado.

        Es la pieza que impide que una promocion reescriba el historico de
        asignaciones.
        """
        for v in self.historico_categoria:
            if v.vigente_en(momento):
                return v.codigo_categoria
        return None

    def skill(self, codigo: str) -> Optional[Skill]:
        for s in self.skills:
            if s.codigo == codigo:
                return s
        return None

    def activa_en(self, momento: date) -> bool:
        if momento < self.fecha_alta:
            return False
        return self.fecha_baja is None or momento <= self.fecha_baja


@dataclass(frozen=True)
class Ausencia:
    persona_id: str
    tipo: TipoDisponibilidad
    desde: date
    hasta: date
    aprobada: bool = True

    def solapa(self, desde: date, hasta: date) -> bool:
        return self.desde <= hasta and desde <= self.hasta


@dataclass(frozen=True)
class Proyecto:
    codigo: str
    nombre: str
    cliente: str
    responsable: str
    desde: date
    hasta: date


@dataclass(frozen=True)
class Posicion:
    """Una posicion de una demanda: que categoria y que skill se piden."""
    rol: str
    codigo_categoria: str
    skill: str
    nivel_minimo: int
    dedicacion_pct: int


@dataclass
class Demanda:
    demanda_id: str
    proyecto: str
    solicitante: str
    posiciones: list
    desde: date
    hasta: date
    prioridad: str              # alta | media | baja
    momento_solicitud: str
    estado: EstadoDemanda = EstadoDemanda.SOLICITADA

    @property
    def posiciones_totales(self) -> int:
        return len(self.posiciones)


@dataclass
class Asignacion:
    """Asignacion de una persona a un proyecto.

    Registra la categoria vigente de la persona EN SU FECHA DE INICIO, y la
    version de catalogo y de politica aplicadas. Una promocion posterior no
    cambia nada de esto.
    """
    asignacion_id: str
    persona_id: str
    proyecto: str
    rol: str
    desde: date
    hasta: date
    dedicacion_pct: int
    modalidad: Modalidad
    categoria_registrada: str
    version_catalogo: str
    version_politica: str
    confirmada: bool = False
    horas: Optional[int] = None

    def solapa(self, desde: date, hasta: date) -> bool:
        return self.desde <= hasta and desde <= self.hasta


@dataclass
class Propuesta:
    """Salida del agente de staffing para una posicion de una demanda."""
    demanda_id: str
    rol: str
    candidatos: list = field(default_factory=list)
    descartados: list = field(default_factory=list)
    explicacion: str = ""
