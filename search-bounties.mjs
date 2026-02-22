import { algora } from "@algora/sdk";

// Search for bounties across multiple organizations
async function searchBounties() {
  const args = process.argv.slice(2);
  const query = args[0];
  const minReward = parseInt(args[1]) || 0;

  if (!query) {
    console.log("Usage: node search-bounties.mjs <query> [min-reward]");
    console.log("Example: node search-bounties.mjs cal 1000");
    process.exit(1);
  }

  console.log(`🔍 Searching for bounties matching: "${query}"`);
  if (minReward > 0) {
    console.log(`💰 Minimum reward: $${minReward.toLocaleString()}`);
  }
  console.log();

  // List of organizations to search
  const orgs = [
    "cal", "vercel", "remotion-dev", "stripe", "supabase",
    "nextjs", "tailwindlabs", "mdn", "reactjs", "vuejs",
    "nodejs", "deno", "docker", "kubernetes", "angular"
  ];

  let totalFound = 0;
  const matches = [];

  for (const org of orgs) {
    try {
      const result = await algora.bounty.list.query({
        org,
        limit: 100,
        status: 'active'
      });

      const filtered = result.items.filter(bounty => {
        const titleMatch = bounty.task.title.toLowerCase().includes(query.toLowerCase());
        const repoMatch = bounty.task.repo_name.toLowerCase().includes(query.toLowerCase());
        const rewardMatch = !bounty.reward || bounty.reward.amount >= minReward;

        return (titleMatch || repoMatch) && rewardMatch;
      });

      if (filtered.length > 0) {
        console.log(`\n📦 ${org} (${filtered.length} match(es))`);
        console.log("─".repeat(70));

        filtered.forEach((bounty, idx) => {
          const reward = bounty.reward ? `$${bounty.reward.amount.toLocaleString()}` : 'Points';
          console.log(`\n${idx + 1}. ${bounty.task.title}`);
          console.log(`   💰 ${reward} | ${bounty.task.repo_owner}/${bounty.task.repo_name}`);
          console.log(`   🔗 ${bounty.task.url}`);
        });

        totalFound += filtered.length;
        matches.push(...filtered);
      }
    } catch (error) {
      // Skip orgs with errors
    }
  }

  console.log("\n" + "=".repeat(70));
  console.log(`✅ Found ${totalFound} bounties matching "${query}"`);
  console.log("=".repeat(70));

  // Show summary
  if (matches.length > 0) {
    const totalReward = matches
      .filter(b => b.reward)
      .reduce((sum, b) => sum + b.reward.amount, 0);

    const avgReward = totalReward / matches.filter(b => b.reward).length;

    console.log(`\n📊 Summary:`);
    console.log(`   Total reward value: $${totalReward.toLocaleString()}`);
    console.log(`   Average reward: $${avgReward.toLocaleString().split('.')[0]}`);
    console.log(`   Organizations: ${[...new Set(matches.map(b => b.org.handle))].length}`);
    console.log(`   Repositories: ${[...new Set(matches.map(b => `${b.task.repo_owner}/${b.task.repo_name}`))].size}`);
  }
}

searchBounties().catch(console.error);
