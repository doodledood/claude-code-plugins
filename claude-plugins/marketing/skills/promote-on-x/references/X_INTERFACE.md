# X Interface Reference

Operational reference for interacting with X (Twitter) via claude-in-chrome MCP tools.

## Character Limits

| Tier | Post Limit | Reply Limit | URL Length |
|------|-----------|-------------|------------|
| Free | 280 chars | 280 chars | 23 chars (t.co shortening) |
| Premium | 25,000 chars | 25,000 chars | 23 chars (t.co shortening) |

All URLs are shortened to 23 characters via t.co regardless of actual length. Count 23 chars per URL when calculating reply length.

## Claude in Chrome Tool Patterns

The skill uses Anthropic's Claude in Chrome extension (`claude-in-chrome` MCP server), which operates on your real browser session with existing login state.

### Page Navigation

Use the `navigate` tool to go to URLs:
```
navigate(url: "https://x.com/home")
```

### Reading Page Content

Use `read_page` to get structured page content (text, elements, links). Use `computer` tool with screenshot action when visual context is needed (images, layout).

### Scrolling the Feed

Use the `computer` tool to scroll:
```
computer(action: "scroll", coordinate: [640, 400], direction: "down", amount: 3)
```

Or use keyboard shortcuts:
```
computer(action: "key", text: "space")        # scroll down one viewport
computer(action: "key", text: "shift+space")  # scroll up one viewport
```

### Opening Posts in New Tabs (Preserves Scroll Position)

When you find a relevant post while scrolling the feed, open it in a new tab rather than clicking into it. This preserves your scroll position on the main feed.

Use `tabs_create_mcp` to open the post permalink in a new tab:
```
tabs_create_mcp(url: "https://x.com/{username}/status/{tweet_id}")
```

After capturing details from the new tab, close it and return to the main feed tab.

### Getting Post Permalink URLs

Post permalink format: `https://x.com/{username}/status/{tweet_id}`

To capture a permalink from the feed:
1. Read the page to identify the post
2. Look for the timestamp link (e.g., "2h", "44m") — its href contains the permalink
3. Alternatively, look for status URL patterns in link elements
4. Open the permalink in a new tab to verify and capture full details

### Reading Post Details

After opening a post permalink (in a new tab), read the page to capture:
- Full post text
- Author name and handle
- Engagement metrics (likes, retweets, replies, views/impressions)
- Existing reply threads
- Whether the post contains images/video (describe visual content)

### Clicking Elements

Use the `computer` tool to click on elements:
```
computer(action: "click", coordinate: [x, y])
```

Or use `find` to locate elements, then click by coordinate.

## Typing Replies — JS Injection (Required Workaround)

**X keyboard shortcuts intercept normal typing.** The `form_input` tool and direct keyboard input via `computer` trigger X's global shortcut handler — the "e" key navigates to Explore, other keys trigger other actions. This causes navigation away from the tweet page instead of text entry.

**Always use JavaScript injection to type reply text:**

```javascript
// Use via javascript_tool
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

1. **Navigate** to the tweet permalink URL (in a new tab from the approval plan URLs)
2. **Wait** for page load (read page to verify)
3. **Find reply field** — look for "Post your reply" or the reply compose area
4. **Click** the reply field to expand it (it starts collapsed as a single line)
5. **Wait** briefly for the reply editor to expand (shows "Replying to @username")
6. **Inject text** using the JS injection pattern above
7. **Verify** — read page or screenshot to confirm text content and any link preview cards
8. **Click Reply button** — find the "Reply" or "Post" button and click it
9. **Verify** — read page or screenshot to confirm successful posting (look for your reply appearing)

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
