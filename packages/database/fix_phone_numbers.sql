-- 修复电话号码前导零丢失问题的SQL脚本
-- 类似于邮政编码的修复，为9位数字的电话号码添加前导零

-- 更新agent_phone字段，为9位数字的电话号码添加前导零
UPDATE properties
SET agent_phone = CONCAT('0', agent_phone)
WHERE LENGTH(agent_phone) = 9 
  AND agent_phone ~ '^[0-9]+$' -- 确保只包含数字
  AND agent_phone NOT LIKE '0%'; -- 确保不以0开头

-- 输出更新的行数
SELECT 'Updated ' || COUNT(*) || ' phone numbers by adding leading zero.' AS update_summary
FROM properties
WHERE LENGTH(agent_phone) = 10 
  AND agent_phone ~ '^0[0-9]+$' -- 以0开头的10位数字
  AND agent_phone LIKE '0%';