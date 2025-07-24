

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

## **4. Cấu Trúc Thư Mục**

final-airflow/
├── config/                          # <-- THƯ MỤC CONFIG ĐÃ THÊM
│   ├── log_data/
│   └── song_data/
├── dags/
│   └── dag_test.py   # File định nghĩa DAG chính
├── plugins/
│   ├── init.py
│   ├── helpers/
│   │   ├── init.py
│   │   └── sql_queries.py          # Module chứa các câu lệnh SQL
│   └── operators/
│       ├── init.py
│       ├── stage_postgres.py       # Operator cho việc staging
│       ├── load_fact.py            # Operator cho bảng fact
│       ├── load_dimension.py       # Operator cho các bảng dimension
│       └── data_quality.py         # Operator kiểm tra chất lượng dữ liệu
├── screenshots/
│   ├── 1.png
│   └── 2.png
├── create_tables.sql               # File SQL để tạo bảng
├── docker-compose.yaml             # file để chạy docker
└── README.md                       # File báo cáo