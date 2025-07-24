

**Bước 1: Chuẩn bị Dữ liệu và Môi trường**
* Đặt 2 thư mục dữ liệu thô `song_data` và `log_data` vào một đường dẫn trên máy.
* Cập nhật lại biến `DATA_PATH` trong file `dags/final_project_local_dag.py` để trỏ đến đúng đường dẫn chứa dữ liệu ở trên.

**Bước 2: Cài đặt Cơ sở dữ liệu**
* Tạo một database mới trong PostgreSQL run bằng Docker
* Kết nối vào database vừa tạo bằng dbeaver và chạy toàn bộ câu lệnh trong file `create_tables.sql` để khởi tạo cấu trúc cho các bảng.

**Bước 3: Cấu hình Airflow**
* Sao chép 2 thư mục `dags` và `plugins` vào trong thư mục làm việc của Airflow.
* Tại giao diện Airflow Web UI, vào mục **Admin -> Connections**, tạo một kết nối mới với các thông số:
    * **Connection Id**: `postgres_default`
    * **Connection Type**: `Postgres`

**Bước 4: Chạy Pipeline**
* Tại giao diện Airflow UI, tìm đến DAG có tên `final_project_local_dag`.
* Nhấn vào nút "Play" (Trigger DAG) để bắt đầu chạy pipeline.


## 📁 Cấu trúc thư mục

```
final-airflow/
├── config/                          # Thư mục chứa dữ liệu đầu vào
│   ├── log_data/                    # Dữ liệu log dạng JSON
│   └── song_data/                   # Dữ liệu bài hát dạng JSON
├── dags/
│   └── dag_test.py                  # File định nghĩa DAG chính
├── plugins/
│   ├── __init__.py
│   ├── helpers/
│   │   ├── __init__.py
│   │   └── sql_queries.py          # Module chứa các câu lệnh SQL
│   └── operators/                  
│       ├── __init__.py
│       ├── stage_postgres.py       # Operator để load dữ liệu staging vào PostgreSQL
│       ├── load_fact.py            # Operator load dữ liệu vào bảng fact (songplays)
│       ├── load_dimension.py       # Operator load dữ liệu vào các bảng dimension
│       └── data_quality.py         # Operator kiểm tra chất lượng dữ liệu
├── screenshots/
│   ├── 1.png                        # Ảnh minh họa UI hoặc kết quả DAG
│   └── 2.png
├── create_tables.sql               # Script SQL để tạo các bảng trong schema
├── docker-compose.yaml             # File cấu hình Docker Compose để chạy Airflow và PostgreSQL
└── README.md                       # Tài liệu mô tả dự án
```