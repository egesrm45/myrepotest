USE account;

ALTER TABLE `account`
ADD COLUMN `tradehouse_balance`  bigint(16) NULL DEFAULT 0 AFTER `coins`;