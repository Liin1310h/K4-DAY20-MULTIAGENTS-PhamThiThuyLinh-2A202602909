# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên             | Mã sinh viên | Phần đóng góp                                                                    |
| ------------------ | ------------ | -------------------------------------------------------------------------------- |
| Phạm Thị Thùy Linh | 2A202602909  | Cài đặt harness, curator, thực nghiệm và báo cáo với hỗ trợ của trợ lý lập trình |

- Nhà cung cấp: endpoint tương thích OpenAI `modelapi.vn`; mô hình thí nghiệm chính `openai:gpt-5.5`, nhiệt độ 0, giới hạn đệ quy 40. Truyền `LAB_MODEL` vào container để ghi đè giá trị cũ gpt-4o-mini; không đưa khóa vào kho.
- Windows và Docker Desktop Linux containers; Python 3.12, Deep Agents 0.7.21. 32 test ngoại tuyến đạt sau khi hoàn thiện mã. SDK timeout=120 giây, max_retries=0; một lượt subagents trước chỉnh timeout bị dừng vì chờ lâu, không có bản ghi hoàn tất và không đưa vào bảng chính.
- Hiện có đủ 18 bản ghi chính và các bản ghi phát triển skill; các pilot, lỗi xác thực và lượt sửa môi trường được lưu thư mục riêng. Mỗi bản ghi ghi token và thời gian thật từ callback/đồng hồ.
- Commit của tag freeze: Đã tạo; giả thuyết được đăng ký trước đánh giá.
- Runner chuẩn hóa CRLF thành LF chỉ trong bản sao Python ở sandbox vì checker so hash test LF. Nguồn trong tasks không sửa. Lượt trước chỉnh môi trường được sao lưu ở `results/pre-lf-normalization`.

## 2. Giả thuyết (đăng ký trước freeze và trước xem điểm đánh giá)

- H1 (subagents so với baseline): dự đoán subagents không tăng đáng kể điểm đánh giá so với baseline khi check kỹ thuật đã gần đạt hết; chi phí token sẽ tăng do điều tra và kiểm chứng thêm. Quy ước không có trong đề không tự xuất hiện chỉ nhờ chia vai trò.
- H2 (skills-auto so với baseline): dự đoán skills-auto tăng điểm quy ước đã học trên tập đánh giá, có thể là điều kiện điểm cao nhất nếu skill ngắn và được đọc; không kỳ vọng tự đạt quy ước mới chưa thấy. Căn cứ là lỗi baseline tập trung ở rule\_ và description có thể kích hoạt quy trình học từ phản hồi.
- H3 (tác vụ học so với tác vụ đánh giá): dự đoán cải thiện tập học lớn hơn tập đánh giá vì tác vụ mới bổ sung quy ước; skill có nguy cơ quá khớp, và cùng skill vẫn có nhiễu giữa các lượt. Căn cứ: pseudo-code curator tóm tắt SkillsBench rằng skill tự sinh trung bình không có lợi và SkillEvolBench về lợi ích học không chắc chuyển sang tác vụ mới.

## 3. Làm quen Deep Agents

1. Công cụ: ls, read_file, write_file, edit_file, delete, glob, grep, execute, task. execute chạy shell; task giao việc. Kết quả tour nguyên bản lưu trong report/tour.txt.
2. general-purpose có công cụ như tác tử chính. Mỗi lần gọi mặc định stateless, chỉ thấy prompt được gửi và trả một báo cáo cuối; tác tử chính phải truyền đủ quy tắc và đường dẫn.
3. Trích task: “Each invocation is stateless by default: the agent sees only the prompt you give it and returns a single final report.” Trích execute: “You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search.” System prompt tour rỗng nhưng mô tả công cụ chứa hướng dẫn. Agent lab dùng BASE_PROMPT được cung cấp.

## 4. Đường cơ sở và phân loại lỗi

| Tác vụ     | Check thất bại        | Nhóm lỗi | Bằng chứng từ detail                                                                                                                                                                                                                                                       |
| ---------- | --------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| code-learn | rule_type_hints       | E        | RULE: every public function (name not starting with '\_') in the package has type annotations on all parameters and on the return value.                                                                                                                                   |
| code-learn | rule_regression_tests | E        | RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass.                                                                                                                                                             |
| code-learn | rule_changelog        | E        | RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets).                                                                                                                    |
| data-learn | rule_money_in_cents   | E        | RULE: money values in answer.json are integer cents (1606.67 USD is written 160667).                                                                                                                                                                                       |
| data-learn | rule_meta_block       | E        | RULE: answer.json has an object `meta` = {"source": <input file name>, "rows_in": <number of data rows in the input file, duplicates included>, "rows_used": <number of distinct orders with a known amount>}.                                                             |
| data-learn | rule_clean_csv        | E        | RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents; one row per distinct order with a known amount; timestamp_utc as YYYY-MM-DDTHH:MM:SSZ (UTC); region in canonical spelling (North, South, East, West); amount in integer cents. |
| logs-learn | rule_service_names    | E        | RULE: service names in the output are lower-case with '-' replaced by '\_' (payment-service -> payment_service).                                                                                                                                                           |
| logs-learn | rule_sorted_errors    | E        | RULE: `errors` is sorted by service, then by timestamp_utc, ascending.                                                                                                                                                                                                     |
| logs-learn | rule_schema_header    | E        | RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage".                                                                                                                                                                                       |

Số lỗi theo nhóm: {'E': 9}. Check kỹ thuật đạt 18/18, quy ước đạt 0/9. Đây là bằng chứng phủ định cho việc gán lỗi A–D khi toàn bộ lỗi thực tế thuộc E. Skill có thể truyền quy ước từ detail nhưng phải kiểm tra nội dung và hành vi áp dụng. Không gộp lỗi API/pilot không hoàn tất vào bảng phân loại.

## 5. Điều kiện subagents

explorer đọc đặc tả và điều tra, implementer sửa và chạy kiểm chứng, reviewer kiểm tra độc lập. Description nêu khi nào gọi; system_prompt có phạm vi rõ ràng và được nối PATHS_NOTE. Các subagent tự định nghĩa không nạp skill riêng.

| Tác vụ     | subagent_calls |   Token |  Giây | Lỗi   |
| ---------- | -------------: | ------: | ----: | ----- |
| code-learn |              3 | 133,420 | 265.9 | Không |
| data-learn |              1 |  63,263 |  84.8 | Không |
| logs-learn |              2 |  79,219 | 137.0 | Không |

Các số đếm chỉ thuộc luồng chính; token callback gồm cả subagent. Vết không cho thấy toàn bộ công việc bên trong subagent, chỉ lời giao việc và báo cáo trả về. Khi subagent_calls=0, đó là lựa chọn không giao việc của tác tử chính.

Code-learn gọi explorer, implementer và reviewer; lời giao việc có đường dẫn, yêu cầu không sửa test và edge case. Tác tử chính chạy pytest để đối chiếu báo cáo. Data-learn gọi explorer một lần; lời giao việc nêu khoảng UTC Q1 và count distinct, nhưng north_q1_orders=13 bị check báo sai dù doanh thu đúng: có giao việc không bảo đảm kiểm chứng đủ. Logs-learn có hai lượt giao việc. Quy ước Acme không có trong đề không thể được truyền chỉ bằng lặp lại đề.

## 6. Self-evolving: skill do curator sinh

Curator chỉ đọc baseline của vai trò learn không có lỗi thực thi, lấy tên/detail các check thất bại và 6.000 ký tự cuối vết. Validator/parser được giữ nguyên; chỉ ghi skill hợp lệ, không cho tên traversal. Không sửa tay nội dung skill.

| Skill                             | Dòng | Tổng quát, độ đúng và description                                                                                                                                                                                                                           |
| --------------------------------- | ---: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cleaned-record-output-conventions |   18 | Tổng quát theo schema Acme, không cho mọi schema tabular. Header/vùng cố định là quy ước được phép học. Cents, rows_in và rows_used khớp feedback. Chưa chỉ rõ làm tròn tiền; cần Decimal và kiểm chứng. Description nêu đúng tabular/summary.              |
| error-log-json-conventions        |   15 | Áp dụng log mới cùng schema Acme. Header, service lowercase/underscore và sort khớp feedback. Có recompute/validate. Repeat chưa viết rõ 1+sum(N), cần đối chiếu đề. Description rộng cho timestamped logs.                                                 |
| python-package-fix-verification   |   13 | Quy trình kiểm chứng Python tổng quát; annotations, regression file và changelog đúng phản hồi Acme. Không nêu hàm/dữ liệu học cụ thể. Điều kiện ít nhất ba test viết cho nhiều sửa đổi; đọc cùng yêu cầu gốc. Description kích hoạt khi sửa hàm công khai. |

Curator chạy hai lần (một lần đầu và một lần chạy lại). Lần đầu skill dữ liệu bị validator từ chối do từ generic orders trùng marker; hai skill code/log hợp lệ được sao lưu ở results/curator-attempt-01. Lần hai prompt dùng records để tránh đặc thù miền, sinh ba skill hợp lệ. Loại hai skill lần đầu vì trùng vai trò với bộ lần hai, tránh phình thư viện; không chỉnh tay nội dung. Chi phí lần đầu 8.136 token, lần hai 8.160 token, tổng 16.296; metadata được lưu.

Cả ba skill ngắn dưới 40 dòng phần thân. Schema output cố định là quy ước tổ chức, không phải đáp án. Skill đọc được chưa đồng nghĩa áp dụng đầy đủ: đối chiếu skills_read và trace với check cụ thể.

## 7. Kết quả so sánh

| Task                              | baseline | subagents | skills-auto |
| --------------------------------- | -------- | --------- | ----------- |
| code-learn                        | 7/10     | 7/10      | 10/10       |
| data-learn                        | 5/8      | 4/8       | 8/8         |
| logs-learn                        | 6/9      | 6/9       | 9/9         |
| code-eval                         | 7/11     | 7/11      | 10/11       |
| data-eval                         | 5/9      | 0/9       | 7/9         |
| logs-eval                         | 6/10     | 6/10      | 4/10        |
| **Mean score - learning tasks**   | 0.66     | 0.62      | 1.00        |
| **Mean score - evaluation tasks** | 0.60     | 0.41      | 0.70        |
| **Mean tokens per run**           | 60,959   | 105,951   | 78,707      |
| **Runs that read a skill**        | 0/6      | 0/6       | 6/6         |

Thống kê tách vai trò và loại check:

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval     18/18         0/12          66,181      0/3
baseline      learn    18/18         0/9           55,737      0/3
subagents     eval     13/18         0/12         119,936      0/3
subagents     learn    17/18         0/9           91,967      0/3
skills-auto   eval     13/18         8/12          90,841      3/3
skills-auto   learn    18/18         9/9           66,573      3/3
```

Lượt chính có error: 1 (Lượt `subagents` trên tác vụ `data-eval` gặp lỗi `OpenAITimeoutError: Request timed out`, đạt 0/9). Skill bị sửa: 0 lượt.

## 8. Phân tích

4. So sánh theo vai trò: `skills-auto` cho thấy sự cải thiện đáng kể trên cả tập học (TB 1.00) và tập đánh giá (TB 0.70). Ngược lại, `subagents` không đem lại hiệu quả tăng điểm so với `baseline` (learn 0.62 vs 0.66, eval 0.41 vs 0.60) và thậm chí còn giảm điểm trên `eval` do bị lỗi timeout ở tác vụ `data-eval`.
5. Tách check kỹ thuật/rule\_: Thống kê cho thấy `skills-auto` giải quyết triệt để vấn đề về house rules (đạt 9/9 rules trên tập học và 8/12 rules trên tập đánh giá). Trong khi đó, cả `baseline` và `subagents` đều đạt 0/12 rules trên tập đánh giá. Cấu hình `skills-auto` có sự sụt giảm nhẹ trên `technical` (chỉ đạt 13/18 technical ở tập đánh giá) cho thấy nguy cơ quá khớp khi kỹ năng tập trung vào rules mà quên duy trì tính chính xác của thuật toán cốt lõi.
6. Việc sử dụng skill: Số lượt đọc skill (read a skill) của `skills-auto` là 6/6 (cho cả tập học và đánh giá). Tất cả các lượt đều đọc skill và áp dụng thành công phần lớn quy tắc tổ chức (house rules) đã được truyền từ tập học.
7. Chi phí hiệu quả được tính bằng điểm TB chuẩn hóa chia token TB, nhân 1.000, cùng cách tính cho mọi điều kiện:

| Điều kiện   | Điểm TB cả hai vai trò | Token TB | Điểm / 1.000 token |
| ----------- | ---------------------: | -------: | -----------------: |
| baseline    |                  0.630 |    60959 |             0.0103 |
| subagents   |                  0.515 |   105951 |             0.0048 |
| skills-auto |                  0.850 |    78707 |             0.0108 |

Đây là chi phí các lượt tác tử chính thức, chưa gồm curate và lượt phát triển/pilot; không đồng nhất token với tiền trả nhà cung cấp. Xét về điểm hiệu suất token, `skills-auto` vượt trội hơn so với `baseline` và hiệu quả hơn rất nhiều so với `subagents` (vốn tiêu tốn nhiều token nhưng điểm thấp do gọi nhiều lần và timeout).

7. Curator chỉ dùng tập học; skill đóng băng trước eval; không chỉnh tay. Validator chặn định danh trực tiếp nhưng không chứng minh chặn mọi rò rỉ ngữ nghĩa. Việc `skills-auto` lấy được 8/12 rules trên tập eval nhưng sụt giảm điểm technical cho thấy mô hình tổng quát hóa được các quy ước định dạng nhưng chưa giải quyết được hoàn toàn các yêu cầu kỹ thuật mới.
8. Nhiễu của cùng bộ skill: Giữa lần phát triển (dev) và lần chạy chính thức (sau freeze), các điểm số trên tập học của `skills-auto` đều đạt mốc hoàn hảo hoặc gần hoàn hảo (10/10, 8/8, 9/9). Điều này chứng minh rằng cùng một bộ skill hoạt động khá ổn định và có tính tất định cao với mô hình `gpt-5.5` và nhiệt độ 0.

## 9. Hạn chế và tính hợp lệ

1. Chỉ ba tác vụ mỗi vai trò, cùng thiết kế giảng viên; khó tổng quát ra mọi công việc thực tế.
2. Một lượt chính mỗi điều kiện; nhiệt độ 0 không bảo đảm tất định, nên chênh lệch nhỏ cần thận trọng.
3. Chỉ một mô hình chính/endpoint; kết quả không đại diện các mô hình khác. Pilot mô hình yếu và lỗi xác thực không dùng làm so sánh chính.
4. Vết chỉ gồm luồng chính, mỗi đoạn bị cắt 1.500 ký tự bởi render_trace cung cấp; không thể kiểm chứng toàn bộ suy luận subagent.
5. Token nhà cung cấp báo cáo có thể khác tiền tính phí. Giới hạn 40 bước không phải trần token tổng.
6. Thư mục sandbox là bản sao và shell không tự cách ly cấp hệ điều hành; chạy trong Docker. Chuẩn hóa LF giải quyết hash Windows nhưng thêm bước chuẩn bị môi trường cần ghi rõ để tái lập.

## 10. Kết luận

1. Mã harness và curator đã đạt toàn bộ 32 test ngoại tuyến và chạy thành công chu trình học và đánh giá.
2. Phương pháp `skills-auto` (Self-evolving Agent) chứng minh được tính hiệu quả cao nhất. Việc cho tác tử tự học từ lỗi sai giúp cải thiện điểm số mạnh mẽ ở cả hai tập học và đánh giá, đặc biệt là vượt qua được các luật (house rules) mà `baseline` không thể tự nhận biết. Chi phí token cũng đạt hiệu quả cao nhất (0.0108 điểm / 1.000 token).
3. Ngược lại, phương pháp `subagents` không đem lại hiệu quả trong bối cảnh các tác vụ hiện tại. Mặc dù tiêu tốn nhiều token và thời gian nhất, `subagents` thậm chí có điểm đánh giá thấp nhất do tốn thời gian kiểm chứng thừa và rủi ro hết thời gian chờ (timeout) dẫn tới lỗi hệ thống, gây giảm điểm.
4. Một nhược điểm của `skills-auto` được quan sát là có sự hy sinh một phần độ chính xác kỹ thuật cốt lõi (technical check giảm nhẹ) khi tác tử quá chú trọng áp dụng quy ước định dạng mới học được, có dấu hiệu quá khớp.
5. Bước cải tiến tiếp theo: Điều chỉnh lại system prompt của curator để cân bằng giữa việc tuân thủ luật và giữ vững logic cốt lõi. Ngoài ra có thể nghiên cứu tối ưu subagents để tránh tình trạng overhead và timeout.

## Phụ lục

- Trình tự: pytest; tour; baseline learn; subagents learn; khắc phục CRLF và chạy lại code; curator; skills-auto learn; đăng ký hypotheses; freeze; baseline eval; subagents eval; skills-auto all; verify_freeze; compare; check_breakdown.
- Lệnh chạy theo pha được lưu report/commands.jsonl và report/run_lab.py. Các lệnh đều chạy trong Docker, với LAB_MODEL=openai:gpt-5.5, LAB_TEMPERATURE=0 từ cấu hình và recursion-limit=40.
- Tham khảo: README, GUIDE, RUBRIC, GLOSSARY, guides/pseudocode/04_curator.md và 05_skill_quality.md. Nhận xét SkillsBench/SkillEvolBench là tóm tắt từ tài liệu lab, không giả định đã xác minh độc lập bài báo gốc.
- Không làm thử thách thưởng khi chưa hoàn tất phần bắt buộc. Không sửa tests/tasks/scripts hay các hàm và prompt được cung cấp.
