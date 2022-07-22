from pydantic import BaseModel, Field


class Geometry(BaseModel):
    type: str = Field("Polygon")
    coordinates: list[list[list[float]]]


class Probsevere(BaseModel):
    PROB: int
    LINE01: str
    LINE02: str
    LINE03: str
    LINE04: str
    LINE05: str
    LINE06: str
    LINE07: str
    LINE08: str
    LINE09: str
    LINE10: str
    LINE11: str
    LINE12: str
    LINE13: str
    LINE14: str
    LINE15: str


class Probtor(BaseModel):
    PROB: int
    LINE01: str
    LINE02: str
    LINE03: str
    LINE04: str
    LINE05: str
    LINE06: str
    LINE07: str
    LINE08: str
    LINE09: str
    LINE10: str


class Probhail(BaseModel):
    PROB: int
    LINE01: str
    LINE02: str
    LINE03: str
    LINE04: str
    LINE05: str
    LINE06: str
    LINE07: str
    LINE08: str


class Probwind(BaseModel):
    PROB: int
    LINE01: str
    LINE02: str
    LINE03: str
    LINE04: str
    LINE05: str
    LINE06: str
    LINE07: str
    LINE08: str
    LINE09: str
    LINE10: str


class Models(BaseModel):
    probsevere: Probsevere
    probtor: Probtor
    probhail: Probhail
    probwind: Probwind


class Properties(BaseModel):
    MUCAPE: int
    MLCAPE: int
    MLCIN: int
    EBSHEAR: float
    SRH01KM: int
    MEANWIND_1_3kmAGL: float = Field(..., alias="MEANWIND_1-3kmAGL")
    MESH: float
    VIL_DENSITY: float
    FLASH_RATE: str
    FLASH_DENSITY: float
    MAXLLAZ: float
    P98LLAZ: float
    P98MLAZ: float
    MAXRC_EMISS: float
    MAXRC_ICECF: float
    WETBULB_0C_HGT: float
    PWAT: float
    CAPE_M10M30: float
    LJA: float
    SIZE: int
    AVG_BEAM_HGT: str
    MOTION_EAST: float
    MOTION_SOUTH: float
    PS: int
    ID: int


class Feature(BaseModel):
    type: str = Field("Feature")
    geometry: Geometry
    models: Models
    properties: Properties


class FeatureCollection(BaseModel):
    source: str
    product: str
    validTime: str
    productionTime: str
    machine: str
    type: str = Field("FeatureCollection")
    features: list[Feature]
