# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Phạm Thị Thùy Linh (theo tên kho) | 2A202602909 (theo tên kho) | Cài đặt harness, curator, thực nghiệm và báo cáo với hỗ trợ của trợ lý lập trình |

- Nhà cung cấp: endpoint tương thích OpenAI `modelapi.vn`; mô hình thí nghiệm chính `openai:gpt-5.5`, nhiệt độ 0, giới hạn đệ quy 40. Truyền `LAB_MODEL` vào container để ghi đè giá trị cũ gpt-4o-mini; không đưa khóa vào kho.
- Windows và Docker Desktop Linux containers; Python 3.12, Deep Agents 0.7.21. 32 test ngoại tuyến đạt sau khi hoàn thiện mã. SDK timeout=120 giây, max_retries=0; một lượt subagents trước chỉnh timeout bị dừng vì chờ lâu, không có bản ghi hoàn tất và không đưa vào bảng chính.
- Hiện có 6 bản ghi chính và 3 bản ghi phát triển skill; các pilot, lỗi xác thực và lượt sửa môi trường được lưu thư mục riêng. Mỗi bản ghi ghi token và thời gian thật từ callback/đồng hồ.
- Commit của tag freeze: Chưa tạo; giả thuyết được đăng ký trước đánh giá.
- Runner chuẩn hóa CRLF thành LF chỉ trong bản sao Python ở sandbox vì checker so hash test LF. Nguồn trong tasks không sửa. Lượt trước chỉnh môi trường được sao lưu ở `results/pre-lf-normalization`.

## 2. Giả thuyết (đăng ký trước freeze và trước xem điểm đánh giá)

- H1 (subagents so với baseline): dự đoán subagents không tăng đáng kể điểm đánh giá so với baseline khi check kỹ thuật đã gần đạt hết; chi phí token sẽ tăng do điều tra và kiểm chứng thêm. Quy ước không có trong đề không tự xuất hiện chỉ nhờ chia vai trò.
- H2 (skills-auto so với baseline): dự đoán skills-auto tăng điểm quy ước đã học trên tập đánh giá, có thể là điều kiện điểm cao nhất nếu skill ngắn và được đọc; không kỳ vọng tự đạt quy ước mới chưa thấy. Căn cứ là lỗi baseline tập trung ở rule_ và description có thể kích hoạt quy trình học từ phản hồi.
- H3 (tác vụ học so với tác vụ đánh giá): dự đoán cải thiện tập học lớn hơn tập đánh giá vì tác vụ mới bổ sung quy ước; skill có nguy cơ quá khớp, và cùng skill vẫn có nhiễu giữa các lượt. Căn cứ: pseudo-code curator tóm tắt SkillsBench rằng skill tự sinh trung bình không có lợi và SkillEvolBench về lợi ích học không chắc chuyển sang tác vụ mới.

## 3. Làm quen Deep Agents

1. Công cụ: ls, read_file, write_file, edit_file, delete, glob, grep, execute, task. execute chạy shell; task giao việc. Kết quả tour nguyên bản lưu trong report/tour.txt.
2. general-purpose có công cụ như tác tử chính. Mỗi lần gọi mặc định stateless, chỉ thấy prompt được gửi và trả một báo cáo cuối; tác tử chính phải truyền đủ quy tắc và đường dẫn.
3. Trích task: “Each invocation is stateless by default: the agent sees only the prompt you give it and returns a single final report.” Trích execute: “You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search.” System prompt tour rỗng nhưng mô tả công cụ chứa hướng dẫn. Agent lab dùng BASE_PROMPT được cung cấp.

## 4. Đường cơ sở và phân loại lỗi

| Tác vụ | Check thất bại | Nhóm lỗi | Bằng chứng từ detail |
|---|---|---|---|
| code-learn | rule_type_hints | E | RULE: every public function (name not starting with '_') in the package has type annotations on all parameters and on the return value. |
| code-learn | rule_regression_tests | E | RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass. |
| code-learn | rule_changelog | E | RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets). |
| data-learn | rule_money_in_cents | E | RULE: money values in answer.json are integer cents (1606.67 USD is written 160667). |
| data-learn | rule_meta_block | E | RULE: answer.json has an object `meta` = {"source": <input file name>, "rows_in": <number of data rows in the input file, duplicates included>, "rows_used": <number of distinct orders with a known amount>}. |
| data-learn | rule_clean_csv | E | RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents; one row per distinct order with a known amount; timestamp_utc as YYYY-MM-DDTHH:MM:SSZ (UTC); region in canonical spelling (North, South, East, West); amount in integer cents. |
| logs-learn | rule_service_names | E | RULE: service names in the output are lower-case with '-' replaced by '_' (payment-service -> payment_service). |
| logs-learn | rule_sorted_errors | E | RULE: `errors` is sorted by service, then by timestamp_utc, ascending. |
| logs-learn | rule_schema_header | E | RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage". |

Số lỗi theo nhóm: {'E': 9}. Check kỹ thuật đạt 18/18, quy ước đạt 0/9. Đây là bằng chứng phủ định cho việc gán lỗi A–D khi toàn bộ lỗi thực tế thuộc E. Skill có thể truyền quy ước từ detail nhưng phải kiểm tra nội dung và hành vi áp dụng. Không gộp lỗi API/pilot không hoàn tất vào bảng phân loại.

## 5. Điều kiện subagents

explorer đọc đặc tả và điều tra, implementer sửa và chạy kiểm chứng, reviewer kiểm tra độc lập. Description nêu khi nào gọi; system_prompt có phạm vi rõ ràng và được nối PATHS_NOTE. Các subagent tự định nghĩa không nạp skill riêng.

| Tác vụ | subagent_calls | Token | Giây | Lỗi |
|---|---:|---:|---:|---|
| code-learn | 3 | 133,420 | 265.9 | Không |
| data-learn | 1 | 63,263 | 84.8 | Không |
| logs-learn | 2 | 79,219 | 137.0 | Không |

Các số đếm chỉ thuộc luồng chính; token callback gồm cả subagent. Vết không cho thấy toàn bộ công việc bên trong subagent, chỉ lời giao việc và báo cáo trả về. Khi subagent_calls=0, đó là lựa chọn không giao việc của tác tử chính.

Code-learn gọi explorer, implementer và reviewer; lời giao việc có đường dẫn, yêu cầu không sửa test và edge case. Tác tử chính chạy pytest để đối chiếu báo cáo. Data-learn gọi explorer một lần; lời giao việc nêu khoảng UTC Q1 và count distinct, nhưng north_q1_orders=13 bị check báo sai dù doanh thu đúng: có giao việc không bảo đảm kiểm chứng đủ. Logs-learn có hai lượt giao việc. Quy ước Acme không có trong đề không thể được truyền chỉ bằng lặp lại đề.

## 6. Self-evolving: skill do curator sinh

Curator chỉ đọc baseline của vai trò learn không có lỗi thực thi, lấy tên/detail các check thất bại và 6.000 ký tự cuối vết. Validator/parser được giữ nguyên; chỉ ghi skill hợp lệ, không cho tên traversal. Không sửa tay nội dung skill.

| Skill | Dòng | Tổng quát, độ đúng và description |
|---|---:|---|
| cleaned-record-output-conventions | 18 | Tổng quát theo schema Acme, không cho mọi schema tabular. Header/vùng cố định là quy ước được phép học. Cents, rows_in và rows_used khớp feedback. Chưa chỉ rõ làm tròn tiền; cần Decimal và kiểm chứng. Description nêu đúng tabular/summary. |
| error-log-json-conventions | 15 | Áp dụng log mới cùng schema Acme. Header, service lowercase/underscore và sort khớp feedback. Có recompute/validate. Repeat chưa viết rõ 1+sum(N), cần đối chiếu đề. Description rộng cho timestamped logs. |
| python-package-fix-verification | 13 | Quy trình kiểm chứng Python tổng quát; annotations, regression file và changelog đúng phản hồi Acme. Không nêu hàm/dữ liệu học cụ thể. Điều kiện ít nhất ba test viết cho nhiều sửa đổi; đọc cùng yêu cầu gốc. Description kích hoạt khi sửa hàm công khai. |

Curator chạy hai lần (một lần đầu và một lần chạy lại). Lần đầu skill dữ liệu bị validator từ chối do từ generic orders trùng marker; hai skill code/log hợp lệ được sao lưu ở results/curator-attempt-01. Lần hai prompt dùng records để tránh đặc thù miền, sinh ba skill hợp lệ. Loại hai skill lần đầu vì trùng vai trò với bộ lần hai, tránh phình thư viện; không chỉnh tay nội dung. Chi phí lần đầu 8.136 token, lần hai 8.160 token, tổng 16.296; metadata được lưu.

Cả ba skill ngắn dưới 40 dòng phần thân. Schema output cố định là quy ước tổ chức, không phải đáp án. Skill đọc được chưa đồng nghĩa áp dụng đầy đủ: đối chiếu skills_read và trace với check cụ thể.

## 7. Kết quả so sánh

| Task | baseline | subagents |
|---|---|---|
| code-learn | 7/10 | 7/10 |
| data-learn | 5/8 | 4/8 |
| logs-learn | 6/9 | 6/9 |
| **Mean score - learning tasks** | 0.66 | 0.62 |
| **Mean score - evaluation tasks** | - | - |
| **Mean tokens per run** | 55,737 | 91,967 |
| **Runs that read a skill** | 0/3 | 0/3 |

Thống kê tách vai trò và loại check:

```text
baseline     learn score=0.6639 technical=18/18 rules=0/9 tokens=55737.7 read=0/3
subagents    learn score=0.6222 technical=17/18 rules=0/9 tokens=91967.3 read=0/3
```

Lượt chính có error: 0. Không có lỗi thực thi trong các bản ghi chính hiện có. Các lượt lỗi xác thực/pilot giữ riêng, không trộn vào bảng. Skill bị sửa: 0 lượt.

## 8. Phân tích

1. So sánh theo vai trò dùng điểm TB ở bảng mục 7; không gộp lợi ích học với tổng quát hóa. Các nhận xét cơ chế bổ sung dựa trên vết sau khi đủ kết quả.
2. Tách check kỹ thuật/rule_ theo thống kê mục 7; quy ước mới phải đối chiếu từng check eval sau freeze. Không sửa skill dựa trên check eval.
3. Việc sử dụng skill được đánh giá qua số lượt read và vết; chọn check chuyển từ fail sang pass và check còn fail để giải thích bằng quy tắc có/thiếu trong skill.
4. Chi phí hiệu quả được tính bằng điểm TB chuẩn hóa chia token TB, nhân 1.000, cùng cách tính cho mọi điều kiện:

| Điều kiện | Điểm TB cả hai vai trò | Token TB | Điểm / 1.000 token |
|---|---:|---:|---:|
| baseline | 0.6639 | 55737.7 | 0.011911 |
| subagents | 0.6222 | 91967.3 | 0.006766 |

Đây là chi phí các lượt tác tử chính thức, chưa gồm curate và lượt phát triển/pilot; không đồng nhất token với tiền trả nhà cung cấp.

5. Curator chỉ dùng tập học; skill đóng băng trước eval; không chỉnh tay. Validator chặn định danh trực tiếp nhưng không chứng minh chặn mọi rò rỉ ngữ nghĩa. Chênh lệch học/eval có thể do độ khó hoặc quy ước mới, không đủ tự kết luận quá khớp.
6. Nhiễu của cùng bộ skill:

| Tác vụ | Trước freeze | Sau freeze | Chênh lệch điểm chuẩn hóa |
|---|---:|---:|---:|

Một cặp lặp chỉ là bằng chứng dao động, chưa ước lượng phương sai hoặc khoảng tin cậy.

## 9. Hạn chế và tính hợp lệ

1. Chỉ ba tác vụ mỗi vai trò, cùng thiết kế giảng viên; khó tổng quát ra mọi công việc thực tế.
2. Một lượt chính mỗi điều kiện; nhiệt độ 0 không bảo đảm tất định, nên chênh lệch nhỏ cần thận trọng.
3. Chỉ một mô hình chính/endpoint; kết quả không đại diện các mô hình khác. Pilot mô hình yếu và lỗi xác thực không dùng làm so sánh chính.
4. Vết chỉ gồm luồng chính, mỗi đoạn bị cắt 1.500 ký tự bởi render_trace cung cấp; không thể kiểm chứng toàn bộ suy luận subagent.
5. Token nhà cung cấp báo cáo có thể khác tiền tính phí. Giới hạn 40 bước không phải trần token tổng.
6. Thư mục sandbox là bản sao và shell không tự cách ly cấp hệ điều hành; chạy trong Docker. Chuẩn hóa LF giải quyết hash Windows nhưng thêm bước chuẩn bị môi trường cần ghi rõ để tái lập.

## 10. Kết luận

Mã harness và curator đã đạt toàn bộ 32 test ngoại tuyến. Các kết luận về hiệu quả phải căn cứ bảng chính và vết thay vì chỉ sự hiện diện skill/subagent. Không coi kết quả âm là lỗi thí nghiệm. Bước cải tiến tiếp theo là lặp trên tác vụ đánh giá để ước lượng nhiễu và kiểm tra quy ước mới.

## Phụ lục

- Trình tự: pytest; tour; baseline learn; subagents learn; khắc phục CRLF và chạy lại code; curator; skills-auto learn; đăng ký hypotheses; freeze; baseline eval; subagents eval; skills-auto all; verify_freeze; compare; check_breakdown.
- Lệnh chạy theo pha được lưu report/commands.jsonl và report/run_lab.py. Các lệnh đều chạy trong Docker, với LAB_MODEL=openai:gpt-5.5, LAB_TEMPERATURE=0 từ cấu hình và recursion-limit=40.
- Tham khảo: README, GUIDE, RUBRIC, GLOSSARY, guides/pseudocode/04_curator.md và 05_skill_quality.md. Nhận xét SkillsBench/SkillEvolBench là tóm tắt từ tài liệu lab, không giả định đã xác minh độc lập bài báo gốc.
- Không làm thử thách thưởng khi chưa hoàn tất phần bắt buộc. Không sửa tests/tasks/scripts hay các hàm và prompt được cung cấp.
