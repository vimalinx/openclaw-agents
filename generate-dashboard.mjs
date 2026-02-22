import { algora } from "@algora/sdk";
import fs from 'fs';

async function generateDashboard() {
  const orgs = ["cal", "vercel", "remotion-dev", "stripe", "supabase", "nextjs"];
  const allBounties = [];

  console.log("🔍 Fetching bounty data...");

  for (const org of orgs) {
    try {
      const result = await algora.bounty.list.query({ org, limit: 100, status: 'active' });
      result.items.forEach(bounty => {
        allBounties.push({ ...bounty, orgName: org });
      });
    } catch (error) {
      // Skip errors
    }
  }

  console.log(`✅ Found ${allBounties.length} bounties`);

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Algora Bounty Dashboard</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 2rem;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    h1 {
      color: white;
      text-align: center;
      margin-bottom: 2rem;
      font-size: 2.5rem;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .stat-card {
      background: white;
      padding: 1.5rem;
      border-radius: 12px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .stat-card h3 {
      color: #666;
      font-size: 0.875rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 0.5rem;
    }

    .stat-card .value {
      color: #333;
      font-size: 2rem;
      font-weight: bold;
    }

    .bounty-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 1.5rem;
    }

    .bounty-card {
      background: white;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .bounty-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }

    .bounty-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 1.5rem;
      color: white;
    }

    .bounty-reward {
      font-size: 2rem;
      font-weight: bold;
      margin-bottom: 0.5rem;
    }

    .bounty-org {
      font-size: 0.875rem;
      opacity: 0.9;
    }

    .bounty-body {
      padding: 1.5rem;
    }

    .bounty-title {
      font-size: 1.125rem;
      font-weight: 600;
      color: #333;
      margin-bottom: 1rem;
      line-height: 1.5;
    }

    .bounty-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1rem;
    }

    .badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 500;
    }

    .badge-dev {
      background: #e0e7ff;
      color: #4338ca;
    }

    .badge-content {
      background: #fce7f3;
      color: #be185d;
    }

    .badge-cash {
      background: #d1fae5;
      color: #047857;
    }

    .badge-point {
      background: #fef3c7;
      color: #b45309;
    }

    .bounty-link {
      display: inline-block;
      padding: 0.75rem 1.5rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      text-decoration: none;
      border-radius: 8px;
      font-weight: 500;
      transition: opacity 0.2s;
    }

    .bounty-link:hover {
      opacity: 0.9;
    }

    .repo-name {
      color: #666;
      font-size: 0.875rem;
      margin-bottom: 1rem;
    }

    .no-bounties {
      text-align: center;
      color: white;
      font-size: 1.5rem;
      padding: 4rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>💰 Algora Bounty Dashboard</h1>

    <div class="stats">
      <div class="stat-card">
        <h3>Total Bounties</h3>
        <div class="value">${allBounties.length}</div>
      </div>
      <div class="stat-card">
        <h3>Total Value</h3>
        <div class="value">$${allBounties.reduce((sum, b) => sum + (b.reward?.amount || 0), 0).toLocaleString()}</div>
      </div>
      <div class="stat-card">
        <h3>Average Reward</h3>
        <div class="value">$${Math.round(allBounties.reduce((sum, b) => sum + (b.reward?.amount || 0), 0) / allBounties.length).toLocaleString()}</div>
      </div>
      <div class="stat-card">
        <h3>Organizations</h3>
        <div class="value">${[...new Set(allBounties.map(b => b.orgName))].length}</div>
      </div>
    </div>

    ${allBounties.length > 0 ? `
    <div class="bounty-grid">
      ${allBounties.map(bounty => `
        <div class="bounty-card">
          <div class="bounty-header">
            <div class="bounty-reward">$${bounty.reward?.amount?.toLocaleString() || 'Points'}</div>
            <div class="bounty-org">${bounty.orgName}</div>
          </div>
          <div class="bounty-body">
            <div class="bounty-title">${bounty.task.title}</div>
            <div class="repo-name">📦 ${bounty.task.repo_owner}/${bounty.task.repo_name}</div>
            <div class="bounty-meta">
              <span class="badge badge-${bounty.kind}">${bounty.kind}</span>
              <span class="badge badge-${bounty.reward_type}">${bounty.reward_type}</span>
            </div>
            <a href="${bounty.task.url}" target="_blank" class="bounty-link">View Bounty →</a>
          </div>
        </div>
      `).join('')}
    </div>
    ` : `
    <div class="no-bounties">
      No bounties found at this time. Check back later!
    </div>
    `}
  </div>

  <script>
    // Add some interactivity
    document.querySelectorAll('.bounty-card').forEach(card => {
      card.addEventListener('click', () => {
        const link = card.querySelector('.bounty-link');
        if (link) window.open(link.href, '_blank');
      });
    });
  </script>
</body>
</html>`;

  fs.writeFileSync('bounty-dashboard.html', html);
  console.log("✅ Generated bounty-dashboard.html");
  console.log("💡 Open this file in your browser to view the dashboard!");
}

generateDashboard().catch(console.error);
