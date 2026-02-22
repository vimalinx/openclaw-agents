#!/usr/bin/env node

/**
 * Algora Bounty Finder
 * 自动查找高价值悬赏任务并分析
 */

const https = require('https');

// Algora API base URL
const ALGORA_API_BASE = 'https://api.algora.io';

/**
 * 调用 Algora API
 */
async function callAlgoraAPI(endpoint, params = {}) {
  const url = new URL(`${ALGORA_API_BASE}${endpoint}`);
  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

  return new Promise((resolve, reject) => {
    https.get(url.toString(), {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; AlgoraBountyFinder/1.0)',
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const jsonData = JSON.parse(data);
          resolve(jsonData);
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

/**
 * 查找活跃的赏金任务
 */
async function findActiveBounties() {
  console.log('🔍 查找活跃的赏金任务...\n');

  try {
    // 尝试获取所有活跃的赏金任务
    const result = await callAlgoraAPI('/bounties', {
      status: 'active',
      limit: 100
    });

    return result;
  } catch (error) {
    console.error('获取赏金列表失败:', error.message);
    return null;
  }
}

/**
 * 筛选高赏金任务（>$5K）
 */
function filterHighValueBounties(bounties) {
  if (!bounties || !bounties.items) {
    return [];
  }

  return bounties.items.filter(bounty => {
    // 解析赏金金额（可能是数字或字符串格式）
    const reward = bounty.reward || bounty.reward_amount || 0;
    // 假设单位是美分，转换为美元
    const rewardUSD = typeof reward === 'number' ? reward / 100 : parseFloat(reward) || 0;

    return rewardUSD >= 5000;
  }).map(bounty => {
    const reward = bounty.reward || bounty.reward_amount || 0;
    const rewardUSD = typeof reward === 'number' ? reward / 100 : parseFloat(reward) || 0;

    return {
      ...bounty,
      rewardUSD,
      rewardFormatted: `$${rewardUSD.toLocaleString()}`
    };
  }).sort((a, b) => b.rewardUSD - a.rewardUSD);
}

/**
 * 分析任务技术栈
 */
function analyzeTechStack(bounty) {
  const repoName = bounty.task?.repo_name || '';
  const title = bounty.task?.title || '';
  const description = bounty.task?.body || '';

  // 检查关键词
  const techStack = [];

  const keywords = {
    'Python': ['python', 'py', 'django', 'flask', 'fastapi', 'pandas', 'numpy'],
    'TypeScript': ['typescript', 'ts', 'tsx'],
    'JavaScript': ['javascript', 'js', 'jsx', 'nodejs', 'node', 'react', 'vue', 'angular'],
    'Playwright': ['playwright', 'e2e', 'end-to-end'],
    'AI/ML': ['ai', 'ml', 'machine learning', 'artificial intelligence', 'openai', 'llm', 'gpt'],
    'Rust': ['rust', 'cargo'],
    'Go': ['golang', 'go'],
  };

  const text = `${repoName} ${title} ${description}`.toLowerCase();

  for (const [tech, keys] of Object.entries(keywords)) {
    if (keys.some(key => text.includes(key))) {
      techStack.push(tech);
    }
  }

  return techStack.length > 0 ? techStack : ['Unknown'];
}

/**
 * 格式化任务信息
 */
function formatBountyInfo(bounty) {
  const task = bounty.task || {};
  const techStack = analyzeTechStack(bounty);

  return `
📦 任务: ${task.title || 'N/A'}
💰 赏金: ${bounty.rewardFormatted}
🔗 链接: ${task.html_url || task.url || 'N/A'}
📂 仓库: ${task.repo_name || 'N/A'}
🏷️  Issue: #${task.number}
🛠️  技术栈: ${techStack.join(', ')}
📝 状态: ${bounty.status || 'active'}
`;
}

/**
 * 主函数
 */
async function main() {
  console.log('╔══════════════════════════════════════════════╗');
  console.log('║     Algora 高赏金任务查找器                 ║');
  console.log('╚══════════════════════════════════════════════╝\n');

  // 查找活跃任务
  const allBounties = await findActiveBounties();

  if (!allBounties) {
    console.log('❌ 无法获取赏金任务列表');
    console.log('\n💡 提示：可能需要 Algora API token');
    console.log('   请访问 https://algora.io 获取更多信息');
    return;
  }

  console.log(`📊 共找到 ${allBounties.items?.length || 0} 个活跃任务\n`);

  // 筛选高赏金任务
  const highValueBounties = filterHighValueBounties(allBounties);

  if (highValueBounties.length === 0) {
    console.log('😔 没有找到 $5K+ 的高赏金任务');
    console.log('💡 建议：降低赏金门槛查看更多任务\n');
  } else {
    console.log('🎯 找到以下高赏金任务（>$5K）:\n');
    console.log('═'.repeat(60));

    highValueBounties.forEach((bounty, index) => {
      console.log(formatBountyInfo(bounty));

      // 技术栈匹配度分析
      const techStack = analyzeTechStack(bounty);
      const matchedSkills = techStack.filter(t =>
        ['Python', 'TypeScript', 'Playwright', 'AI/ML'].includes(t)
      );

      if (matchedSkills.length > 0) {
        console.log(`✅ 匹配技能: ${matchedSkills.join(', ')}\n`);
      } else {
        console.log(`⚠️  技术栈不匹配\n`);
      }

      console.log('─'.repeat(60));
    });

    console.log(`\n📈 统计:`);
    console.log(`   高赏金任务总数: ${highValueBounties.length}`);
    const matched = highValueBounties.filter(b => {
      const techStack = analyzeTechStack(b);
      return techStack.some(t =>
        ['Python', 'TypeScript', 'Playwright', 'AI/ML'].includes(t)
      );
    });
    console.log(`   匹配技能栈的任务: ${matched.length}`);
    console.log(`   最高赏金: $${highValueBounties[0]?.rewardUSD?.toLocaleString() || 'N/A'}`);
  }

  // 保存结果到 JSON
  const result = {
    timestamp: new Date().toISOString(),
    totalBounties: allBounties.items?.length || 0,
    highValueBounties: highValueBounties.map(b => ({
      title: b.task?.title,
      rewardUSD: b.rewardUSD,
      rewardFormatted: b.rewardFormatted,
      url: b.task?.html_url || b.task?.url,
      repo: b.task?.repo_name,
      issueNumber: b.task?.number,
      techStack: analyzeTechStack(b)
    }))
  };

  const fs = require('fs');
  fs.writeFileSync(
    '/home/vimalinx/.openclaw/workspace/algora-bounties.json',
    JSON.stringify(result, null, 2)
  );

  console.log('\n💾 结果已保存到: algora-bounties.json');
}

// 运行
main().catch(console.error);
