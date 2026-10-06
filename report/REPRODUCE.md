# Kiểm tra và tái lập bài lab

Chạy tại gốc kho trong PowerShell, Docker Desktop dùng Linux containers. Không cần cài thư viện vào Python Windows.

```powershell
docker build -t lab-deepagents .
docker build -f report/Dockerfile.tools -t lab-deepagents-tools .
$labWorkspace = (Get-Location).Path
docker run --rm --network none -e PYTHONDONTWRITEBYTECODE=1 --mount "type=bind,source=$labWorkspace,target=/lab" lab-deepagents-tools python -m pytest
docker run --rm --network none --mount "type=bind,source=$labWorkspace,target=/lab" lab-deepagents-tools python scripts/verify_freeze.py
docker run --rm --network none --mount "type=bind,source=$labWorkspace,target=/lab" lab-deepagents-tools python report/check_submission.py
docker run --rm --network none --mount "type=bind,source=$labWorkspace,target=/lab" lab-deepagents-tools python -m lab.compare
docker run --rm --network none --mount "type=bind,source=$labWorkspace,target=/lab" lab-deepagents-tools python scripts/check_breakdown.py
```

Các kiểm tra này không gọi API. Phép băm skill phải được kiểm tra trong Linux giống môi trường thí nghiệm vì hàm hash được cung cấp dùng chuỗi đường dẫn của hệ điều hành.

**Cấu hình thí nghiệm**: endpoint tương thích OpenAI modelapi.vn, `LAB_MODEL=openai:gpt-5.5`, `LAB_TEMPERATURE=0`, giới hạn 40 bước, timeout API 120 giây, không retry SDK. Cấu hình khóa nằm trong `.env` bị Git ignore. Có thể dùng biến `OPENAI_BASE_URL` với nhà cung cấp OpenAI-compatible khi đặt `openai:<model>`; cấu hình phải khớp nhà cung cấp thực tế của người chạy.

Để làm thí nghiệm mới, dùng bản sao/nhánh độc lập và thư mục kết quả riêng, không thay skill hoặc tag freeze của bài đã nộp. Các pha của script hỗ trợ là:

```text
python report/run_lab.py learning
python report/run_lab.py curator
python report/run_lab.py development
```

Các lệnh API trên phải chạy bằng Docker tương tự các lệnh kiểm tra, bổ sung `--env-file .env`. Chi phí token phát sinh thật. Sau phát triển, đánh giá skill nguyên bản; không sửa tay. Sao lưu results/skills-auto thành results/skills-auto-dev, điền và commit H1–H3 với message hypotheses, tạo commit freeze skills riêng rồi tag freeze; chỉ sau đó chạy:

```text
python report/run_lab.py evaluation
```

Script ghi lệnh con, thời gian và mã thoát vào report/commands.jsonl, không ghi khóa. Mã thoát CLI không chứng minh mọi tác vụ thành công: phải đọc trường error trong run.json. Không chạy lại lượt có điểm thấp chỉ để chọn kết quả tốt; chỉ khắc phục lỗi thực thi/môi trường có ghi chú.

Runner chỉ chuẩn hóa CRLF trong bản sao sandbox, không sửa nguồn tasks. Skill được curator ghi UTF-8 nguyên bản, được băm trước/sau mỗi lượt. Các tệp tools/script hỗ trợ trong report không thay cho các script chấm được cung cấp.

`report/compose_report.py` dựng bản nháp bảng/số liệu; báo cáo cuối có phân tích bổ sung dựa trên vết, nên không chạy script này đè lên báo cáo cuối nếu muốn giữ phần nhận xét.
