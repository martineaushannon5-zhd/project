<template>
  <div class="author-page portal-fade-up">
    <div class="author-hero">
      <div class="hero-orb hero-orb-left"></div>
      <div class="hero-orb hero-orb-right"></div>
      
      <div class="author-profile">
        <div class="avatar-ring">
          <img src="./touxiang.jpg" alt="Author Avatar" class="avatar-img" />
        </div>
        <h1 class="author-name">Full-Stack Developer</h1>
        <p class="author-bio">致力于打造高颜值、高性能的现代 Web 应用。全栈开发工程师，热爱开源与技术分享。</p>
        
        <div class="author-tags">
          <span class="tag tech-vue">Vue 3</span>
          <span class="tag tech-fastapi">FastAPI</span>
          <span class="tag tech-node">Node.js</span>
          <span class="tag tech-ts">TypeScript</span>
          <span class="tag tech-db">TiDB Serverless</span>
        </div>
      </div>
    </div>

    <div class="author-content">
      <div class="content-grid">
        <div class="info-card">
          <div class="card-icon"><el-icon><Monitor /></el-icon></div>
          <h3>专注领域</h3>
          <p>个人品牌门户、博客系统开发。自习室、会议室等预约调度系统的高效全栈解决方案。</p>
        </div>
        
        <div class="info-card">
          <div class="card-icon"><el-icon><MagicStick /></el-icon></div>
          <h3>设计理念</h3>
          <p>追求极致的用户体验与现代 SaaS 风格 UI。喜欢轻量级卡片、弥散阴影及舒适的色彩搭配。</p>
        </div>

        <div class="info-card">
          <div class="card-icon"><el-icon><Cloudy /></el-icon></div>
          <h3>部署架构</h3>
          <p>擅长云端自动化部署与公网 架构。Vercel + Render + 线上 Serverless 数据库的高可用配置。</p>
        </div>
      </div>

      <div class="project-showcase">
        <h2>关于本项目 (Study Room Booking)</h2>
        <div class="showcase-box">
          <div class="showcase-text">
            <p>本项目是一个基于 <strong>Vue 3 (前端)</strong> 和 <strong>FastAPI (后端)</strong> 构建的现代化自习室预约系统。它拥有独立的轻量级学生端和极端硬核的运营控制台。</p>
            <ul class="feature-list">
              <li><el-icon><Check /></el-icon> 实时空间节点负载监控与预警</li>
              <li><el-icon><Check /></el-icon> 可视化座位矩阵与物理空间划分</li>
              <li><el-icon><Check /></el-icon> 完整的权限与通知反馈体系</li>
              <li><el-icon><Check /></el-icon> 暗黑/亮色主题深度定制</li>
            </ul>
          </div>
          <div class="showcase-actions">
            <el-button type="primary" size="large" class="action-btn github-btn" @click="goGithub">
              <el-icon class="btn-icon"><Position /></el-icon>
              访问 GitHub 仓库
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Monitor, MagicStick, Cloudy, Check, Position } from '@element-plus/icons-vue'

const goGithub = () => {
  window.open('https://github.com/', '_blank')
}
</script>

<style scoped>
.author-page {
  max-width: 1000px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.author-hero {
  position: relative;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 32px;
  padding: 60px 20px;
  text-align: center;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.05);
  overflow: hidden;
  margin-bottom: 40px;
}

.hero-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
  z-index: 0;
  opacity: 0.5;
}

.hero-orb-left {
  width: 300px;
  height: 300px;
  background: #dbeafe;
  top: -100px;
  left: -100px;
}

.hero-orb-right {
  width: 250px;
  height: 250px;
  background: #ede9fe;
  bottom: -50px;
  right: -50px;
}

.author-profile {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-ring {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  padding: 6px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
  margin-bottom: 24px;
}

.avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #fff;
  object-fit: cover;
}

.author-name {
  font-size: 32px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 12px;
  letter-spacing: -0.02em;
}

.author-bio {
  font-size: 16px;
  color: #475569;
  max-width: 500px;
  line-height: 1.6;
  margin: 0 0 24px;
}

.author-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.tag {
  padding: 6px 16px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid transparent;
}

.tech-vue { background: #ecfdf5; color: #059669; border-color: #a7f3d0; }
.tech-fastapi { background: #eff6ff; color: #2563eb; border-color: #bfdbfe; }
.tech-node { background: #f0fdf4; color: #16a34a; border-color: #bbf7d0; }
.tech-ts { background: #eef2ff; color: #4f46e5; border-color: #c7d2fe; }
.tech-db { background: #fffbeb; color: #d97706; border-color: #fde68a; }

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.info-card {
  background: #ffffff;
  padding: 32px 24px;
  border-radius: 24px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px -10px rgba(37, 99, 235, 0.1);
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: #eff6ff;
  color: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.info-card h3 {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 12px;
}

.info-card p {
  font-size: 14px;
  color: #64748b;
  line-height: 1.7;
  margin: 0;
}

.project-showcase {
  background: #ffffff;
  border-radius: 28px;
  padding: 40px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
}

.project-showcase h2 {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 24px;
}

.showcase-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}

.showcase-text p {
  font-size: 15px;
  color: #475569;
  line-height: 1.7;
  margin: 0 0 20px;
}

.showcase-text strong {
  color: #0f172a;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #334155;
}

.feature-list .el-icon {
  color: #10b981;
  font-weight: bold;
}

.showcase-actions {
  flex-shrink: 0;
}

.action-btn {
  height: 48px;
  padding: 0 28px;
  border-radius: 999px;
  font-size: 15px;
  font-weight: 600;
}

.github-btn {
  background: #0f172a;
  border-color: #0f172a;
  color: #fff;
  transition: all 0.3s ease;
}

.github-btn:hover {
  background: #1e293b;
  border-color: #1e293b;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.2);
}

.btn-icon {
  margin-right: 6px;
  font-size: 18px;
}

@media (max-width: 768px) {
  .showcase-box {
    flex-direction: column;
    align-items: flex-start;
  }
  .feature-list {
    grid-template-columns: 1fr;
  }
  .project-showcase {
    padding: 24px;
  }
}
</style>
