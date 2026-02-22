# Algora SDK Exploration Report

## Overview

I explored the **Algora SDK** - a platform that connects open source maintainers with bounties for contributing to projects. Here's what I discovered and built.

---

## What is Algora?

Algora is a bounty platform for open source projects. Organizations can create bounties for:
- **Development tasks** (fixing bugs, adding features, implementing integrations)
- **Content tasks** (documentation, tutorials, videos)

Contributors can claim these bounties and get paid in cash or points.

---

## SDK Capabilities

The Algora SDK (`@algora/sdk`) provides:

### 1. **List Bounties**
```javascript
await algora.bounty.list.query({
  org: "cal",
  limit: 10,
  status: "active" // or "inactive"
});
```

Returns:
- Bounty details (title, reward, repository)
- Task information (issue URL, description)
- Organization metadata
- Bids from contributors

### 2. **Get Single Bounty**
```javascript
await algora.bounty.get.query({ id: "bounty-id" });
```

Returns full bounty details including bids and claim information.

### 3. **Get Organization Leaderboard**
```javascript
await algora.org.getLeaderboard.query({ org: "cal" });
```
*Note: This endpoint returned HTML instead of JSON, likely requires authentication*

---

## Key Findings

### Organizations with Active Bounties

From exploring 20+ popular open source organizations:

| Organization | Active Bounties | Total Rewards | Top Bounty |
|-------------|---------------|---------------|------------|
| **cal** (Cal.com) | 8 | $53,500 | $20,000 |
| Other orgs | 0 | - | - |

### Current Bounty Landscape (Feb 2026)

- **Total Active Bounties**: 8
- **Total Reward Value**: $53,500
- **Average Reward**: $6,687
- **Reward Range**: $2,000 - $20,000

### Reward Distribution

| Range | Count | Percentage |
|-------|-------|------------|
| $1,000-$5,000 | 3 | 37.5% |
| $5,000-$10,000 | 3 | 37.5% |
| $10,000-$50,000 | 2 | 25.0% |

### Top Bounties

1. **$20,000** - Take into account guest's availability when rescheduling
   - Repository: calcom/cal.com
   - Issue: #16378

2. **$10,000** - Plans on weights?
   - Repository: calcom/font
   - Issue: #2

3. **$5,000** - add no-show to zapier
   - Repository: calcom/cal.com
   - Issue: #18992

---

## Tools I Built

### 1. **Bounty Explorer** (`algora-explorer.mjs`)
Basic script to explore bounties from an organization.

**Usage:**
```bash
node algora-explorer.mjs
```

### 2. **Bounty Viewer** (`bounty-viewer.mjs`)
Nicely formatted display of active and completed bounties.

**Usage:**
```bash
node bounty-viewer.mjs
```

**Output:**
```
📋 CAL - ACTIVE BOUNTIES
================================================================================

Found 8 active bounties:

🟢 1. [CAL-5091] additional settings: "add team member as optional guest
   💰 Reward: $2,500
   📦 Repository: calcom/cal.com
   🔗 Issue: https://github.com/calcom/cal.com/issues/18947
   📊 Type: dev | cash
   📅 Created: Feb 11, 2025
   ...
```

### 3. **Search Bounties** (`search-bounties.mjs`)
Search across organizations for bounties matching keywords.

**Usage:**
```bash
node search-bounties.mjs <query> [min-reward]

# Examples:
node search-bounties.mjs "integration"
node search-bounties.mjs "api" 5000
```

### 4. **Top Bounties** (`top-bounties-fixed.mjs`)
Find the highest-paying bounties across all organizations.

**Usage:**
```bash
node top-bounties-fixed.mjs [limit]

# Show top 20 bounties:
node top-bounties-fixed.mjs 20
```

**Output includes:**
- Ranked list of bounties
- Market statistics
- Reward distribution charts
- Organization breakdowns

### 5. **Interactive CLI** (`bounty-cli.mjs`)
Interactive menu-driven explorer.

**Usage:**
```bash
node bounty-cli.mjs
```

**Features:**
1. List bounties for an organization
2. Search popular organizations
3. Show bounty statistics
4. Exit

### 6. **Dashboard Generator** (`generate-dashboard.mjs`)
Generate an HTML dashboard visualization.

**Usage:**
```bash
node generate-dashboard.mjs
```

Creates `bounty-dashboard.html` - a beautiful, interactive web dashboard with:
- Summary statistics cards
- Grid of bounty cards with hover effects
- Color-coded badges for bounty types
- Direct links to GitHub issues

---

## Bounty Data Structure

Each bounty contains:

```javascript
{
  id: "string",
  kind: "dev" | "content",           // Bounty type
  reward_type: "cash" | "point",      // Reward currency
  status: "active" | "inactive",      // Active or completed
  type: "standard" | "tip",          // Standard or tip bounty

  task: {
    id: "string",
    number: 123,                      // Issue/PR number
    title: "string",
    body: "string",
    repo_owner: "calcom",
    repo_name: "cal.com",
    url: "https://github.com/...",
    forge: "github"
  },

  org: {
    id: "string",
    handle: "cal",
    display_name: "Cal.com",
    description: "...",
    avatar_url: "...",
    members: [...],
    tech: ["TypeScript", "Next.js", ...]
  },

  reward: {
    amount: 5000,                     // In cents
    currency: "USD"
  },

  reward_formatted: "$5,000",         // Display string

  bids: [{                           // Who has bid
    id: "string",
    amount: 5000,
    status: "pending" | "accepted",
    user: {...}
  }],

  created_at: Date,
  updated_at: Date
}
```

---

## Interesting Discoveries

### 1. **Cal.com is Active**
Cal.com is the most active organization on Algora, with 8 active bounties worth $53,500 total.

### 2. **Reward Variability**
Bounties range from $2,000 to $20,000, showing organizations are willing to pay significant amounts for quality contributions.

### 3. **Diverse Tasks**
Bounties cover various areas:
- Integration with third-party services (Zapier, BigBlueButton)
- Feature additions (booking questions, rescheduling logic)
- Exchange server integration
- Font development

### 4. **Organization Metadata**
Each organization has rich metadata:
- Tech stack preferences
- Team members with roles (admin, mod, expert)
- Social media links
- Stargazer counts

---

## Potential Use Cases

### For Contributors
- **Find high-paying bounties** matching your skills
- **Track organizations** you're interested in
- **Search by keywords** to find relevant tasks
- **Filter by reward amount** to meet income goals

### For Organizations
- **Showcase bounties** on your website
- **Embed bounty board** in documentation
- **Track leaderboard** of top contributors
- **Create dashboards** for internal tracking

### For Researchers/Analysts
- **Analyze bounty market** trends
- **Track reward pricing** over time
- **Study contribution patterns**
- **Monitor organization activity**

---

## Technical Notes

### API Behavior
- **Rate limiting**: No explicit limit observed, but be respectful
- **Pagination**: Supported via `cursor` parameter
- **Filtering**: `status`, `rewarded` filters available
- **Authentication**: Some endpoints (like leaderboard) may require auth

### Error Handling
- **404**: Organization or bounty not found
- **HTML responses**: Some endpoints return HTML (likely auth required)
- **Network errors**: Standard fetch errors apply

### Best Practices
- Cache results to avoid repeated API calls
- Handle errors gracefully
- Use appropriate limits (default: 100)
- Respect rate limits

---

## Files Created

| File | Description |
|------|-------------|
| `algora-explorer.mjs` | Basic exploration script |
| `bounty-viewer.mjs` | Formatted bounty display |
| `search-bounties.mjs` | Keyword search tool |
| `top-bounties-fixed.mjs` | Highest-paying bounties finder |
| `bounty-cli.mjs` | Interactive CLI interface |
| `generate-dashboard.mjs` | HTML dashboard generator |
| `bounty-dashboard.html` | Generated dashboard (run generate-dashboard.mjs) |

---

## Next Steps

### Ideas for Further Exploration

1. **Historical Analysis**
   - Track bounty creation and completion over time
   - Analyze reward pricing trends
   - Identify seasonal patterns

2. **Contributor Analysis**
   - Track top contributors
   - Analyze contribution velocity
   - Build contributor profiles

3. **Skill Matching**
   - Match bounties to contributors by skills
   - Build recommendation engine
   - Create personalized feeds

4. **Notifications**
   - Alert on new bounties
   - Watch for specific keywords
   - Track organization activity

5. **Integrations**
   - GitHub Actions integration
   - Discord bot for notifications
   - Slack workspace app

---

## Conclusion

The Algora SDK provides a clean, well-documented API for interacting with the bounty platform. With just a few API calls, you can:
- List and filter bounties
- Get detailed bounty information
- Build custom dashboards and tools
- Integrate bounty data into your applications

The platform appears to be growing (Cal.com's active participation is promising), and the SDK makes it easy to build innovative tools on top of it.

**Recommendation**: If you're interested in contributing to open source and getting paid for it, Algora is worth exploring. The bounties pay well (average $6,687), and the tasks range from quick integrations to complex feature work.

---

*Report generated: February 20, 2026*
*SDK version: @algora/sdk@0.3.1*
