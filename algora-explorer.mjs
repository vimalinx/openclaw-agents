import { algora } from "@algora/sdk";

async function exploreAlgora() {
  console.log("🔍 Exploring Algora SDK...\n");

  // Test 1: List bounties from a popular organization
  console.log("📋 Test 1: Listing active bounties...");
  try {
    const result = await algora.bounty.list.query({
      org: "acme",  // Using acme as example
      limit: 5,
      status: "active"
    });

    console.log(`Found ${result.items.length} bounties:\n`);
    result.items.forEach((bounty, idx) => {
      console.log(`${idx + 1}. ${bounty.task.title}`);
      console.log(`   Reward: ${bounty.reward_formatted}`);
      console.log(`   Repo: ${bounty.task.repo_owner}/${bounty.task.repo_name}`);
      console.log(`   Issue: #${bounty.task.number}`);
      console.log(`   URL: ${bounty.task.url}\n`);
    });
  } catch (error) {
    console.error("Error listing bounties:", error.message);
  }

  // Test 2: Get organization leaderboard
  console.log("\n🏆 Test 2: Getting organization leaderboard...");
  try {
    const leaderboard = await algora.org.getLeaderboard.query({
      org: "acme"
    });

    console.log(`Found ${leaderboard.length} leaderboard entries:\n`);
    leaderboard.slice(0, 5).forEach((entry, idx) => {
      console.log(`${idx + 1}. ${entry.user.name || entry.user.login} (@${entry.user.login})`);
      console.log(`   Completed: ${entry.stats.num_completed_bounties} bounties`);
      console.log(`   Earnings: $${entry.stats.total_earnings / 100}\n`);
    });
  } catch (error) {
    console.error("Error getting leaderboard:", error.message);
  }

  // Test 3: Try to get a specific bounty
  console.log("\n💰 Test 3: Getting bounty details...");
  if (result && result.items.length > 0) {
    try {
      const bountyId = result.items[0].id;
      const bounty = await algora.bounty.get.query({ id: bountyId });

      console.log("Bounty Details:");
      console.log(`Title: ${bounty.task.title}`);
      console.log(`Reward: ${bounty.reward_formatted}`);
      console.log(`Status: ${bounty.status}`);
      console.log(`Type: ${bounty.type}`);
      console.log(`Visibility: ${bounty.visibility}`);
      console.log(`Created: ${bounty.created_at}`);
      console.log(`Bids: ${bounty.bids.length}\n`);
    } catch (error) {
      console.error("Error getting bounty details:", error.message);
    }
  }
}

exploreAlgora().catch(console.error);
