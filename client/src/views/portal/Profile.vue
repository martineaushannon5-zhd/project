<template>
  <div class="profile-page">
    <section class="profile-hero portal-fade-up">
      <div class="hero-copy">
        <div class="kicker">PROFILE / STUDENT CENTER</div>
        <h1>PERSONAL CONTROL ROOM</h1>
        <p>这里是你的个人中心。查看资料、预约状态、学习足迹与反馈记录，让自习安排更清晰。</p>
        <div class="hero-actions">
          <el-button class="primary-btn" @click="go('/portal/my-reservations')">查看预约</el-button>
          <el-button class="outline-btn" @click="go('/portal/feedback')">提交反馈</el-button>
        </div>
      </div>

      <div class="hero-status floating-card">
        <div class="status-band"></div>
        <div class="status-grid">
          <div>
            <span>USER</span>
            <strong>{{ user?.username || 'STUDENT' }}</strong>
          </div>
          <div>
            <span>ROLE</span>
            <strong>{{ roleText }}</strong>
          </div>
          <div>
            <span>NAME</span>
            <strong>{{ user?.real_name || '—' }}</strong>
          </div>
          <div>
            <span>STATUS</span>
            <strong class="status-active">ACTIVE</strong>
          </div>
        </div>
      </div>
    </section>

    <section class="profile-bands">
      <div class="profile-card profile-card-summary portal-hover">
        <div class="card-label">ACCOUNT SUMMARY</div>
        <div class="summary-list">
          <div class="summary-row">
            <span>用户名</span>
            <strong>{{ user?.username || '—' }}</strong>
          </div>
          <div class="summary-row">
            <span>真实姓名</span>
            <strong>{{ user?.real_name || '未填写' }}</strong>
          </div>
          <div class="summary-row">
            <span>账号角色</span>
            <strong>{{ roleText }}</strong>
          </div>
          <div class="summary-row">
            <span>登录入口</span>
            <strong>PORTAL</strong>
          </div>
        </div>
      </div>

      <div class="profile-card profile-card-tracks portal-hover">
        <div class="card-label">LIFE TRACKS</div>
        <div class="track-grid">
          <div class="track-item" @click="go('/portal/booking')">
            <span>预约入口</span>
            <strong>BOOKING</strong>
            <p>快速进入座位预约页面，按时间段选位。</p>
          </div>
          <div class="track-item" @click="go('/portal/my-reservations')">
            <span>签到与取消</span>
            <strong>CHECK-IN</strong>
            <p>在我的预约中完成签到或取消操作。</p>
          </div>
          <div class="track-item" @click="go('/portal/feedback')">
            <span>意见反馈</span>
            <strong>FEEDBACK</strong>
            <p>向管理员提交建议、问题与留言。</p>
          </div>
          <div class="track-item" @click="go('/portal/notices')">
            <span>公告信息</span>
            <strong>NOTICE</strong>
            <p>第一时间掌握自习室通知动态。</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))
const roleText = computed(() => (user.value?.role === 'admin' ? 'ADMIN' : 'STUDENT'))
const go = (path: string) => router.push(path)
</script>

<style scoped>
.profile-page {
  /* 移除黑色背景，由父组件 Layout 的浅色背景接管，或者保留透明 */
  background: transparent;
  color: #0f172a;
  min-height: calc(100vh - 160px);
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-hero {
  position: relative;
  overflow: hidden;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 24px;
  align-items: stretch;
  min-height: 400px;
  padding: 44px;
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 24px;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.04);
}

.profile-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 80% 20%, rgba(37, 99, 235, 0.04), transparent 24%),
              radial-gradient(circle at 12% 70%, rgba(124, 58, 237, 0.04), transparent 18%);
  pointer-events: none;
}

.kicker {
  color: #2563eb;
  font-size: 14px;
  letter-spacing: 1.8px;
  font-weight: 800;
  text-transform: uppercase;
}

.hero-copy {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-copy h1 {
  margin: 14px 0 16px;
  font-size: 56px;
  line-height: 1.05;
  letter-spacing: -0.5px;
  text-transform: uppercase;
  font-weight: 800;
  background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-copy p {
  max-width: 600px;
  color: #64748b;
  line-height: 1.8;
  font-size: 16px;
  font-weight: 400;
}

.hero-actions {
  display: flex;
  gap: 14px;
  margin-top: 32px;
}

.primary-btn,
.outline-btn {
  height: 48px;
  border-radius: 12px !important;
  letter-spacing: 1px;
  font-weight: 700;
  padding: 0 26px;
  border: none;
  transition: all 0.3s ease;
}

.primary-btn {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #fff;
  box-shadow: 0 8px 16px rgba(37, 99, 235, 0.2);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 20px rgba(37, 99, 235, 0.3);
}

.outline-btn {
  background: #f8fafc;
  color: #0f172a;
  border: 1px solid #e2e8f0;
}

.outline-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #2563eb;
}

.hero-status {
  position: relative;
  z-index: 1;
  align-self: center;
  padding: 32px;
  border-radius: 20px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  background: linear-gradient(180deg, #ffffff, #f8fafc);
  box-shadow: 0 16px 32px rgba(15, 23, 42, 0.06);
}

.status-band {
  height: 4px;
  border-radius: 4px;
  background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
  margin-bottom: 24px;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.status-grid span,
.card-label,
.track-item span {
  font-size: 12px;
  color: #94a3b8;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  font-weight: 600;
}

.status-grid strong {
  display: block;
  margin-top: 6px;
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
}

.status-active {
  color: #10b981 !important;
}

.profile-bands {
  display: grid;
  grid-template-columns: 0.85fr 1.15fr;
  gap: 24px;
}

.profile-card {
  min-height: 320px;
  padding: 36px;
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 24px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.03);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px rgba(15, 23, 42, 0.06);
}

.card-label {
  margin-bottom: 24px;
  color: #64748b;
}

.summary-list {
  display: grid;
  gap: 0;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid #f1f5f9;
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-row span {
  color: #64748b;
  font-weight: 500;
}

.summary-row strong {
  color: #0f172a;
  font-weight: 700;
}

.track-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.track-item {
  padding: 20px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.track-item:hover {
  background: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
  transform: translateY(-2px);
}

.track-item strong {
  display: block;
  margin: 6px 0 8px;
  font-size: 24px;
  line-height: 1.1;
  font-weight: 800;
  color: #0f172a;
  text-transform: uppercase;
}

.track-item p {
  margin: 0;
  color: #64748b;
  line-height: 1.6;
  font-size: 13px;
  font-weight: 400;
}

.floating-card {
  animation: floatY 6s ease-in-out infinite;
}

@keyframes floatY {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

@media (max-width: 1100px) {
  .profile-hero,
  .profile-bands {
    grid-template-columns: 1fr;
  }

  .hero-copy h1 {
    font-size: 44px;
  }
}

@media (max-width: 768px) {
  .profile-page {
    gap: 16px;
  }

  .profile-hero {
    padding: 28px 20px;
    border-radius: 20px;
  }

  .hero-copy h1 {
    font-size: 36px;
  }

  .hero-actions {
    flex-direction: column;
    width: 100%;
  }

  .primary-btn, .outline-btn {
    width: 100%;
  }

  .status-grid,
  .track-grid {
    grid-template-columns: 1fr;
  }

  .profile-card {
    padding: 24px 20px;
    border-radius: 20px;
  }
}
</style>
