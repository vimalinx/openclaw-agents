import { algora } from "@algora/sdk";
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function question(query) {
  return new Promise((resolve) => {
    rl.question(query, resolve);
  });
}

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

async function listBounties(org, filters = {}) {
  try {
    const result = await algora.bounty.list.query({
      org,
      limit: filters.limit || 20,
      status: filters.status || 'active'
    });

    return result.items;
  } catch (error) {
    console.error(`Error: ${error.message}`);
    return [];
  }
}

function displayBounty(bounty, idx) {
  const reward = bounty.reward ? formatCurrency(bounty.reward.amount) : 'Points';
  const statusEmoji = bounty.status === 'active' ? '🟢' : '✅';

  console.log(`\n${statusEmoji} [#${idx + 1}] ${bounty.task.title}`);
  console.log(`   💰 ${reward} | 📦 ${bounty.task.repo_owner}/${bounty.task.repo_name}`);
  console.log(`   🔗 ${bounty.task.url}`);
  console.log(`   📅 ${formatDate(bounty.created_at)} | Type: ${bounty.kind}`);

  if (bounty.bids && bounty.bids.length > 0) {
    console.log(`   🏆 ${bounty.bids.length} bid(s)`);
  }
}

async function showMenu() {
  console.log("\n" + "=".repeat(70));
  console.log("🎯 Algora Bounty Explorer");
  console.log("=".repeat(70));
  console.log("\n1. List bounties for an organization");
  console.log("2. Search popular organizations");
  console.log("3. Show bounty statistics");
  console.log("4. Exit");
  console.log("\nSelect an option:");
}

async function searchPopularOrgs() {
  console.log("\n🔍 Searching for organizations with bounties...");

  const popularOrgs = [
    "cal", "vercel", "remotion-dev", "stripe", "supabase",
    "nextjs", "tailwindlabs", "mdn", "facebook", "google",
    "microsoft", "github", "gitlab", "docker", "kubernetes",
    "angular", "reactjs", "vuejs", "nodejs", "deno"
  ];

  console.log("\nChecking organizations... (this may take a moment)\n");

  const orgsWithBounties = [];

  for (const org of popularOrgs) {
    try {
      const result = await algora.bounty.list.query({
        org,
        limit: 1,
        status: 'active'
      });

      if (result.items.length > 0) {
        orgsWithBounties.push({ org, count: result.items.length });
        console.log(`✅ ${org} has bounties!`);
      }
    } catch (error) {
      // Silently skip orgs without bounties or errors
    }
  }

  if (orgsWithBounties.length > 0) {
    console.log(`\n🎉 Found ${orgsWithBounties.length} organizations with bounties!`);
    orgsWithBounties.forEach(({ org, count }) => {
      console.log(`   • ${org}`);
    });
  } else {
    console.log("\n⚪ No organizations found with active bounties.");
  }
}

async function showStats(org) {
  console.log(`\n📊 Statistics for ${org}`);

  try {
    const active = await algora.bounty.list.query({ org, limit: 100, status: 'active' });
    const inactive = await algora.bounty.list.query({ org, limit: 100, status: 'inactive' });

    const activeReward = active.items
      .filter(b => b.reward)
      .reduce((sum, b) => sum + b.reward.amount, 0);

    const inactiveReward = inactive.items
      .filter(b => b.reward)
      .reduce((sum, b) => sum + b.reward.amount, 0);

    const avgActive = active.items.filter(b => b.reward).length > 0
      ? activeReward / active.items.filter(b => b.reward).length
      : 0;

    const repos = new Set([
      ...active.items.map(b => `${b.task.repo_owner}/${b.task.repo_name}`),
      ...inactive.items.map(b => `${b.task.repo_owner}/${b.task.repo_name}`)
    ]);

    console.log(`\nActive Bounties: ${active.items.length}`);
    console.log(`Completed Bounties: ${inactive.items.length}`);
    console.log(`\n💰 Active Rewards: ${formatCurrency(activeReward)}`);
    console.log(`💰 Total Paid Out: ${formatCurrency(inactiveReward)}`);
    console.log(`💰 Average Reward: ${formatCurrency(avgActive)}`);
    console.log(`\n📦 Unique Repositories: ${repos.size}`);
    console.log(`\nRepositories:`);
    Array.from(repos).forEach(repo => console.log(`   • ${repo}`));

    // Bounty type breakdown
    const kinds = {};
    [...active.items, ...inactive.items].forEach(b => {
      kinds[b.kind] = (kinds[b.kind] || 0) + 1;
    });

    console.log(`\nBounty Types:`);
    Object.entries(kinds).forEach(([kind, count]) => {
      console.log(`   • ${kind}: ${count}`);
    });

  } catch (error) {
    console.error(`Error getting stats: ${error.message}`);
  }
}

async function main() {
  console.clear();
  console.log("🚀 Welcome to Algora Bounty Explorer!");

  let running = true;

  while (running) {
    await showMenu();
    const choice = await question("> ");

    switch (choice.trim()) {
      case '1':
        const org = await question("\nEnter organization name (e.g., cal): ");
        const status = await question("Status (active/inactive) [default: active]: ") || 'active';

        console.log("\n🔍 Searching...");
        const bounties = await listBounties(org.trim(), { status: status.trim() });

        if (bounties.length > 0) {
          console.log(`\n✅ Found ${bounties.length} ${status} bounties for ${org}`);
          bounties.slice(0, 10).forEach((bounty, idx) => displayBounty(bounty, idx));

          if (bounties.length > 10) {
            console.log(`\n... and ${bounties.length - 10} more`);
          }
        } else {
          console.log(`\n⚪ No bounties found for ${org}`);
        }

        await question("\nPress Enter to continue...");
        break;

      case '2':
        await searchPopularOrgs();
        await question("\nPress Enter to continue...");
        break;

      case '3':
        const orgForStats = await question("\nEnter organization name: ");
        await showStats(orgForStats.trim());
        await question("\nPress Enter to continue...");
        break;

      case '4':
        console.log("\n👋 Goodbye!");
        running = false;
        break;

      default:
        console.log("\n❌ Invalid option. Please try again.");
        await question("\nPress Enter to continue...");
    }

    console.clear();
  }

  rl.close();
}

main().catch(console.error);
