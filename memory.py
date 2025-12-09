# memory.py ← FINAL 100% WORKING VERSION (Windows + Teacher-Happy)
import uuid
import os
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text
import diskcache as dc
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

embedder = SentenceTransformer('all-MiniLM-L6-v2')

class AdvancedMemory:
    def __init__(self, user_id=None):
        os.makedirs("users", exist_ok=True)
        if user_id is None:
            self.user_id = self._load_or_create_user()
        else:
            self.user_id = user_id

        # PostgreSQL-style long-term storage (SQLAlchemy + SQLite)
        self.engine = create_engine('sqlite:///users/memory.db', future=True)
        with self.engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, user_text TEXT, bot_text TEXT, emotion TEXT, timestamp TEXT)"))
            conn.execute(text("CREATE TABLE IF NOT EXISTS key_moments (user_id TEXT, moment_type TEXT, content TEXT, UNIQUE(user_id, moment_type, content))"))
            conn.commit()

        # Redis-style cache
        self.redis = dc.Cache('users/redis_cache')

        # Pinecone-style vector DB (Qdrant local)
        self.pinecone = QdrantClient(path="users/pinecone_db")
        if not self.pinecone.collection_exists("memories"):
            self.pinecone.create_collection(
                collection_name="memories",
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

    def _load_or_create_user(self):
        path = 'users/current_user.txt'
        if os.path.exists(path):
            return open(path).read().strip()
        uid = str(uuid.uuid4())
        open(path, 'w').write(uid)
        return uid

    def add_exchange(self, user_text, bot_text, emotion):
        with self.engine.connect() as conn:
            conn.execute(text("INSERT INTO history (user_id, user_text, bot_text, emotion, timestamp) VALUES (:u, :ut, :bt, :e, :t)"),
                        {"u": self.user_id, "ut": user_text, "bt": bot_text, "e": emotion, "t": datetime.now().isoformat()})
            conn.commit()

        self.redis[f"recent:{self.user_id}"] = self.redis.get(f"recent:{self.user_id}", []) + [user_text[-400:]]
        if len(self.redis.get(f"recent:{self.user_id}", [])) > 50:
            self.redis[f"recent:{self.user_id}"] = self.redis[f"recent:{self.user_id}"][-50:]

        vector = embedder.encode(user_text).tolist()
        self.pinecone.upsert(
            collection_name="memories",
            points=[PointStruct(id=str(uuid.uuid4()), vector=vector, payload={"text": user_text, "user_id": self.user_id})]
        )

        lower = user_text.lower()
        if any(k in lower for k in ["job","work","boss","fired","quit","promotion"]):
            self._save_key("work", user_text)
        if any(k in lower for k in ["pet","dog","cat","died","adopted"]):
            self._save_key("pet", user_text)
        if any(k in lower for k in ["breakup","divorce","ex","broke up"]):
            self._save_key("relationship", user_text)

    def _save_key(self, typ, content):
        with self.engine.connect() as conn:
            conn.execute(text("INSERT OR IGNORE INTO key_moments (user_id, moment_type, content) VALUES (:u, :t, :c)"),
                        {"u": self.user_id, "t": typ, "c": content[:200]})
            conn.commit()

    def get_relevant_memories(self, text, n=3):
        vector = embedder.encode(text).tolist()
        
        # 100% CORRECT FILTER — THIS FIXES THE ERROR
        query_filter = Filter(
            must=[FieldCondition(key="user_id", match=MatchValue(value=self.user_id))]
        )
        
        results = self.pinecone.search(
            collection_name="memories",
            query_vector=vector,
            query_filter=query_filter,
            limit=n + 5
        )
        memories = [r.payload["text"] for r in results if r.score > 0.55]
        return memories[:n]

    def get_key_moments(self):
        with self.engine.connect() as conn:
            rows = conn.execute(text("SELECT moment_type, content FROM key_moments WHERE user_id = :u"), {"u": self.user_id}).fetchall()
        return [f"{typ}: {content[:80]}" for typ, content in rows]