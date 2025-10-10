#!/usr/bin/env node
/**
 * Figma API 403 问题自检脚本
 *
 * 用途：
 * - 快速确认你当前使用的 PAT（Personal Access Token）是否有权访问目标文件与节点
 * - 复现场景“有时行/有时不行”，区分权限 vs 其他问题
 *
 * 使用方式（任选其一）：
 * 1) 通过环境变量传入 PAT（推荐）
 *    PowerShell:
 *      $env:FIGMA_PAT = "YOUR_PAT"
 *      node tools/figma/check-api.mjs 1:1220 1:497
 *
 * 2) 作为第一个参数直接传入 PAT（适合一次性测试）
 *      node tools/figma/check-api.mjs YOUR_PAT 1:1220 1:497
 *
 * 说明：
 * - 未传入节点 ID 时，默认测试 1:1220 与 1:497
 * - 脚本会自动对冒号进行 URL 编码（: → %3A）
 * - Node.js 18+ 内置 fetch，若版本过低请升级或改用 curl
 */

const fileKey = "lXOwmixlbhaJZWc4w2pk1s";

const args = process.argv.slice(2);
let pat;
let nodeIds = [];

// 判定第一个参数是否为 PAT（粗略规则：不包含冒号）
if (args.length && !args[0].includes(":") && !args[0].includes("%3A")) {
  pat = args.shift();
  nodeIds = args;
} else {
  pat = process.env.FIGMA_PAT || process.env.FIGMA_API_TOKEN;
  nodeIds = args;
}

if (!nodeIds.length) {
  nodeIds = ["1:1220", "1:497"];
}

if (!pat) {
  console.error("错误：未提供 Figma PAT。请设置环境变量 FIGMA_PAT 或作为第一个参数传入。");
  process.exit(1);
}

const headers = { "X-Figma-Token": pat };

/**
 * 简单请求封装：返回 { status, ok, data?, text? }
 */
async function httpGet(url) {
  try {
    const res = await fetch(url, { headers });
    const contentType = res.headers.get("content-type") || "";
    let payload;
    if (contentType.includes("application/json")) {
      payload = await res.json().catch(() => undefined);
    } else {
      payload = await res.text().catch(() => undefined);
    }
    return { status: res.status, ok: res.ok, data: payload };
  } catch (err) {
    return { status: -1, ok: false, data: String(err) };
  }
}

async function checkMe() {
  const { status, ok, data } = await httpGet("https://api.figma.com/v1/me");
  if (!ok) {
    console.log(`[me] 失败，状态码=${status}`);
    console.log(data);
    return { ok: false };
  }
  const email = data?.email || "(unknown)";
  console.log(`[me] 成功，账号邮箱=${email}`);
  return { ok: true, email };
}

async function checkNode(nodeId) {
  const encodedId = encodeURIComponent(nodeId);
  const url = `https://api.figma.com/v1/files/${fileKey}/nodes?ids=${encodedId}`;
  const { status, ok, data } = await httpGet(url);

  if (!ok) {
    console.log(`[nodes:${nodeId}] 失败，状态码=${status}`);
    if (status === 403) {
      console.log(
        "- 403 Forbidden：PAT 有效，但该账号对目标文件无访问权限。\n" +
        "  请将 /v1/me 返回的邮箱邀请为该 Figma 文件的 Viewer/Editor，或使用有权限账号的 PAT。"
      );
    }
    if (status === 404) {
      console.log("- 404：fileKey 或 nodeId 不存在/不可见，请检查节点 ID 是否变化。");
    }
    if (status === 429) {
      console.log("- 429：限流，稍后重试或降低请求频率。");
    }
    try {
      console.log(typeof data === "string" ? data : JSON.stringify(data, null, 2));
    } catch {
      console.log(data);
    }
    return { ok: false };
  }

  // 成功
  const nodes = data?.nodes || {};
  const nodeEntry = nodes[nodeId] || Object.values(nodes)[0];
  const nodeName = nodeEntry?.document?.name || "(unknown)";
  const nodeType = nodeEntry?.document?.type || "(unknown)";
  console.log(`[nodes:${nodeId}] 成功，name=${nodeName}, type=${nodeType}`);
  return { ok: true, name: nodeName, type: nodeType };
}

(async function main() {
  console.log("=== Figma API 自检开始 ===");
  console.log(`fileKey=${fileKey}`);
  console.log(`待检查节点：${nodeIds.join(", ")}`);
  console.log("");

  const me = await checkMe();
  if (!me.ok) {
    console.log("请先确保 PAT 有效（/v1/me 应返回 200 且包含 email）。");
    process.exit(2);
  }

  for (const id of nodeIds) {
    await checkNode(id);
  }

  console.log("\n=== 自检结束 ===");
  console.log("若 /v1/me 成功但 /nodes 403，请将上述 email 邀请为 Figma 文件 Viewer/Editor，然后重试。");
})();
