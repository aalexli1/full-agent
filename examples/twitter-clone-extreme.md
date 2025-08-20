# Project Spec: Twitter Clone Extreme

## 1. Purpose

Cross-platform microblogging app with core Twitter-like functionality, plus bespoke enhancements to make it stand out.

---

## 2. Platforms

* **Web**: Responsive PWA built with React.
* **iOS**: Native app via React Native (with Swift modules for deep integration).
* **Android**: Native app via React Native (with Kotlin modules if needed).
* **API**: REST + GraphQL, accessible by web/mobile clients.
* **Deployment environments**:

  * Dev (local Docker Compose).
  * Staging (cloud host, seeded test data).
  * Production (scalable, CDN-backed).

---

## 3. Core Features

### 3.1 Accounts & Auth

* Email/username/password sign-up.
* Secure login with JWT + refresh.
* Password reset flow.
* Multi-account switching (max 5).

### 3.2 Posts ("Chirps")

* Text posts up to 280 characters.
* Media: 1–4 images OR 1 video (<60s).
* Ephemeral posts (auto-expire after 24h).
* Threads with reorder + preview.
* Offline drafts with sync.
* Scheduled posting (1m–30d).

### 3.3 Engagement

* Likes, retweets, replies.
* Retweet with comment.
* Emoji reactions (👍😂🔥).

### 3.4 Following & Feeds

* Follow/unfollow.
* Home feed tabs:

  * **Following** (chronological).
  * **For You** (algorithmic).
  * **Communities** (group content).
* Mute by user, topic, keyword.

### 3.5 Profiles

* Avatar, banner, bio (160 chars).
* Theme colors (WCAG AA contrast enforced).
* Archive view: "On This Day" (excludes ephemeral).

### 3.6 Discovery

* Search: username, keyword, hashtag.
* Explore page: trending hashtags (city/regional).
* Chirp Roulette: random post (safety-filtered).

### 3.7 Messaging (MVP)

* 1:1 DMs only.
* Encrypted at rest + transport (not E2EE).
* Text + images.

### 3.8 Notifications

* Push + in-app for mentions, likes, follows, DMs.
* Unified inbox with filters.
* Per-account notification settings.

---

## 4. Bespoke Features

* AI summarizer: TL;DR for threads >5 posts.
* Roast Mode (mutual opt-in, rate limited).
* Communities with their own feeds.
* Accessibility nudges (alt text suggestions, contrast checks).

---

## 5. Technical Expectations

* **Frontend**: React (web), React Native (mobile).
* **Backend**: Node.js or Python (FastAPI).
* **Database**: Postgres + Redis.
* **Media Storage**: S3-compatible + CDN.
* **Real-time**: WebSockets.
* **Deployment**: Docker + CI/CD pipeline.

---

## 6. Constraints & Policies

* Ephemeral posts excluded from rewind/archive.
* Deleted posts retained for 30 days in encrypted abuse escrow.
* Media limits: 10MB images, 50MB video.
* Accessibility required across all clients.
* Max accounts per user: 5.

---

## 7. Conflict Matrix

| Feature A         | Feature B           | Conflict               | Resolution                                    |
| ----------------- | ------------------- | ---------------------- | --------------------------------------------- |
| Ephemeral posts   | Rewind              | Content unavailable    | Exclude ephemeral from rewind.                |
| Ephemeral posts   | Scheduled posts     | TTL overlap            | Enforce TTL preview, block invalid schedules. |
| Encrypted DMs     | AI moderation       | E2EE prevents analysis | MVP uses encrypted-at-rest, not E2EE.         |
| Roast Mode        | Anti-harassment     | Abuse risk             | Mutual opt-in, rate limit, blocklists apply.  |
| Custom themes     | Accessibility       | Bad contrast           | Enforce WCAG AA, high-contrast override.      |
| Shake-to-retweet  | Accidental triggers | Unintended actions     | Confirmation toast, disable option.           |
| Geo trends        | Privacy             | Location leaks         | Coarse data, default opt-out.                 |
| Chirp Roulette    | Moderation          | Harmful content risk   | Eligibility filters, pre-checks.              |
| Reputation system | Cold start          | Entrenches incumbents  | Time-decay, newcomer boosts.                  |
| Communities       | Home feed           | User confusion         | Tabbed Home UX.                               |
| Longform posts    | Simplicity          | Feature creep          | Collapse as "read more" cards.                |
| AR filters        | App size            | Bloat                  | Modular packs, on-demand.                     |
| Multi-accounts    | Notifications       | Chaos                  | Unified inbox + per-account prefs.            |
| Deleted posts     | Legal               | Retention vs trust     | Transparent 30d escrow.                       |
| Marketplace       | Fraud/spam          | Exploitation           | Verified sellers, escrow, labels.             |
| Topic mute        | Recommendations     | Reduces training data  | Respect mutes, explain recs.                  |
| Fact-checking     | Latency             | Slower feed            | Async overlays.                               |
| Offline drafts    | Real-time           | Sync conflicts         | Last-write-wins + badges.                     |

---

## 8. Success Criteria

* Users can sign up, log in, and switch accounts.
* Users can post, like, reply, retweet, and schedule posts.
* Ephemeral posts expire correctly.
* Feeds render with proper content and filtering.
* Profiles display correctly with accessible themes.
* Search and discovery work.
* DMs function for 1:1 with images.
* Notifications delivered and configurable.
* App deployable via Docker/CI pipeline.

---

## 9. User Stories & Acceptance Criteria

### Auth & Accounts

* **Story**: As a new user, I want to sign up with email so I can create an account.
  **Acceptance**: Registration stores user record in DB, returns auth token, logs in.
* **Story**: As a user, I want to switch accounts without logging out.
  **Acceptance**: UI allows switching; push notifications reflect active account.

### Posting

* **Story**: As a user, I want to post up to 280 chars.
  **Acceptance**: Server rejects >280 chars; post appears in timeline within 500ms.
* **Story**: As a user, I want ephemeral posts that vanish after 24h.
  **Acceptance**: Post flagged ephemeral; deleted from user feeds after 24h.
* **Story**: As a user, I want to schedule posts.
  **Acceptance**: Post is stored with future timestamp; publishes at correct time.
* **Story**: As a user, I want to compose threads.
  **Acceptance**: Posts linked under a thread\_id; reorder works in UI.

### Engagement

* **Story**: As a user, I want to like, retweet, and reply.
  **Acceptance**: DB updates recorded; counts updated in <1s.
* **Story**: As a user, I want emoji react.
  **Acceptance**: Limited emoji set; each user can react once per post.

### Feeds

* **Story**: As a user, I want to see only followed users in chronological feed.
  **Acceptance**: Feed endpoint returns strictly time-ordered followed posts.
* **Story**: As a user, I want algorithmic recommendations.
  **Acceptance**: Ranked feed available via For You tab.
* **Story**: As a user, I want to mute topics.
  **Acceptance**: Muted content never appears in feed.

### Profiles

* **Story**: As a user, I want to set a bio and avatar.
  **Acceptance**: Profile updates stored, appear on timeline/profile.
* **Story**: As a user, I want accessible themes.
  **Acceptance**: UI prevents invalid colors; overrides available.
* **Story**: As a user, I want to see "On This Day" content.
  **Acceptance**: Archive endpoint excludes ephemeral posts.

### Discovery

* **Story**: As a user, I want to search content.
  **Acceptance**: Search returns matches for keywords, hashtags, usernames.
* **Story**: As a user, I want to see trending topics.
  **Acceptance**: Trending endpoint returns geo-scoped hashtags.
* **Story**: As a user, I want Chirp Roulette.
  **Acceptance**: Random post returned, filtered for safety.

### Messaging

* **Story**: As a user, I want to DM 1:1.
  **Acceptance**: DM saved in DB; recipient notified; encrypted at rest.
* **Story**: As a user, I want to attach images.
  **Acceptance**: Media uploads <10MB succeed.

### Notifications

* **Story**: As a user, I want push notifications for activity.
  **Acceptance**: Push triggered <5s after event.
* **Story**: As a user, I want to configure notifications.
  **Acceptance**: Per-account preferences respected.

---

## 10. Stretch Goals

* Collaborative posts with dual attribution.
* AI-generated alt text.
* Voice posts + Spaces.
* Topic-based feeds.
* Marketplace for promos/shoutouts.

