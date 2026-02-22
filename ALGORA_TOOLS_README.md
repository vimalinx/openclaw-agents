# 🎯 Algora Bounty Tools

A collection of CLI tools for exploring and interacting with Algora bounties.

## 📦 Installation

First, install the Algora SDK:

```bash
npm install @algora/sdk
```

## 🛠️ Available Tools

### 1. Bounty Explorer
**File:** `bounty-viewer.mjs`

Display active and completed bounties in a nice format.

```bash
node bounty-viewer.mjs
```

**Output:**
```
🎯 Algora Bounty Viewer

================================================================================
📋 CAL - ACTIVE BOUNTIES
================================================================================

Found 8 active bounties:

🟢 1. [CAL-5091] additional settings: "add team member as optional guest
   💰 Reward: $2,500
   📦 Repository: calcom/cal.com
   🔗 Issue: https://github.com/calcom/cal.com/issues/18947
   ...
```

---

### 2. Search Bounties
**File:** `search-bounties.mjs`

Search across organizations for bounties matching keywords.

```bash
# Search by keyword
node search-bounties.mjs "integration"

# Search with minimum reward
node search-bounties.mjs "api" 5000
```

**Parameters:**
- `query`: Keyword to search for in bounty titles or repo names
- `min-reward`: (optional) Minimum reward amount in USD

---

### 3. Top Bounties
**File:** `top-bounties-fixed.mjs`

Find the highest-paying bounties across all organizations.

```bash
# Show top 10 bounties (default)
node top-bounties-fixed.mjs

# Show top 20 bounties
node top-bounties-fixed.mjs 20

# Show top 50 bounties
node top-bounties-fixed.mjs 50
```

**Output includes:**
- Ranked list of bounties
- Market statistics
- Reward distribution chart
- Organization breakdown

---

### 4. Interactive CLI
**File:** `bounty-cli.mjs`

Interactive menu-driven bounty explorer.

```bash
node bounty-cli.mjs
```

**Menu:**
```
1. List bounties for an organization
2. Search popular organizations
3. Show bounty statistics
4. Exit
```

---

### 5. Dashboard Generator
**File:** `generate-dashboard.mjs`

Generate a beautiful HTML dashboard.

```bash
node generate-dashboard.mjs
```

Creates `bounty-dashboard.html` - open in your browser!

**Features:**
- Summary statistics cards
- Interactive bounty cards
- Color-coded badges
- Direct GitHub links

---

### 6. Full Explorer
**File:** `algora-full-explorer.mjs`

Comprehensive exploration across multiple organizations.

```bash
node algora-full-explorer.mjs
```

Scans multiple organizations and provides:
- Total bounty counts
- Reward summaries
- Repository breakdown
- Bounty type analysis

---

## 📊 Example Use Cases

### Find a $5,000+ bounty for TypeScript projects
```bash
node top-bounties-fixed.mjs 20 | grep -A 5 '\$5,000'
```

### Search for integration tasks
```bash
node search-bounties.mjs "integration" 2000
```

### Generate a weekly dashboard
```bash
node generate-dashboard.mjs
open bounty-dashboard.html
```

### Explore your favorite organization
```bash
node bounty-viewer.mjs | grep -A 3 "YOUR_ORG"
```

---

## 📈 Sample Output

### Top Bounties
```
💰 Top 20 Highest Bounties
======================================================================

🥇 $20,000 - [CAL-4531] Take into account guest's availability when rescheduling
   📦 calcom/cal.com
   🔗 https://github.com/calcom/cal.com/issues/16378
   📊 cal | dev | cash

🥈 $10,000 - Plans on weights?
   📦 calcom/font
   🔗 https://github.com/calcom/font/issues/2
   📊 cal | dev | cash

🥉 $5,000 - [CAL-5107] add no-show to zapier
   📦 calcom/cal.com
   🔗 https://github.com/calcom/cal.com/issues/18992
   📊 cal | dev | cash
```

### Market Overview
```
📊 Market Overview:
   Total bounties: 8
   Total value: $53,500
   Average: $6,687
   Organizations: 1
   Repositories: 2
   Range: $2,000 - $20,000
```

---

## 🔍 Bounty Types

- **dev**: Development bounties (coding, features, integrations)
- **content**: Content bounties (documentation, tutorials, videos)

### Reward Types

- **cash**: USD monetary rewards
- **point**: Platform points (can be converted or used for reputation)

---

## 💡 Tips

1. **Start with `top-bounties-fixed.mjs`** to see what's available
2. **Use `search-bounties.mjs`** to find tasks matching your skills
3. **Generate a dashboard** for a visual overview
4. **Check back regularly** - new bounties appear frequently

---

## 📝 Data Structure

Each bounty contains:
- **Title & Description**: What needs to be done
- **Reward**: Cash amount or points
- **Repository**: Where the work happens
- **Issue URL**: Link to the GitHub issue/PR
- **Organization**: Who is offering the bounty
- **Bids**: Who has applied and for how much
- **Type**: Development or content task
- **Status**: Active, completed, or inactive

---

## 🚀 Advanced Usage

### Combining Tools

```bash
# Find high-paying API bounties and save to file
node search-bounties.mjs "api" 5000 > api-bounties.txt

# Generate dashboard and view it
node generate-dashboard.mjs && open bounty-dashboard.html

# Get top bounties and extract URLs
node top-bounties-fixed.mjs 10 | grep "🔗" | cut -d' ' -f2 > top-bounty-urls.txt
```

### Customizing Search

Edit the orgs list in the scripts to add your own organizations:

```javascript
const orgs = [
  "cal", "your-org", "another-org"
];
```

---

## 📚 Learn More

- **Full Exploration Report**: See `ALGORA_EXPLORATION_REPORT.md`
- **Algora Website**: https://algora.io
- **Algora Docs**: https://algora.io/docs
- **GitHub**: https://github.com/algora-io/sdk

---

## ⚠️ Notes

- API may have rate limits (be respectful)
- Some endpoints may require authentication
- Organizations and bounties change frequently
- Always verify current status on Algora website

---

*Happy bounty hunting! 💰*
