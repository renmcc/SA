<template>
  <el-card style="margin-bottom:20px;">
    <div slot="header" class="clearfix">
      <span>个人资料</span>
    </div>

    <div class="user-profile">
      <div class="box-center">
        <pan-thumb :image="avatar" :height="'100px'" :width="'100px'" :hoverable="true" />
      </div>
      <div class="box-center">
        <div class="user-name text-center">{{ name }}</div>
        <div class="user-role text-center text-muted">{{ roles.join(' | ') | uppercaseFirst }}</div>
      </div>
    </div>

    <div class="user-bio ">
      <div class="user-education user-bio-section">
        <div class="user-bio-section-header "><i class="el-icon-postcard" /><span>登录账号</span><span class="right">{{ username }}</span></div>
        <div class="user-bio-section-header"><i class="el-icon-message" /><span>邮箱</span><span class="right">{{ email }}</span></div>
        <div class="user-bio-section-header"><i class="el-icon-mobile-phone" /><span>手机号</span><span class="right">{{ mobile }}</span></div>
        <div class="user-bio-section-header"><i class="el-icon-s-custom" /><span>职位</span><span class="right">{{ position }}</span></div>
        <div class="user-bio-section-header"><i class="el-icon-lock" /><span>账号状态</span><span class="right">{{ is_active ? "正常" : "禁用" }}</span></div>
        <div class="user-bio-section-header"><i class="el-icon-timer" /><span>创建时间</span><span class="right">{{ date_joined }}</span></div>
      </div>
    </div>
  </el-card>
</template>

<script>
import PanThumb from '@/components/PanThumb'
import { mapGetters } from 'vuex'

export default {
  name: 'UserCard',
  components: { PanThumb },
  data() {
    return {}
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles',
      'username',
      'mobile',
      'position',
      'date_joined',
      'is_active',
      'email'
    ])
  }
}
</script>

<style lang="scss" scoped>
.box-center {
  margin: 0 auto;
  display: table;
}

.text-muted {
  color: #777;
}

.user-profile {
  .user-name {
    font-weight: bold;
  }

  .box-center {
    padding-top: 10px;
  }

  .user-role {
    padding-top: 10px;
    font-weight: 400;
    font-size: 14px;
  }

  .box-social {
    padding-top: 30px;

    .el-table {
      border-top: 1px solid #dfe6ec;
    }
  }

  .user-follow {
    padding-top: 20px;
  }
}

.user-bio {
  margin-top: 20px;
  color: #606266;

  span {
    padding-left: 4px;
  }

  .user-bio-section {
    font-size: 14px;
    padding: 15px 0;

    .user-bio-section-header {
      border-bottom: 1px solid #dfe6ec;
      padding-bottom: 10px;
      margin-bottom: 10px;
      /*font-weight: bold;*/
    }
  }

  /*左对齐*/
  .left {
    float: left;
  }
  /*右对齐*/
  .right {
    float: right;
  }
}
</style>
