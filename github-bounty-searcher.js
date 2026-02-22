#!/usr/bin/env node

/**
 * GitHub Bounty Searcher
 * 搜索 GitHub 上带有赏金标签的 issues
 */

const https = require('https');

/**
 * 调用 GitHub API
 */
async function callGitHubAPI(endpoint, token = null) {
  const options = {
    hostname: 'api.github.com',
    path: endpoint,
    method: 'GET',
    headers: {
      'User-Agent': 'Mozilla/5.0 (compatible; GitHubBountySearcher/1.0)',
      'Accept': 'application/vnd.github.v3+json',
    }
  };

  if (token) {
    options.headers['Authorization'] = `token ${token}`;
  }

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          if (res.statusCode === 200) {
            const jsonData = JSON.parse(data);
            resolve(jsonData);
          } else {
            reject(new Error(`GitHub API returned status ${res.statusCode}`));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

/**
 * 搜索有赏金标签的 issues
 */
async function searchBountyIssues() {
  console.log('🔍 搜索 GitHub 上的赏金 issues...\n');

  try {
    // 搜索带有 bounty/bounty-hunting/bounties 标签的 issues
    const queries = [
      'label:bounty state:open',
      'label:"💎 Bounty" state:open',
      'label:bounty-hunting state:open',
    ];

    const allIssues = [];

    for (const query of queries) {
      try {
        console.log(`📡 查询: ${query}`);
        const results = await callGitHubAPI(`/search/issues?q=${encodeURIComponent(query)}&per_page=50&sort=created&order=desc`);
        console.log(`   找到 ${results.items?.length || 0} 个 issues\n`);
        allIssues.push(...(results.items || []));
      } catch (e) {
        console.log(`   查询失败: ${e.message}\n`);
      }
    }

    // 去重
    const uniqueIssues = allIssues.filter((issue, index, self) =>
      index === self.findIndex(i => i.id === issue.id)
    );

    return uniqueIssues;
  } catch (error) {
    console.error('搜索失败:', error.message);
    return [];
  }
}

/**
 * 从 issue body 中提取赏金金额
 */
function extractBountyAmount(body) {
  if (!body) return 0;

  // 尝试匹配各种赏金格式
  const patterns = [
    /[$€£]([\d,]+(?:\.\d{2})?)/gi,
    /bounty[:\s]+[$€£]?([\d,]+(?:\.\d{2})?)/gi,
    /reward[:\s]+[$€£]?([\d,]+(?:\.\d{2})?)/gi,
    /price[:\s]+[$€£]?([\d,]+(?:\.\d{2})?)/gi,
    /(\d{3,4})\s*USD/gi,
  ];

  let maxAmount = 0;

  for (const pattern of patterns) {
    const matches = body.match(pattern);
    if (matches) {
      for (const match of matches) {
        const amount = parseFloat(match.replace(/[^\d.]/g, ''));
        if (!isNaN(amount) && amount > maxAmount) {
          maxAmount = amount;
        }
      }
    }
  }

  return maxAmount;
}

/**
 * 分析技术栈
 */
function analyzeTechStack(issue) {
  const repoName = issue.repository_url || '';
  const title = issue.title || '';
  const body = issue.body || '';

  const text = `${repoName} ${title} ${body}`.toLowerCase();

  const techStack = [];

  const keywords = {
    'Python': ['python', 'py', 'django', 'flask', 'fastapi', 'pandas', 'numpy', '.py'],
    'TypeScript': ['typescript', 'ts', 'tsx', '.ts', '.tsx'],
    'JavaScript': ['javascript', 'js', 'jsx', 'nodejs', 'node', 'react', 'vue', 'angular', '.js', '.jsx'],
    'Playwright': ['playwright', 'e2e', 'end-to-end', 'testing'],
    'AI/ML': ['ai', 'ml', 'machine learning', 'artificial intelligence', 'openai', 'llm', 'gpt', 'chatgpt'],
    'Rust': ['rust', 'cargo', '.rs'],
    'Go': ['golang', 'go', '.go'],
    'Java': ['java', '.java', 'spring'],
    'C++': ['c++', 'cpp', '.cpp', '.h'],
  };

  for (const [tech, keys] of Object.entries(keywords)) {
    if (keys.some(key => text.includes(key))) {
      techStack.push(tech);
    }
  }

  return techStack.length > 0 ? techStack : ['Unknown'];
}

/**
 * 格式化 issue 信息
 */
function formatIssueInfo(issue) {
  const body = issue.body || '';
  const bountyAmount = extractBountyAmount(body);
  const techStack = analyzeTechStack(issue);

  // 提取仓库名
  const repoMatch = issue.repository_url?.match(/repos\/([^\/]+\/[^\/]+)/);
  const repoName = repoMatch ? repoMatch[1] : 'unknown';

  return `
📦 标题: ${issue.title}
💰 预估赏金: $${bountyAmount.toLocaleString() || '未知'}
🔗 链接: ${issue.html_url}
📂 仓库: ${repoName}
🏷️  Issue: #${issue.number}
🛠️  技术栈: ${techStack.join(', ')}
👤 创建者: ${issue.user?.login || 'unknown'}
📅 创建时间: ${new Date(issue.created_at).toLocaleDateString('zh-CN')}
⭐ Stars: ${issue.repository?.stargazers_count || 'N/A'}
📝 状态: ${issue.state}
`;
}

/**
 * 主函数
 */
async function main() {
  console.log('╔══════════════════════════════════════════════╗');
  console.log('║     GitHub 赏金任务搜索器                   ║');
  console.log('╚══════════════════════════════════════════════╝\n');

  // 搜索赏金 issues
  const issues = await searchBountyIssues();

  if (issues.length === 0) {
    console.log('😔 没有找到赏金任务');
    console.log('\n💡 提示：');
    console.log('   - 可能需要 GitHub API token 来增加搜索限制');
    console.log('   - 尝试访问 https://algora.io/bounties 查看官方赏金列表\n');
    return;
  }

  console.log(`📊 共找到 ${issues.length} 个赏金相关的 issues\n`);

  // 提取赏金金额并筛选高赏金任务
  const issuesWithBounty = issues.map(issue => {
    const body = issue.body || '';
    const bountyAmount = extractBountyAmount(body);
    const techStack = analyzeTechStack(issue);

    return {
      ...issue,
      bountyAmount,
      techStack
    };
  }).filter(issue => issue.bountyAmount > 0)
    .sort((a, b) => b.bountyAmount - a.bountyAmount);

  if (issuesWithBounty.length === 0) {
    console.log('😔 没有找到明确标注赏金金额的任务\n');
    console.log('显示前 10 个可能包含赏金的任务:\n');

    issues.slice(0, 10).forEach((issue, index) => {
      console.log(`${index + 1}. ${issue.title}`);
      console.log(`   ${issue.html_url}\n`);
    });
  } else {
    console.log('🎯 找到以下有明确赏金的任务:\n');
    console.log('═'.repeat(70));

    issuesWithBounty.forEach((issue, index) => {
      console.log(formatIssueInfo(issue));

      // 检查技能匹配
      const matchedSkills = issue.techStack.filter(t =>
        ['Python', 'TypeScript', 'Playwright', 'AI/ML'].includes(t)
      );

      if (matchedSkills.length > 0) {
        console.log(`✅ 匹配技能: ${matchedSkills.join(', ')}\n`);
      } else {
        console.log(`⚠️  技术栈不匹配\n`);
      }

      console.log('─'.repeat(70));
    });

    console.log(`\n📈 统计:`);
    console.log(`   带明确赏金的任务: ${issuesWithBounty.length}`);
    const matched = issuesWithBounty.filter(issue =>
      issue.techStack.some(t =>
        ['Python', 'TypeScript', 'Playwright', 'AI/ML'].includes(t)
      )
    );
    console.log(`   匹配技能栈的任务: ${matched.length}`);
    console.log(`   最高赏金: $${issuesWithBounty[0]?.bountyAmount?.toLocaleString() || 'N/A'}`);

    // 高赏金任务（>$5K）
    const highValue = issuesWithBounty.filter(i => i.bountyAmount >= 5000);
    if (highValue.length > 0) {
      console.log(`\n🎉 高赏金任务（>$5K）: ${highValue.length} 个\n`);
      highValue.forEach(issue => {
        console.log(`   💰 $${issue.bountyAmount.toLocaleString()} - ${issue.title}`);
        console.log(`      ${issue.html_url}\n`);
      });
    }
  }

  // 保存结果
  const fs = require('fs');
  const result = {
    timestamp: new Date().toISOString(),
    totalIssues: issues.length,
    issuesWithBounty: issuesWithBounty.map(issue => ({
      title: issue.title,
      bountyAmount: issue.bountyAmount,
      url: issue.html_url,
      repo: issue.repository_url,
      number: issue.number,
      techStack: issue.techStack
    }))
  };

  fs.writeFileSync(
    '/home/vimalinx/.openclaw/workspace/github-bounties.json',
    JSON.stringify(result, null, 2)
  );

  console.log('💾 结果已保存到: github-bounties.json');
}

// 运行
main().catch(console.error);
