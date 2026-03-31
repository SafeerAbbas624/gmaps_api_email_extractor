"""
Generate email_preview.html from email_messages.py.

Usage:
    python generate_preview.py          # one-shot generation
    python generate_preview.py --watch  # auto-regenerate whenever email_messages.py is saved
"""

import os
import sys
import json
import re
import time

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(WORKSPACE, 'email_messages.py')
OUTPUT = os.path.join(WORKSPACE, 'email_preview.html')

# Marker that locates the start of the emails array in the HTML
EMAILS_START_MARKER = '// Email messages data\n        const emails = '

# One-time migration: replace the hardcoded plain-text placeholder with the dynamic version
PLAIN_TEXT_PLACEHOLDER = '<div class="email-plain">Plain text version would appear here</div>'
PLAIN_TEXT_DYNAMIC     = "<div class=\"email-plain\">${email.plain || ''}</div>"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_messages():
    """Import EMAIL_MESSAGES fresh from email_messages.py (no cache)."""
    if 'email_messages' in sys.modules:
        del sys.modules['email_messages']
    if WORKSPACE not in sys.path:
        sys.path.insert(0, WORKSPACE)
    import email_messages
    return email_messages.EMAIL_MESSAGES


def build_emails_js(messages):
    """Serialize EMAIL_MESSAGES as a JS array literal (properly JSON-escaped)."""
    entries = []
    for msg in messages:
        subject   = json.dumps(msg.get('subject', ''))
        html_val  = json.dumps(msg.get('html',    ''))
        plain_val = json.dumps(msg.get('plain',   ''))
        entries.append(
            '            {\n'
            f'                subject: {subject},\n'
            f'                html: {html_val},\n'
            f'                plain: {plain_val}\n'
            '            }'
        )
    return '[\n' + ',\n'.join(entries) + '\n        ]'


def find_array_end(html, start):
    """
    Return the index of the closing ] of the JS array that begins at `start`.
    Handles nested arrays/objects and double-quoted strings with escape sequences.
    """
    depth     = 0
    in_string = False
    escaped   = False
    i = start
    while i < len(html):
        ch = html[i]
        if escaped:
            escaped = False
        elif in_string:
            if   ch == '\\': escaped   = True
            elif ch == '"':  in_string = False
        else:
            if   ch == '"':           in_string = True
            elif ch in ('[', '{'):    depth += 1
            elif ch in (']', '}'):
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


# ---------------------------------------------------------------------------
# Core generation
# ---------------------------------------------------------------------------

def generate():
    """Read email_messages.py and rewrite the data block in email_preview.html."""
    messages  = load_messages()
    emails_js = build_emails_js(messages)

    with open(OUTPUT, 'r', encoding='utf-8') as f:
        html = f.read()

    # --- 1. Replace const emails = [...] ---
    marker_idx = html.find(EMAILS_START_MARKER)
    if marker_idx == -1:
        raise ValueError(f"Marker not found in {OUTPUT}.\n"
                         f"Expected: {EMAILS_START_MARKER!r}")

    array_start = marker_idx + len(EMAILS_START_MARKER)
    array_end   = find_array_end(html, array_start)
    if array_end == -1:
        raise ValueError(f"Could not locate end of emails array in {OUTPUT}")

    html = html[:array_start] + emails_js + html[array_end + 1:]

    # --- 2. Migrate plain-text placeholder (once; idempotent after first run) ---
    html = html.replace(PLAIN_TEXT_PLACEHOLDER, PLAIN_TEXT_DYNAMIC)

    # --- 3. Keep stats counters in sync ---
    count = str(len(messages))
    html = re.sub(
        r'(<div class="stat-label">Total Messages</div>\s*<div class="stat-value">)\d+(</div>)',
        rf'\g<1>{count}\g<2>', html
    )
    html = re.sub(
        r'(<div class="stat-label">Unique Subjects</div>\s*<div class="stat-value">)\d+(</div>)',
        rf'\g<1>{count}\g<2>', html
    )

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'[generate_preview] email_preview.html updated  ({len(messages)} messages)')


# ---------------------------------------------------------------------------
# Watch mode
# ---------------------------------------------------------------------------

def watch():
    """Poll email_messages.py; regenerate HTML whenever it is saved."""
    print(f'[generate_preview] Watching:  {SOURCE}')
    print(f'[generate_preview] Output:    {OUTPUT}')
    print('[generate_preview] Press Ctrl+C to stop.\n')

    last_mtime = None
    while True:
        try:
            mtime = os.stat(SOURCE).st_mtime
            if mtime != last_mtime:
                if last_mtime is not None:         # skip the very first run's "change"
                    print('[generate_preview] Change detected — regenerating...')
                generate()
                last_mtime = mtime
            time.sleep(1)
        except KeyboardInterrupt:
            print('\n[generate_preview] Stopped.')
            break
        except Exception as exc:
            print(f'[generate_preview] Error: {exc}')
            time.sleep(2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    if '--watch' in sys.argv:
        watch()
    else:
        generate()
