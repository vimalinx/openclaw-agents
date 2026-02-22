import { algora } from "@algora/sdk";

function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }).format(amount);
}

function formatDate(date) {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(new Date(date));
}

async function showBounties(org, status = 'active') {
  console.log(`\n${"=".repeat(80)}`);
  console.log(`📋 ${org.toUpperCase()} - ${status.toUpperCase()} BOUNTIES`);
  console.log("=".repeat(80));

  try {
    const result = await algora.bounty.list.query({
      org,
      limit: 10,
      status
    });

    if (result.items.length === 0) {
      console.log("⚪ No bounties found.\n");
      return;
    }

    console.log(`\nFound ${result.items.length} ${status} bounties:\n`);

    result.items.forEach((bounty, idx) => {
      const reward = bounty.reward ? formatCurrency(bounty.reward.amount) : 'Points';
      const statusEmoji = bounty.status === 'active' ? '🟢' : '✅';

      console.log(`${statusEmoji} ${idx + 1}. ${bounty.task.title}`);
      console.log(`   💰 Reward: ${reward}`);
      console.log(`   📦 Repository: ${bounty.task.repo_owner}/${bounty.task.repo_name}`);
      console.log(`   🔗 Issue: ${bounty.task.url}`);
      console.log(`   📊 Type: ${bounty.kind} | ${bounty.reward_type}`);
      console.log(`   📅 Created: ${formatDate(bounty.created_at)}`);

      if (bounty.bids && bounty.bids.length > 0) {
        console.log(`   🏆 Bids: ${bounty.bids.length}`);
        bounty.bids.slice(0, 2).forEach((bid, bidIdx) => {
          console.log(`      ${bidIdx + 1}. $${bid.amount} by ${bid.user.name || bid.user.handle} (${bid.status})`);
        });
      }
      console.log();
    });

    // Calculate stats
    const totalReward = result.items
      .filter(b => b.reward)
      .reduce((sum, b) => sum + b.reward.amount, 0);

    const avgReward = result.items.filter(b => b.reward).length > 0
      ? totalReward / result.items.filter(b => b.reward).length
      : 0;

    console.log(`📊 Quick Stats:`);
    console.log(`   Total Rewards: ${formatCurrency(totalReward)}`);
    console.log(`   Average Reward: ${formatCurrency(avgReward)}`);
    console.log(`   Repositories: ${new Set(result.items.map(b => `${b.task.repo_owner}/${b.task.task_repo_name}`)).size}`);

  } catch (error) {
    console.error(`❌ Error: ${error.message}\n`);
  }
}

async function main() {
  console.log("🎯 Algora Bounty Viewer\n");

  // Show active bounties
  await showBounties("cal", "active");

  // Show completed bounties
  await showBounties("cal", "inactive");

  console.log("\n" + "=".repeat(80));
  console.log("💡 Tip: You can contribute to these bounties by visiting the issue URLs!");
  console.log("=".repeat(80) + "\n");
}

main().catch(console.error);
