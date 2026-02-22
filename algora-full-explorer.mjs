import { algora } from "@algora/sdk";

async function exploreAlgora() {
  console.log("🚀 Algora SDK Explorer\n");
  console.log("=" .repeat(60));

  // Organizations to explore
  const orgs = ["cal", "vercel", "remotion-dev", "stripe", "supabase", "nextjs", "tailwindlabs", "mdn"];

  const results = {
    orgsFound: [],
    totalBounties: 0,
    totalReward: 0,
    uniqueRepos: new Set()
  };

  for (const org of orgs) {
    console.log(`\n🔍 Exploring: ${org}`);

    try {
      // Get active bounties
      const active = await algora.bounty.list.query({
        org,
        limit: 10,
        status: "active"
      });

      // Get inactive bounties (completed/archived)
      const inactive = await algora.bounty.list.query({
        org,
        limit: 10,
        status: "inactive"
      });

      const allBounties = [...active.items, ...inactive.items];

      if (allBounties.length > 0) {
        results.orgsFound.push(org);
        results.totalBounties += allBounties.length;

        console.log(`  ✅ Found ${allBounties.length} bounties (${active.items.length} active, ${inactive.items.length} inactive)`);

        // Analyze rewards
        const activeRewards = active.items
          .filter(b => b.reward)
          .reduce((sum, b) => sum + b.reward.amount, 0);

        const inactiveRewards = inactive.items
          .filter(b => b.reward)
          .reduce((sum, b) => sum + b.reward.amount, 0);

        results.totalReward += activeRewards + inactiveRewards;

        console.log(`  💰 Active rewards: $${activeRewards.toLocaleString()}`);
        console.log(`  💰 Paid out: $${inactiveRewards.toLocaleString()}`);

        // Count unique repos
        const repos = new Set(allBounties.map(b => `${b.task.repo_owner}/${b.task.repo_name}`));
        repos.forEach(repo => results.uniqueRepos.add(repo));

        console.log(`  📦 Repositories: ${repos.size}`);

        // Show top active bounties
        if (active.items.length > 0) {
          console.log("\n  Top Active Bounties:");
          active.items.slice(0, 3).forEach((bounty, idx) => {
            const reward = bounty.reward_formatted || 'Points';
            console.log(`    ${idx + 1}. [${bounty.reward_type.toUpperCase()}] ${reward} - ${bounty.task.title.substring(0, 60)}${bounty.task.title.length > 60 ? '...' : ''}`);
          });
        }
      } else {
        console.log(`  ⚪ No bounties found`);
      }
    } catch (error) {
      console.error(`  ❌ Error: ${error.message.substring(0, 100)}`);
    }
  }

  // Summary
  console.log("\n" + "=".repeat(60));
  console.log("\n📊 SUMMARY");
  console.log("=".repeat(60));
  console.log(`Organizations explored: ${orgs.length}`);
  console.log(`Organizations with bounties: ${results.orgsFound.length}`);
  console.log(`Total bounties found: ${results.totalBounties}`);
  console.log(`Total reward value: $${results.totalReward.toLocaleString()}`);
  console.log(`Unique repositories: ${results.uniqueRepos.size}`);
  console.log(`\n📦 Repositories with bounties:`);
  Array.from(results.uniqueRepos).forEach(repo => console.log(`  - ${repo}`));

  // Bounty type analysis
  console.log("\n" + "=".repeat(60));
  console.log("\n🔍 BOUNTY TYPES ANALYSIS");
  console.log("=".repeat(60));

  const bountyTypes = {
    dev: { count: 0, total: 0 },
    content: { count: 0, total: 0 }
  };

  const rewardTypes = {
    cash: { count: 0, total: 0 },
    point: { count: 0, total: 0 }
  };

  for (const org of results.orgsFound) {
    try {
      const result = await algora.bounty.list.query({ org, limit: 100 });
      result.items.forEach(bounty => {
        if (bountyTypes[bounty.kind]) {
          bountyTypes[bounty.kind].count++;
          if (bounty.reward) {
            bountyTypes[bounty.kind].total += bounty.reward.amount;
          }
        }

        if (rewardTypes[bounty.reward_type]) {
          rewardTypes[bounty.reward_type].count++;
          if (bounty.reward && bounty.reward_type === 'cash') {
            rewardTypes[bounty.reward_type].total += bounty.reward.amount;
          } else if (bounty.reward_type === 'point') {
            rewardTypes[bounty.reward_type].total += bounty.point_reward?.amount || 0;
          }
        }
      });
    } catch (error) {
      console.error(`Error analyzing ${org}: ${error.message}`);
    }
  }

  console.log("\nBy Kind:");
  console.log(`  Development: ${bountyTypes.dev.count} bounties, $${bountyTypes.dev.total.toLocaleString()}`);
  console.log(`  Content: ${bountyTypes.content.count} bounties, $${bountyTypes.content.total.toLocaleString()}`);

  console.log("\nBy Reward Type:");
  console.log(`  Cash: ${rewardTypes.cash.count} bounties, $${rewardTypes.cash.total.toLocaleString()}`);
  console.log(`  Points: ${rewardTypes.point.count} bounties, ${rewardTypes.point.total.toLocaleString()} points`);

  console.log("\n✨ Exploration complete!");
}

exploreAlgora().catch(console.error);
