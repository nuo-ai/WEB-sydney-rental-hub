/**
 * URL Query 实用函数
 * 目标：
 * 1) 仅写入“非空有效键”，避免 URL 被空值污染
 * 2) 稳定键顺序（以字母序），防止由于序列化顺序差异导致的 replace 循环
 * 3) 写前对比，若与当前完全一致则不写，避免无意义的 history 变更
 */

/**
 * 判断一个值是否为“空”：
 * - null / undefined / '' 视为空
 * - 对象：无自有键视为空
 * - 数组：长度为 0 视为空
 */
export function isEmptyVal(v) {
  if (v === null || v === undefined) return true;
  if (typeof v === 'string') return v.trim() === '';
  if (Array.isArray(v)) return v.length === 0;
  if (typeof v === 'object') return Object.keys(v).length === 0;
  return false;
}

/**
 * 生成“仅包含非空键”的浅拷贝，并按字母序稳定排序键
 * - 将值统一转为字符串（URLSearchParams 的常见行为），保证比较一致性
 */
export function sanitizeQueryParams(input) {
  try {
    const q = {};
    if (input && typeof input === 'object') {
      Object.keys(input).forEach((k) => {
        const v = input[k];
        if (!isEmptyVal(v)) {
          // 统一序列化为字符串（数组/对象由上层控制，不在此展开）
          q[k] = String(v);
        }
      });
    }
    // 稳定键顺序（按字母序）
    const sorted = {};
    Object.keys(q)
      .sort((a, b) => a.localeCompare(b))
      .forEach((k) => (sorted[k] = q[k]));
    return sorted;
  } catch {
    // 发生异常时，返回一个空对象，避免污染 URL
    return {};
  }
}

/**
 * 对比两个 query 是否“键值完全一致”
 * - 仅比较自有可枚举键（不比较原型链）
 * - 忽略顺序差异
 */
export function isSameQuery(a, b) {
  const ka = (a && typeof a === 'object') ? Object.keys(a) : [];
  const kb = (b && typeof b === 'object') ? Object.keys(b) : [];
  if (ka.length !== kb.length) return false;
  // 使用 Set 加速包含判断
  const setB = new Set(kb);
  for (const k of ka) {
    if (!setB.has(k)) return false;
  }
  // 值比较：统一按字符串比较（与 sanitize 行为一致）
  for (const k of ka) {
    const va = a[k];
    const vb = b[k];
    if (String(va) !== String(vb)) return false;
  }
  return true;
}
