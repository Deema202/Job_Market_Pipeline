from sqlalchemy import (
    create_engine,
    Integer,
    Column,
    String,
    Float,
    Boolean,
    Date,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship

# Base model class for declarative definitions
Base = declarative_base()
DB_URL = "sqlite:///jobs_market.db"


class DimCompany(Base):
    """Dimension table for company details."""
    __tablename__ = "dim_company"
    company_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String, unique=True, nullable=False)

    jobs = relationship("FactJobs", back_populates="company")


class DimLocation(Base):
    """Dimension table for geographic and location details."""
    __tablename__ = "dim_location"
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String, nullable=False)
    country = Column(String)
    region = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    jobs = relationship("FactJobs", back_populates="location")


class DimCategory(Base):
    """Dimension table for job categories and tags."""
    __tablename__ = "dim_category"
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_tag = Column(String, unique=True, nullable=False)
    category_label = Column(String)

    jobs = relationship("FactJobs", back_populates="category")


class DimContract(Base):
    """Dimension table for employment contract types."""
    __tablename__ = "dim_contract"
    contract_id = Column(Integer, primary_key=True, autoincrement=True)
    contract_type = Column(String, nullable=False)
    contract_name = Column(String, nullable=False)

    jobs = relationship("FactJobs", back_populates="contract")


class DimDate(Base):
    """Dimension table for date breakdown and time attributes."""
    __tablename__ = "dim_date"
    date_id = Column(Integer, primary_key=True)
    full_date = Column(Date, nullable=False)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)

    jobs = relationship("FactJobs", back_populates="date_dim")


class FactJobs(Base):
    """Fact table storing core job metrics, attributes, and foreign keys to dimensions."""
    __tablename__ = "fact_jobs"
    job_id = Column(String, primary_key=True)  # Adzuna job ID
    title = Column(String)
    salary_min = Column(Float)
    salary_max = Column(Float)
    salary_avg = Column(Float)
    salary_is_predicted = Column(Boolean)
    redirect_url = Column(Text)
    description = Column(Text)

    # Foreign Keys linking to dimension tables
    company_id = Column(Integer, ForeignKey("dim_company.company_id"))
    location_id = Column(Integer, ForeignKey("dim_location.location_id"))
    category_id = Column(Integer, ForeignKey("dim_category.category_id"))
    contract_id = Column(Integer, ForeignKey("dim_contract.contract_id"))
    date_id = Column(Integer, ForeignKey("dim_date.date_id"))

    # ORM relationships
    company = relationship("DimCompany", back_populates="jobs")
    location = relationship("DimLocation", back_populates="jobs")
    category = relationship("DimCategory", back_populates="jobs")
    contract = relationship("DimContract", back_populates="jobs")
    date_dim = relationship("DimDate", back_populates="jobs")


def get_engine():
    """Creates and returns the SQLite database engine."""
    return create_engine(DB_URL, echo=False)


def create_table(engine):
    """Creates all defined tables in the database if they do not exist."""
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    # Initialize database and tables on direct execution
    engine = get_engine()
    create_table(engine)