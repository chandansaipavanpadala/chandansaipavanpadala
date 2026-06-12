#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

# Reconfigure stdout to use UTF-8 to prevent encoding errors on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


def fetch_activity(username, token=None):
    url = f"https://api.github.com/users/{username}/events/public"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Python-Activity-Updater")
    
    if token:
        req.add_header("Authorization", f"Bearer {token}")
        
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        if e.code == 401:
            print("Please verify that your GH_PAT/token is valid and has read permissions.")
            if token:
                print("Retrying request without Authorization token...")
                return fetch_activity(username, token=None)
        return None
    except Exception as e:
        print(f"Failed to fetch events: {e}")
        return None

def format_event(event):
    # Parse event time
    # e.g., '2026-06-12T05:40:40Z'
    created_at = event.get("created_at", "")
    try:
        dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        date_str = dt.strftime("%b %d, %Y")
    except ValueError:
        date_str = created_at.split("T")[0] if "T" in created_at else created_at

    repo_name = event.get("repo", {}).get("name", "")
    repo_url = f"https://github.com/{repo_name}"
    event_type = event.get("type", "")
    payload = event.get("payload", {})

    if event_type == "PushEvent":
        commits = payload.get("commits", [])
        if commits:
            commit_msg = commits[0].get("message", "").split("\n")[0]
        else:
            commit_msg = "new commits"
        # truncate long commit messages
        if len(commit_msg) > 80:
            commit_msg = commit_msg[:77] + "..."
        return f"- Pushed to [{repo_name}]({repo_url}): {commit_msg} — {date_str}"

    elif event_type == "PullRequestEvent":
        action = payload.get("action", "opened")
        pr = payload.get("pull_request", {})
        pr_title = pr.get("title", "Pull Request")
        pr_url = pr.get("html_url", repo_url)
        return f"- {action.capitalize()} PR [#{pr.get('number', '')}]({pr_url}) in [{repo_name}]({repo_url}): {pr_title} — {date_str}"

    elif event_type == "IssuesEvent":
        action = payload.get("action", "opened")
        issue = payload.get("issue", {})
        issue_title = issue.get("title", "Issue")
        issue_url = issue.get("html_url", repo_url)
        return f"- {action.capitalize()} Issue [#{issue.get('number', '')}]({issue_url}) in [{repo_name}]({repo_url}): {issue_title} — {date_str}"

    elif event_type == "IssueCommentEvent":
        action = payload.get("action", "created")
        issue = payload.get("issue", {})
        comment = payload.get("comment", {})
        comment_url = comment.get("html_url", repo_url)
        return f"- {action.capitalize()} comment on Issue [#{issue.get('number', '')}]({comment_url}) in [{repo_name}]({repo_url}) — {date_str}"

    elif event_type == "CreateEvent":
        ref_type = payload.get("ref_type", "repository")
        ref = payload.get("ref", "")
        if ref_type == "repository":
            return f"- Created repository [{repo_name}]({repo_url}) — {date_str}"
        else:
            return f"- Created {ref_type} `{ref}` in [{repo_name}]({repo_url}) — {date_str}"

    elif event_type == "WatchEvent":
        return f"- Starred [{repo_name}]({repo_url}) — {date_str}"

    elif event_type == "ForkEvent":
        return f"- Forked [{repo_name}]({repo_url}) — {date_str}"

    else:
        # Generic fallback for other event types
        clean_type = event_type.replace("Event", "")
        return f"- Activity ({clean_type}) in [{repo_name}]({repo_url}) — {date_str}"

def update_readme(activity_lines):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(script_dir, "README.md")

    if not os.path.exists(readme_path):
        print(f"Error: README.md not found at {readme_path}")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- LATEST_ACTIVITY:START -->"
    end_marker = "<!-- LATEST_ACTIVITY:END -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Error: LATEST_ACTIVITY start/end comments not found in README.md")
        return

    activity_md = "\n" + "\n".join(activity_lines) + "\n"
    new_content = content[:start_idx + len(start_marker)] + activity_md + content[end_idx:]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md updated with latest activity.")

def main():
    username = "chandansaipavanpadala"
    token = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
    
    if token:
        print("Using Authorization token for GitHub API request.")
    else:
        print("Running unauthenticated. Rate limits may apply.")

    print(f"Fetching public events for user: {username}...")
    events = fetch_activity(username, token)
    
    if not events:
        print("No events fetched. Aborting update.")
        return

    print(f"Successfully fetched {len(events)} events. Processing activity...")
    
    # Process events and keep only the 5 most recent
    activity_lines = []
    seen_events = set()
    
    for event in events:
        if len(activity_lines) >= 5:
            break
            
        # Avoid duplicate consecutive pushes or identical watches to keep feed clean
        event_key = (event.get("type"), event.get("repo", {}).get("name"))
        if event.get("type") in ["WatchEvent", "PushEvent"] and event_key in seen_events:
            continue
            
        formatted = format_event(event)
        if formatted:
            activity_lines.append(formatted)
            seen_events.add(event_key)

    if not activity_lines:
        activity_lines.append("- _No recent public activity recorded._")

    print(f"Prepared {len(activity_lines)} activity items:")
    for line in activity_lines:
        print(line)

    update_readme(activity_lines)

if __name__ == "__main__":
    main()
