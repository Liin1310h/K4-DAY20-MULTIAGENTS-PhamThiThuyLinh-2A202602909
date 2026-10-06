# Kế hoạch thực hiện lab Self evolving Agentic

Kế hoạch dựa trên [README.md](README.md), [GUIDE.md](GUIDE.md), [RUBRIC.md](RUBRIC.md), [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md) và [GLOSSARY.md](GLOSSARY.md). Tên tệp thang điểm trong kho là `RUBRIC.md`, thay cho `RUBIC.md` trong yêu cầu.

Mục tiêu là hoàn thành các hạng mục bắt buộc của thang điểm 100: cài đặt bộ khung điều khiển tác tử, so sánh `baseline`, `subagents`, `skills-auto`, và viết báo cáo có bằng chứng. Không đặt mục tiêu buộc skill phải tăng điểm; kết quả không cải thiện vẫn có giá trị nếu phân tích đúng.

Điểm bắt đầu: bốn tệp cài đặt còn hàm TODO; `report/REPORT.md` đã được tạo nhưng còn nội dung mẫu; chưa có `run.json`, `trace.md` hay skill tự sinh. `.env` và `.venv` đã tồn tại, nhưng chưa xác minh cấu hình hoặc khả năng chạy. Kế hoạch dành cho một người, dự kiến 4 buổi, khoảng 8–13 giờ; thời gian thực tế phụ thuộc API và số lỗi cần xử lý.

**Lịch làm việc đề xuất**

| Buổi | Chặng | Thời gian dự kiến | Kết quả cần đạt |
|---|---|---|---|
| 1 | 0. Chuẩn bị môi trường; 1. Hoàn thiện harness | 2,5–4 giờ | Test môi trường, agent và runner đạt; có lần chạy `baseline/data-learn` |
| 2 | 2. Chạy tập học và phân loại lỗi; 3. Curator sinh skill | 2–3,5 giờ | Đủ kết quả tập học cho hai cấu hình đầu; skill hợp lệ; lưu kết quả thử skill |
| 3 | 4. Giả thuyết và đóng băng; 5. Đánh giá chính thức | 1,25–2 giờ | Commit `hypotheses`, tag `freeze`, đủ 18 kết quả chính thức; kiểm tra đóng băng đạt |
| 4 | 6. Phân tích và báo cáo; 7. Kiểm tra nộp bài | 2–3 giờ | Báo cáo đủ 10 mục, bảng so sánh khớp dữ liệu và sản phẩm nộp đầy đủ |

Các lệnh dưới đây chạy tại thư mục gốc dự án, trong môi trường Python đã kích hoạt. Trên Windows, dùng **WSL hoặc Docker** theo README vì shell của tác tử cần `/bin/sh`. Các lệnh dạng Bash áp dụng trong môi trường đó; không mặc định môi trường ảo Windows hiện có dùng được trong WSL.

**0. Chuẩn bị môi trường và hiểu bài — GUIDE Phần 0**

- [ ] Chọn WSL hoặc Docker; xác nhận Python 3.11 trở lên và cài thư viện theo README.
- [ ] Kiểm tra `.env` đã có đủ cấu hình mô hình hỗ trợ gọi công cụ. Giữ khóa API trong `.env`; tệp này đã được `.gitignore` loại trừ.
- [ ] Giữ `report/REPORT.md` hiện có và điền dần, tránh sao chép mẫu đè lên phần đã viết.
- [ ] Điền mục 1: họ tên, mã sinh viên, mô hình, nhiệt độ, giới hạn đệ quy, hệ điều hành, phiên bản Deep Agents; cập nhật số lần chạy và commit đóng băng về sau.
- [ ] Chạy kiểm tra môi trường và xem công cụ mặc định:

```bash
pip install -e .
pytest tests/test_01_provided.py
python scripts/tour.py
python -c "from lab.model import make_model; print(make_model().invoke('Reply with OK').content)"
pip show deepagents
```

Đầu ra: `test_01` đạt 15 test; lệnh thử mô hình trả lời thành công; mục 3 của báo cáo trả lời đủ ba câu hỏi trong GUIDE. `tour.py` và pytest chạy ngoại tuyến; lệnh thử mô hình dùng API và tốn một lượng token nhỏ.

Nắm các thuật ngữ trong GLOSSARY: harness là bộ khung điều khiển; backend cung cấp tệp và shell; subagent có ngữ cảnh riêng; curator rút skill từ phản hồi; freeze chốt skill trước đánh giá. Phân biệt **test mã nguồn** với **check chấm tác vụ**, và **tác vụ học** với **tác vụ đánh giá**.

**1. Hoàn thiện harness — GUIDE Phần 1, RUBRIC hạng mục 1 và 3**

Làm đúng thứ tự phụ thuộc, chỉ cài đặt các phần TODO và import cần thiết:

| Thứ tự | Tệp/hàm | Tài liệu thực hiện | Kiểm tra ngay sau khi làm |
|---|---|---|---|
| 1 | `src/lab/subagents.py`: `get_subagents` | `guides/pseudocode/02_subagents.md` | `pytest tests/test_02_agent.py -k subagents` |
| 2 | `src/lab/agent.py`: `make_backend`, `build_agent` | `guides/pseudocode/01_agent.md` | `pytest tests/test_02_agent.py` |
| 3 | `src/lab/runner.py`: `run_task` | `guides/pseudocode/03_runner.md` | `pytest tests/test_03_runner.py` |

- [x] Định nghĩa ít nhất hai subagent có vai trò khác nhau, ví dụ thực hiện và kiểm chứng; `description` nói rõ khi nào gọi, `system_prompt` xác định phạm vi công việc.
- [x] Backend tìm được Python, không đưa khóa API vào môi trường shell của tác tử; công cụ tệp và shell cùng dùng đường dẫn tương đối `workspace/...`.
- [x] Runner dùng sandbox riêng, giữ nguyên workspace gốc; ghi điểm, check và `detail`, token, thời gian, lỗi, `timestamp`, `skills_sha256`, `skills_modified`, `skills_read`, `subagent_calls`.
- [ ] Khi test agent và runner đã đạt, chạy thử chuỗi thật:

```bash
python -m lab.runner --condition baseline --tasks data-learn
```

Đầu ra: các test tương ứng đạt toàn bộ; `results/baseline/data-learn/run.json` và `trace.md` tồn tại, token tổng lớn hơn 0, có thông tin check. Lần chạy này được dùng luôn làm baseline của `data-learn`, không chạy lặp lại trong chặng 2 khi kết quả đã hợp lệ.

**2. Chạy tác vụ học, đọc vết và phân loại lỗi — GUIDE Phần 2**

```bash
python -m lab.runner --condition baseline --tasks code-learn logs-learn
python -m lab.runner --condition subagents --tasks learn
```

- [ ] Xác nhận cả hai điều kiện có đủ ba tác vụ học: `code-learn`, `data-learn`, `logs-learn`.
- [ ] Dựa trên baseline, lập bảng ở mục 4 báo cáo: mỗi dòng là một check thất bại, ghi tác vụ, tên check, nhóm lỗi A–G và trích `detail` hoặc vết.
- [ ] Phân loại ít nhất bốn check thất bại thực tế theo tiêu chí RUBRIC. Nếu số lỗi thực tế ít hơn, báo cáo đầy đủ số có được và giải thích; không tạo lỗi giả.
- [ ] Phân biệt các nhóm: A bỏ qua đặc tả; B không kiểm chứng; C vá triệu chứng; D bỏ sót dữ liệu bẩn/định dạng; E vi phạm quy ước tổ chức; F báo cáo hoàn thành sai; G khác.
- [ ] Với nhóm E, đối chiếu check bắt đầu bằng `rule_` và phản hồi `RULE:`. Nếu lỗi tập trung ở E, dùng số check kỹ thuật đạt/tổng làm bằng chứng phủ định cho các nhóm A–D.
- [ ] Không tính lỗi API, mạng hoặc môi trường là lỗi của tác tử. Lưu thông tin lỗi, khắc phục rồi chạy lại và ghi chú.
- [ ] Điền mục 5: vai trò subagent, số `subagent_calls`, nội dung giao việc, việc kiểm chứng báo cáo và chênh lệch token/thời gian với baseline.

Đầu ra: sáu kết quả tập học hợp lệ; mục 4 và 5 có bằng chứng cụ thể. `subagent_calls = 0` vẫn là kết quả hợp lệ cần giải thích. Vết chỉ chứa luồng chính, vì vậy nhận xét về công việc bên trong subagent phải giới hạn ở những gì quan sát được.

**3. Cài đặt curator, sinh và thử skill — GUIDE Phần 3**

- [ ] Đọc `guides/pseudocode/04_curator.md` và `05_skill_quality.md`.
- [ ] Cài đặt `curate_skills` trong `src/lab/curator.py`, giữ nguyên `validate_skill` và `parse_skill_blocks`.
- [ ] Curator chỉ dùng kết quả baseline của tác vụ học, gồm tên check thất bại, `detail` và vết; không đưa dữ liệu đánh giá vào prompt.

```bash
pytest tests/test_04_curator.py
pytest
python -m lab.curator
```

- [ ] Đánh giá từng skill ở mục 6 báo cáo: khả năng tổng quát hóa, tính đúng, số dòng, phần mô tả tình huống kích hoạt (`description`).
- [ ] Có ít nhất một skill hợp lệ do curator sinh. Không sửa tay nội dung. Có thể xóa skill kém chất lượng hoặc có hại và chạy lại curator **tối đa hai lần**, ghi rõ lý do; tổng cộng tối đa ba lần gồm lần đầu.
- [ ] Kiểm tra định dạng qua validator có sẵn: tên an toàn và khớp tên khối, mô tả hợp lệ, phần thân không quá 80 dòng, không chứa định danh đánh giá. Định dạng hợp lệ chưa chứng minh nội dung đúng.
- [ ] Sau khi chọn bộ skill để thử, chạy trên tác vụ học:

```bash
python -m lab.runner --condition skills-auto --tasks learn
```

- [ ] Đọc `skills_read` và vết để phân biệt không đọc skill, đọc nhưng chỉ làm theo một phần, hoặc áp dụng đầy đủ.
- [ ] Chốt bộ skill sau thử nghiệm. Muốn so sánh nhiễu giữa lần thử và lần chính thức, hai lần phải dùng **cùng bộ skill**.
- [ ] Sao lưu kết quả thử trước khi chạy chính thức, với thư mục đích chưa tồn tại:

```bash
mv results/skills-auto results/skills-auto-dev
```

Đầu ra: toàn bộ pytest đạt; có skill tự sinh và bảng nhận xét; `results/skills-auto-dev/` giữ ba kết quả trước đóng băng, phục vụ mục 8 câu 6. Nếu cần thêm lượt thử sau khi curator sinh lại skill, lưu riêng từng lượt và tính vào ngân sách.

**4. Viết giả thuyết và đóng băng — GUIDE Phần 4.0–4.1**

- [ ] Trước khi thấy bất kỳ điểm đánh giá nào, điền đủ H1–H3 ở mục 2 báo cáo, dựa trên tập học và có căn cứ từ tài liệu tham khảo.
- [ ] H1: dự đoán `subagents` so với `baseline` trên tập đánh giá và lý do.
- [ ] H2: dự đoán `skills-auto` so với `baseline`, liên hệ với nhóm lỗi mà skill xử lý.
- [ ] H3: dự đoán khác biệt giữa tập học và tập đánh giá, gồm khả năng tổng quát hóa và quy ước mới.
- [ ] Kiểm tra các tệp sẽ commit; stage rõ phạm vi vì hiện có `.ai-log/` chưa được theo dõi, cần rà soát trước khi quyết định đưa vào kho.

```bash
git status --short
git add src/lab/agent.py src/lab/subagents.py src/lab/runner.py src/lab/curator.py skills/auto report/REPORT.md results KE_HOACH.md
git diff --cached --stat
git commit -m "hypotheses"
git commit --allow-empty -m "freeze skills"
git tag freeze
git rev-parse freeze
```

Đầu ra: commit `hypotheses` chứa H1–H3 đã điền, đứng trước commit được tag `freeze`. Ghi mã commit của tag vào mục 1 báo cáo. Từ mốc này giữ nguyên cây `skills/`; không thay skill theo kết quả đánh giá.

**5. Chạy đánh giá chính thức và sinh bảng — GUIDE Phần 4.2–4.4**

Chạy tuần tự các lệnh sau sau mốc đóng băng:

```bash
python -m lab.runner --condition baseline --tasks eval
python -m lab.runner --condition subagents --tasks eval
python -m lab.runner --condition skills-auto --tasks all
python scripts/verify_freeze.py
python -m lab.compare > report/table.md
python scripts/check_breakdown.py
```

- [ ] Ba thư mục chính `results/baseline/`, `results/subagents/`, `results/skills-auto/` mỗi thư mục đủ sáu tác vụ, tổng cộng 18 bộ `run.json` và `trace.md`.
- [ ] `verify_freeze.py` báo `OK`, kiểm tra sáu lượt `skills-auto` chính thức. Các lượt này dùng đúng băm skill đã đóng băng, bắt đầu sau mốc đóng băng và có `skills_modified = false`.
- [ ] Nếu có lỗi hạ tầng hoặc lượt không hợp lệ, lưu kết quả lỗi trước khi chạy lại; nêu nguyên nhân và cách xử lý trong báo cáo. Không sửa skill để khắc phục điểm đánh giá thấp.
- [ ] `report/table.md` có ba điều kiện, sáu hàng tác vụ và các hàng tổng hợp.
- [ ] Dán bảng cùng thống kê check kỹ thuật/quy ước vào mục 7. Giữ riêng kết quả trước đóng băng để không lẫn vào bảng chính thức.

Đầu ra: đủ kết quả chính thức, kiểm tra đóng băng đạt và bảng được sinh từ dữ liệu thực tế.

**6. Phân tích và hoàn thiện báo cáo — GUIDE Phần 5, RUBRIC hạng mục 6**

Điền báo cáo xuyên suốt quá trình; dùng buổi cuối để hoàn thiện mục 8–10 và rà soát các mục trước:

| Mục báo cáo | Nội dung cần hoàn thành | Bằng chứng chính |
|---|---|---|
| 1 | Thông tin cá nhân, cấu hình, ngân sách/lượt chạy, commit đóng băng | Cấu hình không chứa khóa, phiên bản, lịch sử Git |
| 2 | H1–H3 và căn cứ; giữ nguyên giả thuyết đã đăng ký | Commit `hypotheses` trước `freeze` |
| 3 | Ba câu trả lời làm quen Deep Agents | Kết quả `tour.py` |
| 4 | Phân loại lỗi A–G và nhóm chiếm đa số | Check, `detail`, vết baseline tập học |
| 5 | Thiết kế và hành vi subagent, chi phí | `subagent_calls`, vết, token/thời gian |
| 6 | Đánh giá từng skill và lịch sử tuyển chọn | `SKILL.md`, lý do xóa/chạy lại, `skills_read` |
| 7 | Bảng chính thức và thống kê check, ghi chú lỗi | `table.md`, `check_breakdown.py`, kết quả đóng băng |
| 8 | Trả lời đủ sáu câu phân tích | Số liệu mục 7, vết và kết quả thử đã sao lưu |
| 9 | Ít nhất ba hạn chế và ảnh hưởng đến kết luận | Số mẫu nhỏ, số lần chạy, nhiễu, mô hình duy nhất… |
| 10 | Kết luận tối đa năm câu, một đề xuất tiếp theo | Những nhận định được số liệu hỗ trợ |
| Phụ lục | Lệnh theo thứ tự, tài liệu tham khảo, ghi chú và mở rộng nếu có | Nhật ký thực hiện |

Mục 8 cần so sánh riêng tập học/tập đánh giá; tách check kỹ thuật và `rule_`; giải thích một check skill giúp và một check không giúp bằng vết nếu dữ liệu có các trường hợp đó; phân tích token, quá khớp/rò rỉ và nhiễu giữa hai lần dùng cùng bộ skill. Nếu không có trường hợp skill giúp hoặc không giúp, nêu rõ điều quan sát được, không suy diễn bằng chứng.

Để so sánh chi phí, có thể dùng điểm trung bình chuẩn hóa chia token trung bình, nhân 1.000 để trình bày điểm trên 1.000 token; tính cùng cách cho mọi điều kiện và tách hai vai trò. Nếu đánh giá chi phí toàn quy trình tự tiến hóa, nêu thêm lượt thử và chi phí curator thay vì chỉ nhìn token của tác tử ở lần chính thức.

**7. Kiểm tra trước khi nộp**

- [ ] Các phần cài đặt trong bốn tệp đúng phạm vi; không sửa `tests/`, `tasks/`, `scripts/`, mã và hằng số được cung cấp sẵn.
- [ ] `pytest` đạt; nếu đã chạy toàn bộ và mã không đổi thì không cần chạy lặp lại. Khi mã thay đổi hoặc có lỗi mới, chạy lại kiểm tra liên quan.
- [ ] Kiểm tra cuối `verify_freeze.py` báo `OK`.
- [ ] Đủ 18 bộ kết quả chính thức và ba bộ kết quả thử được dùng để phân tích nhiễu; các lượt lỗi/chạy lại được ghi chú và giữ khi dùng trong báo cáo.
- [ ] Có ít nhất một skill tự sinh nguyên bản; cây skill không đổi sau `freeze`.
- [ ] `report/table.md` khớp `run.json`; báo cáo hoàn thành đủ mục, không còn dòng hướng dẫn từ mẫu.
- [ ] Không có khóa API trong tệp được stage, vết hoặc báo cáo. Kiểm tra `git status` và danh sách tệp trước commit nộp bài.
- [ ] Commit sản phẩm cuối theo quy trình của lớp, giữ nguyên tag `freeze` và lịch sử giả thuyết.

Sản phẩm nộp: bốn tệp mã cài đặt trong `src/lab/`, `skills/auto/`, các kết quả trong `results/`, `report/REPORT.md` và `report/table.md`.

**Ngân sách và mức ưu tiên**

| Loại lượt chạy | Số lượt tối thiểu |
|---|---:|
| Baseline trên ba tác vụ học và ba tác vụ đánh giá | 6 |
| Subagents trên ba tác vụ học và ba tác vụ đánh giá | 6 |
| Skills-auto thử trước đóng băng trên tập học | 3 |
| Skills-auto chính thức sau đóng băng trên cả hai tập | 6 |
| Tổng lượt chạy tác vụ | **21** |

Cộng thêm một lần gọi curator thông thường và lệnh thử mô hình; các lượt chạy lại làm tăng ngân sách. Dùng cùng mô hình, nhiệt độ và giới hạn đệ quy giữa các điều kiện để so sánh; ghi rõ mọi thay đổi. Ưu tiên test ngoại tuyến trước khi dùng API, chạy tuần tự và theo dõi token sau mỗi lượt. Không có hạn mức tiền/token cụ thể trong các tài liệu đã đọc, nên tự đặt mức phù hợp trước khi chạy thật.

Phân bổ ưu tiên theo RUBRIC: mã nguồn 30 điểm; tập học và phân loại lỗi 14; đa tác tử 10; curator và skill 16; bảng và đóng băng 10; báo cáo 20. Hoàn thành cả sáu hạng mục trước khi làm điểm thưởng.

Nếu còn thời gian và ngân sách, chọn hướng 6e: lặp mỗi điều kiện trên tập đánh giá ít nhất hai lần nữa, lưu bằng `--results` vào thư mục riêng, báo cáo trung bình và khoảng dao động. Hướng này cần thêm ít nhất **18 lượt tác vụ** và không trộn vào kết quả chính. Điểm thưởng tối đa +5, tổng điểm không vượt 100.

**Các nguyên tắc giữ thí nghiệm hợp lệ**

- Trước đóng băng, chỉ dùng dữ liệu tác vụ học để phát triển và tuyển chọn skill; giữ nội dung và kết quả đánh giá ngoài quá trình học để tránh rò rỉ.
- Không sửa tay skill tự sinh; không thay bộ skill đã đóng băng theo kết quả đánh giá.
- Không sửa workspace gốc hoặc các tệp được cung cấp sẵn để làm tăng điểm.
- Gắn mọi nhận xét với số liệu hoặc vết; phân biệt lỗi tác tử, lỗi hạ tầng và dao động ngẫu nhiên.
- Lưu kết quả cũ trước khi chạy lại cùng điều kiện vì runner ghi đè cùng đường dẫn.
