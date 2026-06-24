-- 数据库：study_room (Python自习室预约管理系统)
CREATE DATABASE IF NOT EXISTS study_room DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE study_room;

-- 1. 用户表
CREATE TABLE IF NOT EXISTS `user` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
  `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名/学号',
  `password` VARCHAR(100) NOT NULL COMMENT '密码（明文：123456）',
  `real_name` VARCHAR(255) DEFAULT NULL COMMENT '真实姓名',
  `role` VARCHAR(20) DEFAULT 'student' COMMENT '角色：admin-管理员, student-学生',
  `avatar` VARCHAR(255) DEFAULT NULL COMMENT '头像路径',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 2. 自习室/区域表
CREATE TABLE IF NOT EXISTS `room` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自习室ID',
  `name` VARCHAR(50) NOT NULL COMMENT '自习室名称',
  `description` VARCHAR(255) DEFAULT NULL COMMENT '描述',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='自习室表';

-- 3. 座位表
CREATE TABLE IF NOT EXISTS `seat` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '座位ID',
  `room_id` INT NOT NULL COMMENT '所属自习室ID',
  `seat_number` VARCHAR(20) NOT NULL COMMENT '座位号',
  `status` INT DEFAULT 1 COMMENT '状态：1-正常, 0-维护中',
  `has_power` TINYINT(1) DEFAULT 1 COMMENT '是否有电源',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (`room_id`) REFERENCES `room`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='座位表';

-- 4. 预约记录表
CREATE TABLE IF NOT EXISTS `reservation` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '预约ID',
  `user_id` INT NOT NULL COMMENT '预约用户ID',
  `seat_id` INT NOT NULL COMMENT '预约座位ID',
  `date` DATE NOT NULL COMMENT '预约日期',
  `start_time` TIME NOT NULL COMMENT '开始时间',
  `end_time` TIME NOT NULL COMMENT '结束时间',
  `status` VARCHAR(20) DEFAULT 'pending' COMMENT '状态：pending-待使用, active-使用中, completed-已完成, cancelled-已取消',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`seat_id`) REFERENCES `seat`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='预约记录表';

-- 插入测试数据
INSERT INTO `user` (`username`, `password`, `real_name`, `role`) VALUES 
('admin', '123456', 'admin', 'admin'),
('student1', '123456', 'student1', 'student'),
('student2', '123456', 'student2', 'student');

INSERT INTO `room` (`name`, `description`) VALUES 
('A区 沉浸自习室', '安静无声，适合深度学习'),
('B区 讨论自习室', '允许小声讨论，配备白板');

INSERT INTO `seat` (`room_id`, `seat_number`, `status`, `has_power`) VALUES 
(1, 'A-01', 1, 1),
(1, 'A-02', 1, 1),
(1, 'A-03', 1, 0),
(2, 'B-01', 1, 1),
(2, 'B-02', 1, 1);

INSERT INTO `reservation` (`user_id`, `seat_id`, `date`, `start_time`, `end_time`, `status`) VALUES 
(2, 1, CURDATE(), '08:00:00', '12:00:00', 'completed'),
(3, 4, CURDATE(), '14:00:00', '18:00:00', 'pending');
