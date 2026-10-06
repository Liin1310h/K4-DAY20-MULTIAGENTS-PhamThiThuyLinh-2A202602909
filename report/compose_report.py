"""Build a reproducible report from real run records; never invent missing results."""
import json
import subprocess
from collections import Counter
from pathlib import Path
from statistics import mean

from lab.compare import build_table, load_runs

root = Path(__file__).resolve().parents[1]
runs = load_runs(root / "results")
dev = [json.loads(p.read_text(encoding="utf-8")) for p in
       (root / "results" / "skills-auto-dev").glob("*/run.json")]
skills = list((root / "skills" / "auto").glob("*/SKILL.md"))
tag = subprocess.run(["git", "rev-parse", "freeze"], cwd=root, capture_output=True, text=True)
freeze = tag.stdout.strip() if tag.returncode == 0 else "Chưa tạo; giả thuyết được đăng ký trước đánh giá."
def md(text):
    return str(text).replace("|", "\\|").replace("\n", " ")
def group(check):
    if check["name"].startswith("rule_"):
        return "E"
    if check["name"] == "tests_not_modified":
        return "A"
    return "D" if any(s in check["name"] for s in ("timestamp", "repeat", "exception", "count")) else "G"

learning = [r for r in runs if r["condition"] == "baseline" and r["role"] == "learn" and not r["error"]]
failures = [(r, c) for r in learning for c in r["checks"] if not c["passed"]]
taxonomy = ["| Tác vụ | Check thất bại | Nhóm lỗi | Bằng chứng từ detail |", "|---|---|---|---|"]
taxonomy += [f"| {r['task']} | {c['name']} | {group(c)} | {md(c.get('detail',''))} |" for r,c in failures]
technical = [c for r in learning for c in r["checks"] if not c["name"].startswith("rule_")]
rules = [c for r in learning for c in r["checks"] if c["name"].startswith("rule_")]
counts = Counter(group(c) for _, c in failures)
subrows = ["| Tác vụ | subagent_calls | Token | Giây | Lỗi |", "|---|---:|---:|---:|---|"]
subrows += [f"| {r['task']} | {r['subagent_calls']} | {r['tokens']['total']:,} | {r['seconds']} | {md(r['error'] or 'Không')} |"
            for r in runs if r["condition"] == "subagents"]
skillrows = ["| Skill | Dòng | Tổng quát, độ đúng và description |", "|---|---:|---|"]
assessments = {
    "python-package-fix-verification": "Quy trình kiểm chứng Python tổng quát; annotations, regression file và changelog đúng phản hồi Acme. Không nêu hàm/dữ liệu học cụ thể. Điều kiện ít nhất ba test viết cho nhiều sửa đổi; đọc cùng yêu cầu gốc. Description kích hoạt khi sửa hàm công khai.",
    "cleaned-record-output-conventions": "Tổng quát theo schema Acme, không cho mọi schema tabular. Header/vùng cố định là quy ước được phép học. Cents, rows_in và rows_used khớp feedback. Chưa chỉ rõ làm tròn tiền; cần Decimal và kiểm chứng. Description nêu đúng tabular/summary.",
    "error-log-json-conventions": "Áp dụng log mới cùng schema Acme. Header, service lowercase/underscore và sort khớp feedback. Có recompute/validate. Repeat chưa viết rõ 1+sum(N), cần đối chiếu đề. Description rộng cho timestamped logs.",
}
for path in skills:
    text = path.read_text(encoding="utf-8")
    description = next((s.split(":",1)[1].strip() for s in text.splitlines() if s.startswith("description:")), "")
    skillrows.append(f"| {path.parent.name} | {len(text.splitlines())} | {md(assessments.get(path.parent.name,description))} |")
stats = []
for condition in ("baseline", "subagents", "skills-auto"):
    for role in ("learn", "eval"):
        subset = [r for r in runs if r["condition"] == condition and r["role"] == role]
        if not subset:
            continue
        tech = [c for r in subset for c in r["checks"] if not c["name"].startswith("rule_")]
        rule = [c for r in subset for c in r["checks"] if c["name"].startswith("rule_")]
        stats.append(f"{condition:12} {role:5} score={mean(r['score'] for r in subset):.4f} "
                     f"technical={sum(c['passed'] for c in tech)}/{len(tech)} "
                     f"rules={sum(c['passed'] for c in rule)}/{len(rule)} "
                     f"tokens={mean(r['tokens']['total'] for r in subset):.1f} "
                     f"read={sum(r['skills_read'] > 0 for r in subset)}/{len(subset)}")
noise = ["| Tác vụ | Trước freeze | Sau freeze | Chênh lệch điểm chuẩn hóa |", "|---|---:|---:|---:|"]
for before in dev:
    after = next((r for r in runs if r["condition"] == "skills-auto" and r["task"] == before["task"]), None)
    if after:
        noise.append(f"| {before['task']} | {before['passed']}/{before['total']} | {after['passed']}/{after['total']} | {after['score']-before['score']:+.4f} |")
cost = ["| Điều kiện | Điểm TB cả hai vai trò | Token TB | Điểm / 1.000 token |", "|---|---:|---:|---:|"]
for condition in ("baseline", "subagents", "skills-auto"):
    subset = [r for r in runs if r["condition"] == condition]
    if subset:
        score = mean(r["score"] for r in subset)
        tokens = mean(r["tokens"]["total"] for r in subset)
        cost.append(f"| {condition} | {score:.4f} | {tokens:.1f} | {1000*score/tokens if tokens else 0:.6f} |")
errors = [f"- {r['condition']}/{r['task']}: {md(r['error'])}" for r in runs if r['error']]
report = f"""# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Phạm Thị Thùy Linh (theo tên kho) | 2A202602909 (theo tên kho) | Cài đặt harness, curator, thực nghiệm và báo cáo với hỗ trợ của trợ lý lập trình |

- Nhà cung cấp: endpoint tương thích OpenAI `modelapi.vn`; mô hình thí nghiệm chính `openai:gpt-5.5`, nhiệt độ 0, giới hạn đệ quy 40. Truyền `LAB_MODEL` vào container để ghi đè giá trị cũ gpt-4o-mini; không đưa khóa vào kho.
- Windows và Docker Desktop Linux containers; Python 3.12, Deep Agents 0.7.21. 32 test ngoại tuyến đạt sau khi hoàn thiện mã. SDK timeout=120 giây, max_retries=0; một lượt subagents trước chỉnh timeout bị dừng vì chờ lâu, không có bản ghi hoàn tất và không đưa vào bảng chính.
- Hiện có {len(runs)} bản ghi chính và {len(dev)} bản ghi phát triển skill; các pilot, lỗi xác thực và lượt sửa môi trường được lưu thư mục riêng. Mỗi bản ghi ghi token và thời gian thật từ callback/đồng hồ.
- Commit của tag freeze: {freeze}
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

{chr(10).join(taxonomy)}

Số lỗi theo nhóm: {dict(counts)}. Check kỹ thuật đạt {sum(c['passed'] for c in technical)}/{len(technical)}, quy ước đạt {sum(c['passed'] for c in rules)}/{len(rules)}. Đây là bằng chứng phủ định cho việc gán lỗi A–D khi toàn bộ lỗi thực tế thuộc E. Skill có thể truyền quy ước từ detail nhưng phải kiểm tra nội dung và hành vi áp dụng. Không gộp lỗi API/pilot không hoàn tất vào bảng phân loại.

## 5. Điều kiện subagents

explorer đọc đặc tả và điều tra, implementer sửa và chạy kiểm chứng, reviewer kiểm tra độc lập. Description nêu khi nào gọi; system_prompt có phạm vi rõ ràng và được nối PATHS_NOTE. Các subagent tự định nghĩa không nạp skill riêng.

{chr(10).join(subrows)}

Các số đếm chỉ thuộc luồng chính; token callback gồm cả subagent. Vết không cho thấy toàn bộ công việc bên trong subagent, chỉ lời giao việc và báo cáo trả về. Khi subagent_calls=0, đó là lựa chọn không giao việc của tác tử chính.

Code-learn gọi explorer, implementer và reviewer; lời giao việc có đường dẫn, yêu cầu không sửa test và edge case. Tác tử chính chạy pytest để đối chiếu báo cáo. Data-learn gọi explorer một lần; lời giao việc nêu khoảng UTC Q1 và count distinct, nhưng north_q1_orders=13 bị check báo sai dù doanh thu đúng: có giao việc không bảo đảm kiểm chứng đủ. Logs-learn có hai lượt giao việc. Quy ước Acme không có trong đề không thể được truyền chỉ bằng lặp lại đề.

## 6. Self-evolving: skill do curator sinh

Curator chỉ đọc baseline của vai trò learn không có lỗi thực thi, lấy tên/detail các check thất bại và 6.000 ký tự cuối vết. Validator/parser được giữ nguyên; chỉ ghi skill hợp lệ, không cho tên traversal. Không sửa tay nội dung skill.

{chr(10).join(skillrows)}

Curator chạy hai lần (một lần đầu và một lần chạy lại). Lần đầu skill dữ liệu bị validator từ chối do từ generic orders trùng marker; hai skill code/log hợp lệ được sao lưu ở results/curator-attempt-01. Lần hai prompt dùng records để tránh đặc thù miền, sinh ba skill hợp lệ. Loại hai skill lần đầu vì trùng vai trò với bộ lần hai, tránh phình thư viện; không chỉnh tay nội dung. Chi phí lần đầu 8.136 token, lần hai 8.160 token, tổng 16.296; metadata được lưu.

Cả ba skill ngắn dưới 40 dòng phần thân. Schema output cố định là quy ước tổ chức, không phải đáp án. Skill đọc được chưa đồng nghĩa áp dụng đầy đủ: đối chiếu skills_read và trace với check cụ thể.

## 7. Kết quả so sánh

{build_table(runs)}

Thống kê tách vai trò và loại check:

```text
{chr(10).join(stats)}
```

Lượt chính có error: {len(errors)}. {chr(10).join(errors) if errors else 'Không có lỗi thực thi trong các bản ghi chính hiện có.'} Các lượt lỗi xác thực/pilot giữ riêng, không trộn vào bảng. Skill bị sửa: {sum(bool(r['skills_modified']) for r in runs)} lượt.

## 8. Phân tích

1. So sánh theo vai trò dùng điểm TB ở bảng mục 7; không gộp lợi ích học với tổng quát hóa. Các nhận xét cơ chế bổ sung dựa trên vết sau khi đủ kết quả.
2. Tách check kỹ thuật/rule_ theo thống kê mục 7; quy ước mới phải đối chiếu từng check eval sau freeze. Không sửa skill dựa trên check eval.
3. Việc sử dụng skill được đánh giá qua số lượt read và vết; chọn check chuyển từ fail sang pass và check còn fail để giải thích bằng quy tắc có/thiếu trong skill.
4. Chi phí hiệu quả được tính bằng điểm TB chuẩn hóa chia token TB, nhân 1.000, cùng cách tính cho mọi điều kiện:

{chr(10).join(cost)}

Đây là chi phí các lượt tác tử chính thức, chưa gồm curate và lượt phát triển/pilot; không đồng nhất token với tiền trả nhà cung cấp.

5. Curator chỉ dùng tập học; skill đóng băng trước eval; không chỉnh tay. Validator chặn định danh trực tiếp nhưng không chứng minh chặn mọi rò rỉ ngữ nghĩa. Chênh lệch học/eval có thể do độ khó hoặc quy ước mới, không đủ tự kết luận quá khớp.
6. Nhiễu của cùng bộ skill:

{chr(10).join(noise)}

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
"""
(root / "report" / "REPORT.md").write_text(report, encoding="utf-8")
(root / "report" / "table.md").write_text(build_table(runs) + "\n", encoding="utf-8")
print("Wrote report with", len(runs), "official records and", len(dev), "development records")
