# X Algorithm Deep Dive Research
Timestamp: 20260120-172806
Started: 2026-01-20 17:28:06
Thoroughness: very-thorough

## Research Question
Comprehensive deep dive into the X For You feed algorithm to understand:
1. How content is ranked and scored
2. What engagement signals matter most
3. How out-of-network content gets discovered
4. What strategies maximize exposure for creators

## Repository Structure
- `home-mixer/` - Orchestration layer (Rust)
- `phoenix/` - ML models for retrieval and ranking (Python/JAX)
- `thunder/` - In-network post store (Rust)
- `candidate-pipeline/` - Reusable pipeline framework (Rust)

---

## Section 1: System Architecture Overview

### Two-Stage Pipeline
The For You feed uses a **two-stage recommendation pipeline**:

1. **Retrieval Stage**: Narrow millions of candidates down to ~1000s
   - Uses **Two-Tower Model** (user tower + candidate tower)
   - User tower encodes engagement history via transformer
   - Candidate tower projects posts to shared embedding space
   - Top-K retrieved via dot product similarity (ANN search)

2. **Ranking Stage**: Score and order the retrieved candidates
   - Uses **Grok-based transformer** with special attention masking
   - Predicts probabilities for 19 different engagement actions
   - Weighted combination produces final score

### Content Sources
- **Thunder (In-Network)**: Posts from accounts you follow
  - Stored in real-time memory
  - Sub-millisecond lookups
  - Sorted by recency first, then scored

- **Phoenix Retrieval (Out-of-Network)**: ML-discovered posts
  - Uses user's engagement history as context
  - Finds similar posts from global corpus

---

## Section 2: The 19 Predicted Engagement Actions

The Phoenix transformer predicts probabilities for these actions:

### Positive Signals (Boost Score)
| Action | Description |
|--------|-------------|
| `favorite_score` | P(like) - Probability user will like |
| `reply_score` | P(reply) - Probability user will reply |
| `retweet_score` | P(repost) - Probability user will repost |
| `quote_score` | P(quote) - Probability user will quote |
| `click_score` | P(click) - Probability user clicks on post |
| `profile_click_score` | P(profile_click) - Clicks author's profile |
| `photo_expand_score` | P(photo_expand) - Expands images |
| `vqv_score` | P(video_quality_view) - Quality video views |
| `share_score` | P(share) - General share action |
| `share_via_dm_score` | P(share_dm) - Share via DM |
| `share_via_copy_link_score` | P(copy_link) - Copy link to share |
| `dwell_score` | P(dwell) - Stays on post |
| `dwell_time` | Predicted dwell duration (continuous) |
| `quoted_click_score` | P(quoted_click) - Clicks quoted content |
| `follow_author_score` | P(follow) - Follows the author |

### Negative Signals (Reduce Score)
| Action | Description |
|--------|-------------|
| `not_interested_score` | P(not_interested) - Marks not interested |
| `block_author_score` | P(block) - Blocks author |
| `mute_author_score` | P(mute) - Mutes author |
| `report_score` | P(report) - Reports post |

---

## Section 3: Scoring Mechanism Deep Dive

### Weighted Score Formula
```
Final Score = SUM(weight_i * P(action_i))
```

The scoring pipeline:
1. **Phoenix Scorer**: Gets ML predictions for all 19 actions
2. **Weighted Scorer**: Combines predictions with weights
3. **Author Diversity Scorer**: Penalizes repeated authors
4. **OON Scorer**: Adjusts out-of-network content scores

### Key Implementation Details

**Author Diversity Penalty**:
- Uses exponential decay for repeated authors
- `multiplier = (1.0 - floor) * decay^position + floor`
- Each subsequent post from same author gets lower score
- Ensures feed diversity

**Out-of-Network Adjustment**:
- OON content gets multiplied by `OON_WEIGHT_FACTOR`
- In-network content has inherent advantage
- But high-quality OON can still surface

**Video Content Bonus**:
- Videos above minimum duration get VQV weight applied
- `vqv_score` only contributes for eligible videos

### Score Normalization
- Combined scores are normalized
- Negative scores (likely to block/mute/report) get special offset treatment
- Ensures positive content bubbles up

---

## Section 4: Filtering Logic

### Pre-Scoring Filters
Posts are removed before scoring if they:

| Filter | What It Removes |
|--------|-----------------|
| `AgeFilter` | Posts older than threshold |
| `DropDuplicatesFilter` | Duplicate post IDs |
| `SelfpostFilter` | User's own posts |
| `AuthorSocialgraphFilter` | Posts from blocked/muted accounts |
| `MutedKeywordFilter` | Posts containing muted keywords |
| `PreviouslySeenPostsFilter` | Posts user already saw (bloom filter) |
| `PreviouslyServedPostsFilter` | Posts served in current session |
| `RepostDeduplicationFilter` | Reposts of same original content |
| `IneligibleSubscriptionFilter` | Paywalled content user can't access |
| `CoreDataHydrationFilter` | Posts that failed metadata fetch |

### Post-Selection Filters
After ranking, final checks:
- `VFFilter`: Removes deleted/spam/violence/gore
- `DedupConversationFilter`: Deduplicates conversation threads

---

## Section 5: How Out-of-Network Discovery Works

### Two-Tower Retrieval Architecture

**User Tower**:
- Encodes: User features + engagement history
- Uses same transformer architecture as ranker
- Produces normalized user embedding [B, D]

**Candidate Tower**:
- Projects post + author embeddings
- Two-layer MLP with SiLU activation
- L2-normalized output

**Retrieval**:
- Dot product similarity between user and corpus
- Top-K selection
- Posts then go to ranking stage

### Key Insight: Your Engagement History IS Your Algorithm
The model learns what you like by looking at:
- Posts you liked, replied to, reposted
- Authors you engaged with
- Time you spent (dwell)
- What you shared

---

## Section 6: Growth Strategies Based on Algorithm Analysis

### Strategy 1: Optimize for HIGH-WEIGHT Positive Signals

Based on the scoring system, focus on content that drives:

**Tier 1 - Highest Impact**:
- **Likes (favorites)** - Quick engagement signal
- **Replies** - Deep engagement indicator
- **Reposts** - Amplification signal
- **Quotes** - High-quality engagement

**Tier 2 - Significant Impact**:
- **Profile clicks** - Indicates compelling author
- **Shares (DM, copy link)** - Strong intent signal
- **Follows** - Ultimate conversion

**Tier 3 - Supporting Signals**:
- **Dwell time** - Indicates interesting content
- **Video quality views** - For video content
- **Photo expansion** - For visual content

### Strategy 2: Minimize Negative Signals

Content that triggers these HURTS your reach:
- **Not Interested** - Direct negative signal
- **Mutes** - Author-level negative
- **Blocks** - Strong negative signal
- **Reports** - Strongest negative signal

**Implication**: Avoid polarizing content that might trigger these actions from any segment of your audience.

### Strategy 3: Leverage In-Network Priority

**In-network content has advantage** (no OON penalty factor).

**Actions**:
- Build genuine follower relationships
- Engage with followers so they engage back
- Post consistently to stay in Thunder's recency window
- Your followers' feeds prefer YOUR content

### Strategy 4: Get Discovered Out-of-Network

To appear in OON feeds (new audience discovery):

**The algorithm looks for posts similar to what users engaged with.**

**Actions**:
- Create content similar to viral posts in your niche
- Engage with influencers (your history affects their recommendations)
- Content that drives cross-network engagement (quotes, replies) signals quality

### Strategy 5: Author Diversity Awareness

**The algorithm penalizes posting too much in rapid succession.**

**Actions**:
- Space out posts (don't spam)
- Quality > Quantity
- Each additional post from you gets lower score in same user's feed
- Better: fewer high-quality posts than many mediocre ones

### Strategy 6: Content Format Optimization

**Video Content**:
- Videos above minimum duration get VQV score applied
- Quality views (not just impressions) matter
- Hook viewers early to drive dwell time

**Visual Content**:
- Photo expansion is tracked
- High-quality images that invite expansion score better

**Text Content**:
- Dwell time matters - make content worth reading
- Replies indicate conversation-worthy content

### Strategy 7: Timing and Recency

**Thunder serves recent posts from followed accounts sorted by recency.**

**Actions**:
- Post when your audience is active
- Fresh content enters the candidate pool
- Older posts get filtered by AgeFilter

### Strategy 8: Avoid Filtering Pitfalls

**Don't trigger filters**:
- Avoid muted keywords in your niche
- Don't spam (dedup filters)
- Ensure content meets guidelines (VF filter)
- Create original content (repost dedup)

### Strategy 9: Engagement Pattern Optimization

**The model learns from engagement SEQUENCES.**

**Actions**:
- Encourage full engagement loops (like -> reply -> share)
- Each action type adds signal
- Multi-action engagement from users trains the model that your content is valuable

### Strategy 10: Build Embedding Similarity

**The retrieval model finds posts similar to what users liked.**

**Actions**:
- Study viral posts in your niche
- Create content with similar patterns/topics
- Your post embedding should be "near" content users already engaged with

---

## Summary: The Algorithm Formula for Growth

```
Maximize: Likes + Replies + Reposts + Quotes + Shares + Follows + Dwell
Minimize: Not Interested + Mutes + Blocks + Reports
Leverage: In-Network Priority + Recency
Discover: OON via engagement similarity
Diversify: Don't spam, space posts
Format: Videos with quality views, images that expand, text that holds attention
```

**The single most important insight**: The algorithm predicts whether a specific user will ENGAGE with your content based on their history. The best strategy is creating content that genuinely engages your target audience.

---

## Technical Appendix: Key Code References

### Engagement Actions Enum (runners.py:202-222)
```python
ACTIONS: List[str] = [
    "favorite_score", "reply_score", "repost_score",
    "photo_expand_score", "click_score", "profile_click_score",
    "vqv_score", "share_score", "share_via_dm_score",
    "share_via_copy_link_score", "dwell_score", "quote_score",
    "quoted_click_score", "follow_author_score",
    "not_interested_score", "block_author_score",
    "mute_author_score", "report_score", "dwell_time"
]
```

### Weighted Scorer (weighted_scorer.rs:44-70)
Combines all predictions with weights, applies VQV eligibility for videos.

### Author Diversity (author_diversity_scorer.rs:29-31)
```rust
fn multiplier(&self, position: usize) -> f64 {
    (1.0 - self.floor) * self.decay_factor.powf(position as f64) + self.floor
}
```

### Candidate Isolation Attention (grok.py:39-71)
Candidates cannot attend to each other - only to user + history context.
