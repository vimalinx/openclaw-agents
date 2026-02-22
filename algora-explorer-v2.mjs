import { algora } from "@algora/sdk";

async function exploreAlgora() {
  console.log("🔍 Exploring Algora SDK...\n");

  // Try different organizations that might have bounties
  const orgsToTry = ["cal", "vercel", "remotion-dev", "stripe", "nextjs"];

  for (const org of orgsToTry) {
    console.log(`\n📋 Trying organization: ${org}...`);

    try {
      const result = await algora.bounty.list.query({
        org,
        limit: 3,
        status: "active"
      });

      if (result.items.length > 0) {
        console.log(`✅ Found ${result.items.length} active bounties!\n`);

        result.items.forEach((bounty, idx) => {
          console.log(`${idx + 1}. ${bounty.task.title}`);
          console.log(`   💰 Reward: ${bounty.reward_formatted}`);
          console.log(`   📦 Repo: ${bounty.task.repo_owner}/${bounty.task.repo_name}`);
          console.log(`   🔗 URL: ${bounty.task.url}\n`);
        });

        // Try to get leaderboard for this org
        try {
          console.log(`🏆 Getting leaderboard for ${org}...`);
          const leaderboard = await algora.org.getLeaderboard.query({ org });

          if (leaderboard.length > 0) {
            console.log(`Found ${leaderboard.length} entries:\n`);
            leaderboard.slice(0, 3).forEach((entry, idx) => {
              console.log(`${idx + 1}. ${entry.user.name || entry.user.login}`);
              console.log(`   Completed: ${entry.stats.num_completed_bounties} bounties`);
              console.log(`   Earnings: $${entry.stats.total_earnings / 100}\n`);
            });
          } else {
            console.log("No leaderboard entries found.\n");
          }
        } catch (leaderboardError) {
          console.log(`Leaderboard error: ${leaderboardError.message}\n`);
        }

        // Get detailed info on first bounty
        try {
          console.log(`💰 Getting details for first bounty...`);
          const bounty = await algora.bounty.get.query({ id: result.items[0].id });

          console.log("\nBounty Details:");
          console.log(`Title: ${bounty.task.title}`);
          console.log(`Reward: ${bounty.reward_formatted}`);
          console.log(`Status: ${bounty.status}`);
          console.log(`Kind: ${bounty.kind}`);
          console.log(`Type: ${bounty.type}`);
          console.log(`Reward Type: ${bounty.reward_type}`);
          console.log(`Visibility: ${bounty.visibility}`);
          console.log(`Created: ${bounty.created_at}`);
          console.log(`Bids: ${bounty.bids.length}`);

          if (bounty.bids.length > 0) {
            console.log("\nBids:");
            bounty.bids.forEach((bid, idx) => {
              console.log(`  ${idx + 1}. $${bid.amount} by ${bid.user.name || bid.user.handle} (${bid.status})`);
            });
          }
        } catch (bountyError) {
          console.log(`Bounty details error: ${bountyError.message}\n`);
        }

        return; // Stop after finding first org with bounties
      } else {
        console.log(`No active bounties found.\n`);
      }
    } catch (error) {
      console.error(`Error: ${error.message}`);
    }
  }

  console.log("\n✨ Exploration complete!");
}

exploreAlgora().catch(console.error);
