import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.ml.predictor import ClusterPredictor, reset_predictor
from app.ml.training import save_pipeline, train_clustering_pipeline


def _training_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [25, 18, 4, 12, 95.0, 72.0, 1.25],
            [24, 17, 5, 11, 92.0, 74.0, 1.22],
            [8, 16, 12, 3, 55.0, 82.0, 0.95],
            [7, 15, 11, 2, 52.0, 80.0, 0.92],
            [14, 12, 6, 7, 72.0, 68.0, 1.05],
            [13, 13, 5, 6, 70.0, 66.0, 1.02],
            [10, 10, 8, 5, 60.0, 88.0, 1.00],
            [11, 11, 7, 4, 62.0, 85.0, 1.01],
        ],
        columns=["kills", "deaths", "assists", "headshots", "adr", "kast", "rating"],
    )


def _train_model_at(path) -> ClusterPredictor:
    pipeline = train_clustering_pipeline(_training_dataframe(), n_clusters=4)
    save_pipeline(pipeline, path)
    return ClusterPredictor(model_path=str(path))


@pytest.fixture
def db_session() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def predictor(tmp_path) -> ClusterPredictor:
    reset_predictor()
    return _train_model_at(tmp_path / "test_model.joblib")


@pytest.fixture
def client(db_session: Session, tmp_path, monkeypatch) -> TestClient:
    model_path = tmp_path / "api_model.joblib"
    trained = _train_model_at(model_path)

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    monkeypatch.setattr("app.services.analytics_service.get_predictor", lambda: trained)

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    reset_predictor()
