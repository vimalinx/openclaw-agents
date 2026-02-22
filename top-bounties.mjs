import { algora } from "@algora/sdk";

async function showTopBounties() {
  const args = process.argv.slice(2);
  const limit = parseInt(args[0]) || 10;

  console.log(`💰 Top ${limit} Highest Bounties\n`);
  console.log("=".repeat(70));

  const orgs = [
    "cal", "vercel", "remotion-dev", "stripe", "supabase",
    "nextjs", "tailwindlabs", "mdn", "reactjs", "vuejs",
    "nodejs", "deno", "docker", "kubernetes", "angular",
    "facebook", "google", "microsoft", "github", "gitlab"
  ];

  const allBounties = [];

  console.log("\n🔍 Scanning organizations...");

  for (const org of orgs) {
    try {
      const result = await algora.bounty.list.query({
        org,
        limit: 100,
        status: 'active'
      });

      const bountiesWithReward = result.items.filter(b => b.reward);
      allBounties.push(...bountiesWithReward.map(b => ({ ...b, org })));
    } catch (error) {
      // Skip errors
    }
  }

  // Sort by reward amount (descending)
  allBounties.sort((a, b) => b.reward.amount - a.reward.amount);

  // Get top N
  const topBounties = allBounties.slice(0, limit);

  if (topBounties.length === 0) {
    console.log("\n⚪ No bounties found.\n");
    return;
  }

  console.log(`\n✅ Found ${allBounties.length} total bounties, showing top ${limit}:\n`);

  topBounties.forEach((bounty, idx) => {
    const rank = idx + 1;
    const medal = rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : ` #${rank}`;

    console.log(`${medal} $${bounty.reward.amount.toLocaleString()} - ${bounty.task.title}`);
    console.log(`   📦 ${bounty.task.repo_owner}/${bounty.task.repo_name}`);
    console.log(`   🔗 ${bounty.task.url}`);
    console.log(`   📊 ${bounty.org.org.handle} | ${bounty.kind} | ${bounty.reward_type}`);
    console.log(`   📅 Created: ${new Date(bounty.created_at).toLocaleDateString()}\n`);
  });

  // Statistics
  const totalReward = allBounties.reduce((sum, b) => sum + b.reward.amount, 0);
  const avgReward = totalReward / allBounties.length;
  const orgsFound = [...new Set(allBounties.map(b => b.org.org.handle))];
  const reposFound = [...new Set(allBounties.map(b => `${b.task.repo_owner}/${b.task.repo_name}`))];

  console.log("=".repeat(70));
  console.log(`\n📊 Market Overview:`);
  console.log(`   Total bounties: ${allBounties.length}`);
  console.log(`   Total value: $${totalReward.toLocaleString()}`);
  console.log(`   Average: $${avgReward.toLocaleString().split('.')[0]}`);
  console.log(`   Organizations: ${orgsFound.length}`);
  console.log(`   Repositories: ${reposFound.length}`);
  console.log(`   Range: $${Math.min(...allBounties.map(b => b.reward.amount)).toLocaleString()} - $${Math.max(...allBounties.map(b => b.reward.amount)).toLocaleString()}`);

  // Reward distribution
  const ranges = [
    { label: '$0-$1,000', min: 0, max: 1000 },
    { label: '$1,000-$5,000', min: 1000, max: 5000 },
    { label: '$5,000-$10,000', min: 5000, max: 10000 },
    { label: '$10,000-$50,000', min: 10000, max: 50000 },
    { label: '$50,000+', min: 50000, max: Infinity }
  ];

  console.log(`\n📈 Reward Distribution:`);
  ranges.forEach(({ label, min, max }) => {
    const count = allBounties.filter(b => b.reward.amount >= min && b.reward.amount < max).length;
    const percentage = ((count / allBounties.length) * 100).toFixed(1);
    const bar = '█'.repeat(Math.round(percentage / 2));
    console.log(`   ${label.padEnd(18)} ${count.toString().padStart(3)} (${percentage.padStart(4)}%) ${bar}`);
  });

  console.log(`\n📦 Top Organizations by Bounty Count:`);
  const orgCounts = {};
  allBounties.forEach(b => {
    orgCounts[b.org.org.handle] = (orgCounts[b.org.org.handle] || 0) + 1;
  });

  Object.entries(orgCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .forEach(([org, count], idx) => {
      const percentage = ((count / allBounties.length) * 100).toFixed(1);
      console.log(`   ${(idx + 1).toString().padStart(2)}. ${org.padEnd(15)} ${count.toString().padStart(3)} bounties (${percentage}%)`);
    });

  console.log("\n" + "=".repeat(70) + "\n");
}

showTopBounties().catch(console.error);
