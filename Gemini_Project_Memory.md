Partnership Guidelines: Gemini CLI & User
1. Communication & Agency
Directives over Inquiries: If you want an action performed, phrase it as a command (e.g., "Install X," "Move Y"). If you ask "Can you...?", I may default to an explanation rather than execution.
Granting Initiative: When you tell me to "deal with it" or "have some agency," I will take the most direct technical path available, making informed assumptions about file paths and tool configurations.
Implicit Approval: For multi-step workflows (like the OCR pipeline), I will proceed autonomously once the primary objective and destination are confirmed.
2. Navigating the Android Filesystem
The "Internal Storage" Rule: Always remember that UI labels like "Internal Storage" must be translated to /sdcard/ for my shell tools to function.
Permission Persistence: Once termux-setup-storage is configured, I can scan common directories (DCIM, Pictures, Downloads), but specific app folders may require Shizuku-elevated shells which I cannot initiate alone.
Path Verification: If a path fails, I will proactively search for the correct system mount point before asking for clarification.
3. Automation & Tooling
Non-Interactive Execution: When installing packages (e.g., pkg install), I will use the -y flag to ensure the process doesn't hang on confirmation prompts.
Pipeline Engineering: I am most effective when combining several standard Linux utilities (find, grep, xargs, sed) into single-line "pipelines" to bypass workspace listing restrictions.
Tool Discovery: If a task requires a tool I don't have (like tesseract), I will identify, install, and configure it autonomously upon request.
4. Knowledge & Memory
GEMINI.md: This file serves as my "Long-term Project Memory." Use it to store architectural rules, path shortcuts, or preferred naming conventions.
Session Summaries: At the end of complex tasks, ask for a summary to ensure I have correctly indexed our achievements for the current session.

5. Project-Specific Paths
- OCR Source: /storage/emulated/0/DCIM/OCR
- Obsidian Vault: /storage/emulated/0/Obsidian Vault
- Obsidian OCR Log: /storage/emulated/0/Obsidian Vault/Extracted_OCR.md
- Screenshots: /storage/emulated/0/DCIM/Screenshots
- Bash Executable: /data/data/com.termux/files/usr/bin/bash
- Bash Config: /data/data/com.termux/files/home/.bashrc
- OCR Script: /data/data/com.termux/files/home/ocr_script.sh
- OCR Temp Dir: /data/data/com.termux/files/home/.gemini/tmp/ocr_process

6. Architectural & Technical Insights
- Preprocessing ROI: Mobile screenshots require upscaling (300%) and binarization (thresholding) via ImageMagick to achieve high-fidelity OCR with Tesseract.
- Storage Persistence: Use absolute paths (/storage/emulated/0/...) in scripts instead of symlinks to ensure cross-shell reliability.
- Context Bridges: Using gemini.md as a persistent path registry enables the CLI to maintain "project awareness" across separate sessions.