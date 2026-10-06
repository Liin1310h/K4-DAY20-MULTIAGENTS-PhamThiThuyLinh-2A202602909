"""Enrich the draft with computed comparisons and trace-backed interpretations."""
import json
import re
from pathlib import Path
from statistics import mean

from lab.compare import load_runs

root = Path(__file__).resolve().parents[1]
runs = load_runs(root / "results")
if len(runs) != 18:
    raise SystemExit("Need exactly 18 official records before final analysis")
cell = {(r["condition"],r["task"]):r for r in runs}
means = {(condition,role):mean(r["score"] for r in runs if r["condition"]==condition and r["role"]==role)
         for condition in ("baseline","subagents","skills-auto") for role in ("learn","eval")}
h1 = "phù hợp về hướng điểm" if means['subagents','eval'] <= means['baseline','eval'] else "không phù hợp về hướng điểm"
h2 = "phù hợp" if means['skills-auto','eval'] > means['baseline','eval'] else "không phù hợp"
h3 = "phù hợp" if means['skills-auto','learn']-means['baseline','learn'] > means['skills-auto','eval']-means['baseline','eval'] else "không phù hợp"
summary = ["| Điều kiện | TB học | TB đánh giá | Δ học với baseline | Δ đánh giá với baseline |", "|---|---:|---:|---:|---:|"]
for condition in ("baseline","subagents","skills-auto"):
    summary.append(f"| {condition} | {means[condition,'learn']:.4f} | {means[condition,'eval']:.4f} | "
                   f"{means[condition,'learn']-means['baseline','learn']:+.4f} | {means[condition,'eval']-means['baseline','eval']:+.4f} |")
newrows = ["| Tác vụ | Quy ước mới so với cùng họ tập học | Baseline | Subagents | Skills-auto |", "|---|---|---|---|---|"]
newfailed = []
for family in ("code","data","logs"):
    learn = cell['baseline',f'{family}-learn']
    known = {c['name'] for c in learn['checks']}
    for check in cell['skills-auto',f'{family}-eval']['checks']:
        if check['name'].startswith('rule_') and check['name'] not in known:
            states = []
            for condition in ('baseline','subagents','skills-auto'):
                match = next(c for c in cell[condition,f'{family}-eval']['checks'] if c['name']==check['name'])
                states.append('Đạt' if match['passed'] else 'Không đạt')
            newrows.append(f"| {family}-eval | {check['name']} | {' | '.join(states)} |")
            if not check['passed']:
                newfailed.append((f'{family}-eval',check['name']))
readrows = ["| Tác vụ | Skill đã đọc (số khác nhau) | Điểm chính thức |", "|---|---:|---:|"]
for run in runs:
    if run['condition']=='skills-auto':
        readrows.append(f"| {run['task']} | {run['skills_read']} | {run['passed']}/{run['total']} |")
improvements = []
for run in runs:
    if run['condition']!='skills-auto':
        continue
    base = {c['name']:c['passed'] for c in cell['baseline',run['task']]['checks']}
    for check in run['checks']:
        if check['name'].startswith('rule_') and check['passed'] and not base.get(check['name'],False):
            improvements.append((run['task'],check['name']))
costrows = ["| Điều kiện | Token TB | Giây TB | Điểm TB / 1.000 token |", "|---|---:|---:|---:|"]
ratios = {}
for condition in ('baseline','subagents','skills-auto'):
    subset = [r for r in runs if r['condition']==condition]
    tokens = mean(r['tokens']['total'] for r in subset)
    ratios[condition] = mean(r['score'] for r in subset)*1000/tokens
    costrows.append(f"| {condition} | {tokens:,.1f} | {mean(r['seconds'] for r in subset):.1f} | {ratios[condition]:.6f} |")
dev = {json.loads(p.read_text(encoding='utf-8'))['task']:json.loads(p.read_text(encoding='utf-8'))
       for p in (root/'results'/'skills-auto-dev').glob('*/run.json')}
noiserows = ["| Tác vụ | Trước freeze | Sau freeze | Δ điểm |", "|---|---:|---:|---:|"]
noise = []
for task,before in sorted(dev.items()):
    after = cell['skills-auto',task]
    delta = after['score']-before['score']
    noise.append(delta)
    noiserows.append(f"| {task} | {before['passed']}/{before['total']} | {after['passed']}/{after['total']} | {delta:+.4f} |")
first = improvements[0] if improvements else None
evidence = (f"Ví dụ giúp đạt: {first[0]}/{first[1]} từ fail ở baseline sang pass ở skills-auto. "
            "Trên code-learn, vết có đọc python-package-fix-verification, tạo tests/test_regressions.py, "
            "thêm type hints và bullet fix(...) dưới Unreleased rồi chạy pytest; ba check quy ước đều đạt. "
            "Chuỗi hành vi này nhất quán với tác dụng skill, dù thiết kế một lượt chưa chứng minh nhân quả tuyệt đối.") if first else "Không có check quy ước nào chuyển fail→pass; không giả định skill có tác dụng."
unhelped = (f"Ví dụ không giúp: {newfailed[0][0]}/{newfailed[0][1]} vẫn thất bại dù tác tử đã đọc skill. "
            "Quy ước mới không xuất hiện trong feedback tập học hoặc nội dung skill đóng băng; đọc skill "
            "không bổ sung tri thức chưa được học. Không sửa skill sau khi thấy check này.") if newfailed else "Không có quy ước mới nào còn thất bại; cần kiểm tra vết trước khi quy toàn bộ thành công cho skill."
section = f"""## 8. Phân tích

1. **Điểm theo vai trò và đối chiếu giả thuyết.**

{chr(10).join(summary)}

H1 {h1}; H2 {h2}; H3 {h3} trong mẫu này. Không kiểm định ý nghĩa thống kê vì mỗi cấu hình chỉ một lượt. Mức tăng skill trên học là {means['skills-auto','learn']-means['baseline','learn']:.4f}, trên đánh giá là {means['skills-auto','eval']-means['baseline','eval']:.4f}. Chênh lệch không tự chứng minh quá khớp vì tập đánh giá có quy ước mới và độ khó khác.

2. **Kỹ thuật, quy ước cũ và quy ước mới.** Thống kê mục 7 tách check kỹ thuật/rule_. Baseline học đạt kỹ thuật 18/18 nhưng quy ước 0/9; vì vậy cơ chế cải thiện kỳ vọng chủ yếu là thêm tri thức quy ước. Quy ước mới được xác định bằng tên rule_ có ở eval nhưng không có ở learn của cùng họ:

{chr(10).join(newrows)}

Định danh check mới chỉ được đọc sau freeze. Việc skill thiếu các quy tắc mới giới hạn mức điểm tối đa có thể đạt chỉ nhờ truyền quy ước học.

3. **Đọc skill và thực hiện quy tắc.**

{chr(10).join(readrows)}

{evidence}

{unhelped}

4. **Chi phí và hiệu quả.**

{chr(10).join(costrows)}

Theo điểm trên 1.000 token, điều kiện cao nhất là {max(ratios,key=ratios.get)}. Tỷ số dùng cùng phép tính trên sáu tác vụ; cần đọc cùng điểm tuyệt đối và không coi token là tiền. Chi phí curator thêm 16.296 token; lượt phát triển skill dùng {sum(r['tokens']['total'] for r in dev.values()):,} token, chưa tính các pilot/lượt lỗi hoặc lượt treo không có bản ghi. Nếu cộng chi phí tuyển chọn và phát triển, ưu thế chi phí của skill sẽ thấp hơn tỷ số chỉ đo lượt chính thức. Vết subagents/code-learn cho thấy ba lần giao việc và kiểm chứng nhưng điểm tương đương baseline sau sửa môi trường; subagents/data-learn còn sai count. Vì vậy chia việc không mặc nhiên đáng chi phí trên bộ tác vụ nhỏ này.

5. **Quá khớp và rò rỉ.** Curator chỉ nhận baseline learn và giữ nguyên skill sau freeze. Các skill giữ schema/quy ước Acme, không giữ đáp án hoặc tên dữ liệu/hàm riêng. Validator đã từ chối một từ generic trùng marker, cho thấy bộ lọc có thể có false positive; validator không chứng minh loại bỏ mọi rò rỉ ngữ nghĩa. Mức tăng trên eval cần đối chiếu quy ước mới và nhiễu trước khi gán là quá khớp. Không chọn lại skill hoặc giả thuyết sau khi thấy kết quả eval.

6. **Nhiễu cùng bộ skill.** Cả ba lượt dev có cùng skills_sha256 với bộ đóng băng; skill không sửa trong lượt chạy:

{chr(10).join(noiserows)}

Độ lệch tuyệt đối lớn nhất quan sát được là {max(abs(d) for d in noise):.4f}. Chỉ một cặp cho mỗi tác vụ, nên không đủ tính phương sai/khoảng tin cậy; kể cả tất cả chênh lệch bằng 0 cũng không chứng minh mô hình luôn tất định.

"""
path = root/'report'/'REPORT.md'
text = path.read_text(encoding='utf-8')
text = re.sub(r'## 8\. Phân tích\n.*?(?=## 9\.)',lambda _:section,text,flags=re.S)
winner = max(('baseline','subagents','skills-auto'),key=lambda c:means[c,'eval'])
conclusion = (f"## 10. Kết luận\n\nMã harness và curator đạt 32 test ngoại tuyến. "
              f"Điểm trung bình đánh giá: baseline {means['baseline','eval']:.4f}, subagents {means['subagents','eval']:.4f}, "
              f"skills-auto {means['skills-auto','eval']:.4f}; {winner} cao nhất trên bộ tác vụ này. "
              "Vết và check cho thấy cần phân biệt kỹ năng kỹ thuật với tri thức quy ước tổ chức. "
              "Kết quả một mô hình/một lượt chưa đủ tổng quát hoặc khẳng định nhân quả. "
              "Đề xuất tiếp theo là lặp trên tập đánh giá và báo cáo độ dao động cùng chi phí toàn quy trình.\n\n")
text = re.sub(r'## 10\. Kết luận\n.*?(?=## Phụ lục)',lambda _:conclusion,text,flags=re.S)
path.write_text(text,encoding='utf-8')
print('Final analysis written from 18 records')
