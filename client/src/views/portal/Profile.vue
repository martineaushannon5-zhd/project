<template>
  <div class="portal-shell profile-page">
    <section class="profile-hero portal-fade-up hover-card">
      <div class="hero-copy">
        <div class="kicker">PROFILE / STUDENT CENTER</div>
        <h1>PERSONAL CONTROL ROOM</h1>
        <p>这里是你的个人中心。查看资料、预约状态、学习足迹与反馈记录，让自习安排更清晰。</p>
        <div class="hero-actions">
          <el-button type="primary" class="primary-btn" @click="go('/portal/my-reservations')">查看预约</el-button>
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
      <div class="profile-card profile-card-light portal-hover">
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
            <el-tag :type="user?.role === 'admin' ? 'danger' : 'primary'" size="small" effect="light" class="role-tag">
              {{ roleText }}
            </el-tag>
          </div>
          <div class="summary-row">
            <span>登录入口</span>
            <strong>PORTAL</strong>
          </div>
        </div>
      </div>

      <div class="profile-card profile-card-white portal-hover">
        <div class="card-label">LIFE TRACKS</div>
        <div class="track-grid">
          <div class="track-item" @click="go('/portal/booking')">
            <div class="track-icon booking-icon"></div>
            <span>预约入口</span>
            <strong>BOOKING</strong>
            <p>快速进入座位预约页面，按时间段选位。</p>
          </div>
          <div class="track-item" @click="go('/portal/my-reservations')">
            <div class="track-icon checkin-icon"></div>
            <span>签到与取消</span>
            <strong>CHECK-IN</strong>
            <p>在我的预约中完成签到或取消操作。</p>
          </div>
          <div class="track-item" @click="go('/portal/feedback')">
            <div class="track-icon feedback-icon"></div>
            <span>意见反馈</span>
            <strong>FEEDBACK</strong>
            <p>向管理员提交建议、问题与留言。</p>
          </div>
          <div class="track-item" @click="go('/portal/notices')">
            <div class="track-icon notice-icon"></div>
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
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 0;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-hero {
  position: relative;
  overflow: hidden;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 24px;
  align-items: stretch;
  min-height: 400px;
  padding: 48px;
  background: var(--card-bg, #ffffff);
  border-radius: 24px;
  box-shadow: 0 12px 36px rgba(15, 23, 42, 0.04);
  border: 1px solid rgba(148, 163, 184, 0.1);
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
  color: #64748b;
  font-size: 14px;
  letter-spacing: 2px;
  font-weight: 700;
  margin-bottom: 8px;
}

.hero-copy {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-copy h1 {
  margin: 8px 0 16px;
  font-size: 54px;
  line-height: 1.05;
  letter-spacing: -0.5px;
  text-transform: uppercase;
  font-weight: 800;
  color: #0f172a;
  background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-copy p {
  max-width: 600px;
  color: #475569;
  line-height: 1.7;
  font-size: 16px;
  font-weight: 400;
  margin-bottom: 32px;
}

.hero-actions {
  display: flex;
  gap: 16px;
}

.primary-btn,
.outline-btn {
  height: 48px;
  border-radius: 12px !important;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
  padding: 0 28px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.primary-btn {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  border: none;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(37, 99, 235, 0.35);
  background: linear-gradient(135deg, #1d4ed8 0%, #4338ca 100%);
}

.outline-btn {
  background: transparent;
  color: #334155;
  border: 1px solid #cbd5e1;
}

.outline-btn:hover {
  background: #f8fafc;
  color: #0f172a;
  border-color: #94a3b8;
}

.hero-status {
  position: relative;
  z-index: 1;
  align-self: center;
  padding: 32px;
  border-radius: 20px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  background: #ffffff;
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06);
}

.status-band {
  height: 5px;
  border-radius: 3px;
  background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
  margin-bottom: 24px;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

.status-grid span,
.card-label,
.track-item span {
  font-size: 12px;
  color: #64748b;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  font-weight: 600;
}

.status-grid strong {
  display: block;
  margin-top: 6px;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.status-active {
  color: #10b981 !important;
}

.profile-bands {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 24px;
}

.profile-card {
  min-height: 360px;
  padding: 36px;
  border-radius: 24px;
  border: 1px solid rgba(148, 163, 184, 0.15);
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);
}

.profile-card-light {
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
}

.profile-card-white {
  background: #ffffff;
}

.card-label {
  margin-bottom: 28px;
  color: #475569;
}

.summary-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px dashed #cbd5e1;
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-row span {
  color: #64748b;
  font-size: 14px;
}

.summary-row strong {
  color: #0f172a;
  font-weight: 600;
  font-size: 15px;
}

.role-tag {
  font-weight: 600;
  letter-spacing: 1px;
}

.track-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.track-item {
  position: relative;
  padding: 24px;
  background: #f8fafc;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  overflow: hidden;
}

.track-item:hover {
  transform: translateY(-4px);
  background: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.06);
}

.track-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #e0e7ff 0%, #dbeafe 100%);
}

.booking-icon { background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); }
.checkin-icon { background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); }
.feedback-icon { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); }
.notice-icon { background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); }

.track-item strong {
  display: block;
  margin: 6px 0 10px;
  font-size: 22px;
  line-height: 1.2;
  font-weight: 700;
  color: #1e293b;
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

@media (max-width: 1024px) {
  .profile-hero {
    grid-template-columns: 1fr;
    padding: 32px;
  }

  .profile-bands {
    grid-template-columns: 1fr;
  }

  .hero-copy h1 {
    font-size: 42px;
  }
}

@media (max-width: 640px) {
  .hero-copy h1 {
    font-size: 32px;
  }

  .hero-actions {
    flex-direction: column;
  }

  .status-grid,
  .track-grid {
    grid-template-columns: 1fr;
  }
  
  .profile-card {
    padding: 24px;
  }
}
</style>
