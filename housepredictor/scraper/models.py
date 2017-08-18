from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import Column, Integer, String, DateTime

import housepredictor.scraper.settings as settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE),execution_options={'sqlite_raw_colnames':True})

def create_items_table(engine):

    DeclarativeBase.metadata.create_all(engine)


class Items(DeclarativeBase):

    __tablename__ = 'items'


    AantalBadkamers = Column('AantalBadkamers', String, nullable=True) 
    AantalKamers = Column('AantalKamers', String, nullable=True)
    BijdrageVVE = Column('BijdrageVVE', String, nullable=True)
    EnergielabelDefinitief = Column('EnergielabelDefinitief', String, nullable=True)
    EnergielabelIndex = Column('EnergielabelIndex', String, nullable=True)
    EnergielabelNietBeschikbaar = Column('EnergielabelNietBeschikbaar', String, nullable=True)
    EnergielabelNietVerplicht = Column('EnergielabelNietVerplicht', String, nullable=True)
    ErfpachtBedrag = Column('ErfpachtBedrag', String, nullable=True)

    Inhoud = Column('Inhoud', String, nullable=True) 
    PerceelOppervlakte = Column('PerceelOppervlakte', String, nullable=True)
    ServiceKosten = Column('ServiceKosten', String, nullable=True)
    SoortPlaatsing = Column('SoortPlaatsing', String, nullable=True)
    WoonOppervlakte = Column('WoonOppervlakte', String, nullable=True)
    WGS84_X = Column('WGS84_X', String, nullable=True)
    WGS84_Y = Column('WGS84_Y', String, nullable=True)
    Koopprijs = Column('Koopprijs', String, nullable=True)
  


    PublicatieDatum = Column('PublicatieDatum', String, nullable=True) 
    GelegenOp = Column('GelegenOp', String, nullable=True)
    Bouwjaar = Column('Bouwjaar', String, nullable=True)
    AantalWoonlagen = Column('AantalWoonlagen', String, nullable=True)
    Aanvaarding = Column('Aanvaarding', String, nullable=True)
    Bouwvorm = Column('Bouwvorm', String, nullable=True)
    BronCode = Column('BronCode', String, nullable=True)
    GlobalId = Column('GlobalId', Integer, primary_key=True, nullable=False)
    EnergielabelLabel = Column('EnergielabelLabel', String, nullable=True)


    PermanenteBewoning = Column('PermanenteBewoning', String, nullable=True) 
    SchuurBerging = Column('SchuurBerging', String, nullable=True)
    Soort_aanbod = Column('Soort_aanbod', String, nullable=True)
    TuinLigging = Column('TuinLigging', String, nullable=True)
    Woonplaats = Column('Woonplaats', String, nullable=True)
    VolledigeOmschrijving = Column('VolledigeOmschrijving', String, nullable=True)
    Voorzieningen = Column('Voorzieningen', String, nullable=True)
    GarageVoorzieningen = Column('GarageVoorzieningen', String, nullable=True) 
    
    
    SoortDak = Column('SoortDak', String, nullable=True) 
    GarageIsolatie = Column('GarageIsolatie', String, nullable=True)
    Ligging = Column('Ligging', String, nullable=True)
    EigendomsSituatie = Column('EigendomsSituatie', String, nullable=True)
    SchuurBergingIsolatie = Column('SchuurBergingIsolatie', String, nullable=True)
    Bijzonderheden = Column('Bijzonderheden', String, nullable=True)
    BalkonDakterras = Column('BalkonDakterras', String, nullable=True)
    WarmWater = Column('WarmWater', String, nullable=True)


    SoortWoning = Column('SoortWoning', String, nullable=True) 
    Verwarming = Column('Verwarming', String, nullable=True)
    Garage = Column('Garage', String, nullable=True)
    Isolatie = Column('Isolatie', String, nullable=True)
    SchuurBergingVoorzieningen = Column('SchuurBergingVoorzieningen', String, nullable=True)
    ShortURL = Column('ShortURL', String, nullable=True)
    Plaats = Column('Plaats', String, nullable=True)
    Postcode = Column('Postcode', String, nullable=True)
    #LastDayofRecord = Column(String, nullable=True)
    IsSearchable = Column('IsSearchable', String, nullable=True)
   
    IsVerhuurd = Column('IsVerhuurd', String, nullable=True)
    IsVerkocht = Column('IsVerkocht', String, nullable=True)
    IsVerkochtOfVerhuurd = Column('IsVerkochtOfVerhuurd', String, nullable=True)
    IsSearchable = Column('IsSearchable', String, nullable=True)
    MakelaarId = Column('MakelaarId', String, nullable=True)    
    MakelaarNaam = Column('MakelaarNaam', String, nullable=True)
    Adres = Column('Adres', String, nullable=True)

    LastDayofRecord = Column(String, nullable=True)
