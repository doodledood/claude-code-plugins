# X Interface Reference

Operational reference for interacting with X (Twitter) via claude-in-chrome MCP tools.

## Character Limits

| Tier | Post Limit | Reply Limit | URL Length |
|------|-----------|-------------|------------|
| Free | 280 chars | 280 chars | 23 chars (t.co shortening) |
| Premium | 25,000 chars | 25,000 chars | 23 chars (t.co shortening) |

All URLs are shortened to 23 characters via t.co regardless of actual length. Count 23 chars per URL when calculating reply length.

## Chrome Tool Patterns

### Page Navigation

```
# Navigate to URL
mcp__chrome-devtools__navigate_page(type: "url", url: "https://x.com/home")

# Navigate back
mcp__chrome-devtools__navigate_page(type: "back")
```

### Reading Page Content

```
# Text snapshot of page (preferred — faster, structured)
mcp__chrome-devtools__take_snapshot()

# Screenshot for visual verification
mcp__chrome-devtools__take_screenshot()
```

Use snapshots to read post text, engagement metrics (likes, retweets, views, replies), and identify interactive elements by uid. Use screenshots when visual context is needed (images, layout verification).

### Scrolling the Feed

```
# Scroll down through feed — use uid of a visible element, or coordinate-free scroll via keyboard
mcp__chrome-devtools__press_key(key: "Space")      # scroll down one viewport
mcp__chrome-devtools__press_key(key: "Shift+Space") # scroll up one viewport
```

Or target a specific scrollable container element.

### Getting Post Permalink URLs

Post permalink format: `https://x.com/{username}/status/{tweet_id}`

To capture a permalink:
1. Take a snapshot to identify the post
2. Look for the timestamp link element (e.g., "2h", "44m") — clicking it navigates to the permalink
3. Alternatively, look for the post's link elements in the snapshot — the status URL is often present as an `<a>` element
4. The URL is visible in the browser address bar after navigating to the post

### Clicking Into Posts

```
# Click on a post element by uid from snapshot
mcp__chrome-devtools__click(uid: "ref_123")
```

### Reading Post Details

After navigating to a post's permalink page, take a snapshot to read:
- Full post text
- Author name and handle
- Engagement metrics (likes, retweets, replies, views/impressions)
- Existing reply threads
- Whether the post contains images/video (described in snapshot)

## Typing Replies — JS Injection (Required Workaround)

**X keyboard shortcuts intercept normal typing.** The `fill` tool and direct keyboard input trigger X's global shortcut handler — the "e" key navigates to Explore, other keys trigger other actions. This causes navigation away from the tweet page instead of text entry.

**Always use JavaScript injection to type reply text:**

```javascript
// Use via mcp__chrome-devtools__evaluate_script
() => {
  const replyBox = document.querySelector('[data-testid="tweetTextarea_0"]');
  if (replyBox) {
    replyBox.focus();
    document.execCommand('insertText', false, 'YOUR REPLY TEXT HERE');
    return 'Text inserted successfully';
  }
  // Fallback: find any contenteditable element
  const editables = document.querySelectorAll('[contenteditable="true"]');
  return 'Reply box not found. Contenteditable elements: ' +
    JSON.stringify(Array.from(editables).map(e => e.className).slice(0, 5));
}
```

**Why this works:** `execCommand('insertText')` inserts text at the cursor position and triggers React's synthetic change events (X uses React/Draft.js). It does NOT fire keydown/keyup events that X's shortcut handler listens to.

**Key details:**
- Selector: `[data-testid="tweetTextarea_0"]`
- Must call `replyBox.focus()` before `execCommand`
- `execCommand('insertText')` triggers React change handlers (unlike setting `innerText`/`textContent` directly)
- URL preview cards generate automatically after text insertion if the reply contains a URL

## Reply Posting Workflow

1. **Navigate** to the tweet permalink URL
2. **Wait** for page load (take snapshot to verify)
3. **Find reply field** — look for "Post your reply" or the reply compose area in the snapshot
4. **Click** the reply field to expand it (it starts collapsed as a single line)
5. **Wait** briefly for the reply editor to expand (shows "Replying to @username")
6. **Inject text** using the JS injection pattern above
7. **Verify** — take screenshot to confirm text content and any link preview cards
8. **Click Reply button** — find the "Reply" or "Post" button in the snapshot and click it
9. **Verify** — take screenshot to confirm successful posting (look for your reply appearing with "now" or "1s" timestamp)

## Error States to Detect

| State | Indicators | Action |
|-------|-----------|--------|
| Login wall | "Sign in" prompt, redirect to login page | Escalate to user |
| Rate limit | "Rate limit exceeded" message, 429 responses | Escalate — wait or switch account |
| Error page | "Something went wrong", "Try again" | Retry once, then escalate |
| CAPTCHA | Challenge prompt, "verify you're human" | Escalate to user |
| Protected account | "These posts are protected" | Skip this post, log as skipped |
| Suspended/deleted post | "This post is unavailable" | Skip, log as unavailable |
| Reply restrictions | "Who can reply?" restrictions | Skip if restricted, log reason |
