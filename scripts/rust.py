import sqlite3
from datetime import datetime


class KnowledgeDatabase:
    def __init__(self, db_path="example.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """初始化数据库表结构"""
        self.cursor.executescript("""
CREATE TABLE IF NOT EXISTS knowledge_base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 知识库ID, 自动生成
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 创建时间
    finish_time DATETIME,                                  -- 完成录库时间
    encoding_model TEXT,                                   -- 编码模型
    is_multimodal BOOLEAN NOT NULL DEFAULT 0,              -- 是否多模态，0表示否，1表示是
    name TEXT NOT NULL,                                    -- 知识库名称
    description TEXT,                                      -- 知识库描述
    bind_path TEXT,                                        -- 绑定路径
    UNIQUE(name)                                           -- 确保知识库名称唯一
);

CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自动生成的主键id
    knowledge_base_id INTEGER NOT NULL,    -- 知识库ID
    file_path TEXT NOT NULL,               -- 文件路径
    file_md5 TEXT NOT NULL,                -- 文件的MD5
    file_query_count INTEGER DEFAULT 0,    -- 文件被查询次数
    file_modify_time DATETIME NOT NULL,    -- 文件修改时间
    file_type TEXT,                        -- 文件类型
    knowledge_category TEXT,               -- 知识分类
    UNIQUE(file_md5),                      -- 确保文件MD5唯一
    UNIQUE(file_path)                      -- 确保文件路径唯一
);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_id_file_id ON files(knowledge_base_id);

CREATE TABLE IF NOT EXISTS knowledge_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自动生成的主键id
    knowledge_base_id INTEGER NOT NULL,    -- 知识库ID
    file_id INTEGER NOT NULL,              -- 文件ID
    fragment_number INTEGER NOT NULL,      -- 片段编号
    vector_id INTEGER,                     -- 向量ID，可以为空
    fragment_content TEXT,        -- 片段内容
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 更新时间
    finish_time DATETIME ,                   -- 录入完成时间
    fragment_query_count INTEGER DEFAULT 0,  -- 片段被查询次数
    last_query_time DATETIME,              -- 最近查询时间
    knowledge_category TEXT,               -- 知识分类
    FOREIGN KEY (knowledge_base_id) REFERENCES knowledge_base(id),  -- knowledge_base_id knowledge_base中
    FOREIGN KEY (file_id) REFERENCES files(id) -- 确保file_id 存在与files中
);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_id_file_id ON knowledge_details(knowledge_base_id, file_id);
CREATE INDEX IF NOT EXISTS idx_vector_id_knowledge_base_id ON knowledge_details(vector_id, knowledge_base_id);


CREATE VIRTUAL TABLE IF NOT EXISTS fts_knowledge_details USING fts5(
    fragment_content,  -- 用于全文搜索的字段
    knowledge_base_id,  -- 对应的知识库ID
    file_id,            -- 对应的文件ID
    fragment_number,     -- 对应的片段编号
    content=''          -- 可以为空，默认是空的内容
);





        """)
        self.conn.commit()

    def add_knowledge(self, knowledge_base_id, file_id, fragment_number, fragment_content, vector_id=None):
        """添加知识片段"""
        self.cursor.execute(
            """
            INSERT INTO knowledge_details (knowledge_base_id, file_id, fragment_number, fragment_content, vector_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (knowledge_base_id, file_id, fragment_number, fragment_content, vector_id)
        )
        self.conn.commit()

    def add_knowledge_base(self, name, description, encoding_model=None, is_multimodal=0, bind_path=None):
        """添加知识库"""
        self.cursor.execute(
            """
            INSERT INTO knowledge_base (name, description, encoding_model, is_multimodal, bind_path)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, description, encoding_model, is_multimodal, bind_path)
        )
        self.conn.commit()
        return self.cursor.lastrowid  # 返回新插入的知识库ID

    def close(self):
        """关闭数据库连接"""
        self.conn.close()

    def get_all(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()