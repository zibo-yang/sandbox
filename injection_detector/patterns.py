"""Prompt injection detection patterns.

Each pattern is a dict with the following keys:
- name: short identifier for the pattern
- pattern: a regex string (case-insensitive matching is applied at runtime)
- severity: one of "low", "medium", or "high"
- description: human-readable explanation of what the pattern detects
"""
from __future__ import annotations

PATTERNS: list[dict] = [
    {
        "name": "ignore_previous_instructions",
        "pattern": r"ignore\s+(all\s+)?previous\s+instructions?",
        "severity": "high",
        "description": "Attempts to cancel prior instructions by telling the model to ignore them.",
    },
    {
        "name": "ignore_all_instructions",
        "pattern": r"ignore\s+all\s+(prior|earlier|above|preceding)?\s*instructions?",
        "severity": "high",
        "description": "Broad instruction-cancellation phrasing.",
    },
    {
        "name": "new_task_role_purpose",
        "pattern": r"your\s+(new\s+)?(task|role|purpose|goal|objective|job|mission)\s+is\b",
        "severity": "high",
        "description": "Attempts to redefine the model's task, role, or purpose.",
    },
    {
        "name": "do_not_follow_obey",
        "pattern": r"do\s+not\s+(follow|obey|comply\s+with|adhere\s+to)\s+(the\s+)?(previous|above|prior|original|system)?\s*instructions?",
        "severity": "high",
        "description": "Explicitly instructs the model not to follow its given instructions.",
    },
    {
        "name": "system_prompt_extraction",
        "pattern": r"(reveal|show|print|output|display|repeat|tell\s+me|share|leak|expose|give\s+me)\s+(your\s+)?(system\s+prompt|initial\s+prompt|original\s+instructions?|hidden\s+instructions?|confidential\s+prompt)",
        "severity": "high",
        "description": "Attempts to extract or expose the system prompt or hidden instructions.",
    },
    {
        "name": "respond_with_only",
        "pattern": r"(respond|reply|answer|output|say|write|print)\s+with\s+only\b",
        "severity": "medium",
        "description": "Restricts model output to a specific (often adversarial) string.",
    },
    {
        "name": "just_say",
        "pattern": r"(\bjust\s+(say|output|print|write|respond\s+with|reply\s+with)\b|\band\s+say\s+\w+)",
        "severity": "low",
        "description": "Subtly directs the model to produce a specific minimal output.",
    },
    {
        "name": "you_are_now",
        "pattern": r"\byou\s+are\s+now\s+(a\s+|an\s+)?(new\s+)?(\w+\s+)*(AI|assistant|bot|model|system|character|persona|agent)",
        "severity": "high",
        "description": "Role-reassignment attack that attempts to replace the model's identity.",
    },
    {
        "name": "disregard_instructions",
        "pattern": r"\bdisregard\s+(all\s+)?(previous|prior|above|earlier|your|the)?\s*(instructions?|guidelines?|rules?|constraints?|policies?|directives?)",
        "severity": "high",
        "description": "Tells the model to disregard its instructions or guidelines.",
    },
    {
        "name": "override_directives",
        "pattern": r"\b(override|overwrite|supersede|bypass|circumvent|neutralize)\s+(all\s+)?(previous|prior|above|your|the)?\s*(instructions?|directives?|constraints?|rules?|guidelines?|safeguards?|filters?)",
        "severity": "high",
        "description": "Uses override/bypass language to cancel safety instructions.",
    },
    {
        "name": "base64_instruction",
        "pattern": r"(?:[A-Za-z0-9+/]{40,}={0,2})",
        "severity": "medium",
        "description": "Detects suspiciously long Base64-encoded strings that may encode hidden instructions.",
    },
    {
        "name": "html_injection",
        "pattern": r"<\s*(script|iframe|object|embed|form|input|img|svg|meta|link|base)\b[^>]*>",
        "severity": "medium",
        "description": "HTML tags commonly used to inject scripts or alter rendering context.",
    },
    {
        "name": "markdown_link_injection",
        "pattern": r"\[([^\]]*)\]\s*\(\s*(javascript:|data:|vbscript:)[^\)]*\)",
        "severity": "high",
        "description": "Markdown links using dangerous URI schemes (javascript:, data:, vbscript:).",
    },
    {
        "name": "prompt_injection_marker",
        "pattern": r"###\s*(system|user|assistant|instruction|prompt)\s*###",
        "severity": "medium",
        "description": "Attempts to inject fake conversation-turn delimiters or system markers.",
    },
    {
        "name": "forget_previous",
        "pattern": r"\b(forget|erase|clear|reset|wipe)\s+(everything|all)?\s*(you('ve|\s+have))?\s*(been\s+)?(told|instructed|given|taught|trained)",
        "severity": "high",
        "description": "Instructs the model to forget or erase its prior context or training.",
    },
]
