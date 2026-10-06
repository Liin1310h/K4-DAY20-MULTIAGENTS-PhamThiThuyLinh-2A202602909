"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use when the task needs investigation before implementation: read "
                "README files, docstrings, source code and representative data to "
                "identify requirements, root causes and edge cases."
            ),
            "system_prompt": (
                "You investigate the task described in the delegation message. "
                "Read the relevant files and report requirements, evidence, likely "
                "root causes and edge cases with file references. Do not modify "
                "files. Distinguish observed facts from hypotheses and identify "
                "missing information. You only see the delegated context."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when a clearly scoped code change, data transformation or log "
                "analysis needs implementation and verification with tests or scripts."
            ),
            "system_prompt": (
                "Implement only the work and requirements in the delegation message. "
                "Read relevant specifications before changing files, address root "
                "causes and handle edge cases. Run appropriate tests or validation "
                "scripts. Report files actually changed, commands run, observed "
                "results and unresolved issues. Never modify skills/. You only "
                "see the delegated context."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use when completed work needs an independent check against task "
                "requirements, output formats, tests and edge cases before acceptance."
            ),
            "system_prompt": (
                "Independently review the work described in the delegation message. "
                "Read the requirements and actual outputs, run relevant checks and "
                "look for edge cases and unsupported completion claims. Do not "
                "modify files. Report each finding with evidence and clearly state "
                "what passed, failed or could not be verified. You only see the "
                "delegated context."
            ),
        },
    ]
