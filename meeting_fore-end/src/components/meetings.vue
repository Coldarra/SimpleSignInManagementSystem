<template>
  <div id="meeting" class>
    <el-button type="primary" @click="openCreateMeetingDialog" plain circle icon="el-icon-plus"></el-button>
    <el-button type="success" @click="refreshMeetingService" plain circle icon="el-icon-refresh"></el-button>

    <el-dialog
      :title="dialog.type | dialogTitle"
      v-loading="dialog.loading"
      :visible.sync="dialog.visible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="70%"
    >
      <el-card shadow="never">
        <div slot="header" class="clearfix">
          <span>会议信息</span>
          <el-button style="float: right; padding: 3px 0" type="text"></el-button>
        </div>
        <el-form ref="meetingForm" :rules="rules" :model="meetingForm" label-width="80px">
          <el-row>
            <el-col :span="12">
              <el-form-item label="会议名称" prop="name">
                <el-input v-model="meetingForm.name"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="logo">
                <el-button plain :loading="logo.loading" @click="choiceLogo" style="width:100%">{{logo.name}}</el-button>
                <input
                  ref="logoinput"
                  type="file"
                  name="logo"
                  accept=".jpg, .jpeg, .png"
                  style="display:none;"
                  @change="getLogo"
                >
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="会议地点">
            <el-input v-model="meetingForm.venue"></el-input>
          </el-form-item>

          <el-row>
            <el-col :span="12">
              <el-form-item label="会议时间">
                <el-col :span="11">
                  <el-date-picker
                    type="datetime"
                    placeholder="会议开始时间"
                    v-model="meetingForm.meeting_startdate"
                    default-time="12:00:00"
                    style="width: 100%;"
                  ></el-date-picker>
                </el-col>
                <el-col :span="11" :offset="2">
                  <el-date-picker
                    type="datetime"
                    placeholder="会议结束时间"
                    v-model="meetingForm.meeting_finishdate"
                    default-time="12:00:00"
                    style="width: 100%;"
                  ></el-date-picker>
                </el-col>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="报名时间">
                <el-col :span="11">
                  <el-date-picker
                    type="datetime"
                    placeholder="报名开始时间"
                    v-model="meetingForm.signup_startdate"
                    default-time="12:00:00"
                    style="width: 100%;"
                  ></el-date-picker>
                </el-col>
                <el-col :span="11" :offset="2">
                  <el-date-picker
                    type="datetime"
                    placeholder="报名结束时间"
                    v-model="meetingForm.signup_finishdate"
                    default-time="12:00:00"
                    style="width: 100%;"
                  ></el-date-picker>
                </el-col>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <el-form-item label="主办单位">
                <el-input v-model="meetingForm.organizer"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="协办单位">
                <el-input v-model="meetingForm.co_organizer"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="会议内容">
            <el-input type="textarea" v-model="meetingForm.content"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button v-if="dialog.type=='create'" type="primary" @click="createMeetingService">确认</el-button>
            <el-button v-else type="primary" @click="updateMeetingService">更新</el-button>
            <el-button @click="closeDialog">取消</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-dialog>

    <div style="margin-top:2rem"></div>
    <el-card shadow="hover">
      <div v-loading="loading_meetings" class="meetings">
        <template>
          <el-table :data="meetingList" style="width: 100%" :row-class-name="tableRowClassName">
            <el-table-column prop="name" label="会议名称" width="250">
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top-start">
                  <p>创建时间: {{ scope.row.adddate }}</p>
                  <div slot="reference" class="name-wrapper">
                    <p>{{ scope.row.name }}</p>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column prop label="会议时间" width="200">
              <template slot-scope="scope">
                <p>
                  {{ scope.row.meeting_startdate || "Null" }}
                  <!-- <br>~ -->
                  <br>
                  {{ scope.row.meeting_finishdate || "Null" }}
                </p>
              </template>
            </el-table-column>
            <!-- <el-table-column prop label="报名时间" width="200">
              <template slot-scope="scope">
                <p>
                  {{ scope.row.signup_startdate || "Null" }}
                  <br>
                  {{ scope.row.signup_finishdate || "Null" }}
                </p>
              </template>
            </el-table-column> -->
            <el-table-column prop="venue" label="会议地点" width="200">
              <template slot-scope="scope">{{ scope.row.venue || "Null" }}</template>
            </el-table-column>
            <el-table-column prop label="承办单位" width="200">
              <template slot-scope="scope">
                <p class="organizer">
                  <b>{{ scope.row.organizer || "Null" }}</b>
                  <span class="co_organizer" v-if="scope.row.co_organizer">
                    <br>
                    {{ scope.row.co_organizer }}
                  </span>
                </p>
              </template>
            </el-table-column>
            <el-table-column prop label="报名人数" width="100">
              <template slot-scope="scope">
                <p>
                  已报名: {{ scope.row.participant.signup }}
                  <br>
                  已签到: {{ scope.row.participant.arrived }}
                </p>
              </template>
            </el-table-column>

            <el-table-column prop="state" label="会议状态" width="80">
              <template slot-scope="scope">
                <span v-if="scope.row.state=='未开始'" class="notstart">未开始</span>
                <span v-else-if="scope.row.state=='进行中'" class="started">进行中</span>
                <span v-else-if="scope.row.state=='已结束'" class="finished">已结束</span>
                <span v-else-if="scope.row.state=='未知'" class="unknown">未知</span>
              </template>
            </el-table-column>
            <el-table-column prop="setting" label="设置" width="300">
              <template slot-scope="scope">
                <span class="inline">
                  <el-button plain @click="openMeetingDetail(scope.row)" icon="el-icon-search"></el-button>
                  <el-button type="primary" @click="updateMeeting(scope.row)" plain icon="el-icon-edit"></el-button>
                  <el-button type="danger" @click="removeMeeting(scope.row)" plain icon="el-icon-delete"></el-button>
                </span>
              </template>
            </el-table-column>
          </el-table>
        </template>
      </div>
    </el-card>
    <!-- <el-backtop target=".page-component__scroll .el-scrollbar__wrap"></el-backtop> -->
  </div>
</template>


<script>
const defaultMeetingForm = Object.freeze({
  name: "",
  venue: "",
  logo: "",
  meeting_startdate: "",
  meeting_finishdate: "",
  signup_startdate: "",
  signup_finishdate: "",
  organizer: "",
  co_organizer: "",
  content: ""
});
export default {
  name: "meeting",
  filters: {
    dialogTitle: type => {
      return type == "create" ? "新建会议" : "修改会议";
    }
  },
  data() {
    return {
      loading_meetings: true,
      meetingForm: Object.assign({}, defaultMeetingForm),
      logo: {
        name: "点击上传",
        loading: false
      },
      rules: {
        name: [
          { required: true, message: "请输入会议名称", trigger: "blur" },
          { min: 3, message: "会议名称不少于三个字符", trigger: "blur" }
        ]
      },
      meetingList: [],
      dialog: {
        visible: false,
        type: "",
        loading: false,
        meeting_id: ""
      }
    };
  },
  computed: {},
  methods: {
    choiceLogo() {
      this.$refs.logoinput.dispatchEvent(new MouseEvent("click"));
    },
    getLogo() {
      var fileObj = this.$refs.logoinput.files[0];
      var reader = new FileReader();
      reader.readAsDataURL(fileObj);
      reader.onload = () => {
        // console.log("file 转 base64结果：" + reader.result);
        this.meetingForm.logo = reader.result;
        this.logo.name = fileObj.name;
        this.logo.loading = false;
      };
      reader.onerror = function(error) {
        console.log("Error: ", error);
        this.logo.loading = false;
      };
    },
    resetMeetingForm() {
      this.meetingForm = Object.assign({}, defaultMeetingForm);
    },
    openCreateMeetingDialog() {
      if (this.dialog.type != "create") this.resetMeetingForm();
      this.dialog.type = "create";
      this.dialog.visible = true;
    },
    openUpdateMeetingDialog(meeting) {
      this.dialog.type = "update";
      this.dialog.meeting_id = meeting.id;
      this.dialog.visible = true;
      this.meetingForm = Object.assign({}, meeting);
    },
    closeDialog() {
      // if (confirm("退出将不保存更改"))
      this.dialog.visible = false;
    },
    refreshMeetingService() {
      this.loading_meetings = true;
      this.$ajax.post("/api/meeting/all").then(res => {
        if (res.data.ret == "0") {
          this.meetingList = res.data.data.meetings;
          this.filterMeetings();
        }
        this.loading_meetings = false;
      });
    },
    createMeetingService() {
      console.log("createMeeting");
      this.dialog.loading = true;
      this.$ajax.post("/api/meeting/create", this.meetingForm).then(res => {
        this.dialog.loading = false;
        console.log(res.data);

        if (res.data.ret == "0") {
          this.$message({
            message: "会议创建成功",
            type: "success"
          });
          this.resetMeetingForm();
          this.appendToMeetingList(res.data.data.meeting);
          this.dialog.visible = false;
        } else {
        }
      });
    },
    updateMeetingService() {
      console.log("updateMeeting");
      this.dialog.loading = true;
      this.$ajax
        .post(
          "/api/meeting/update",
          Object.assign(this.meetingForm, {
            meeting_id: this.dialog.meeting_id
          })
        )
        .then(res => {
          if (res.data.ret == "0") {
            this.$message({
              message: "会议修改成功",
              type: "success"
            });
            this.resetMeetingForm();
            this.updateToMeetingList(res.data.data.meeting);
            this.dialog.visible = false;
          }
          this.dialog.loading = false;
        });
    },
    removeMeetingService(meeting_id) {
      this.loading_meetings = true;
      this.$ajax
        .post("/api/meeting/remove", { meeting_id: meeting_id })
        .then(res => {
          if (res.data.ret == "0") {
            this.$message({
              message: "会议删除成功",
              type: "success"
            });
            this.removeFromMeetingList(meeting_id);
          }
          this.loading_meetings = false;
        });
    },
    appendToMeetingList(meeting) {
      this.meetingList.push(meeting);
      this.filterMeetings();
    },
    removeFromMeetingList(meeting_id) {
      var index = -1;
      for (var i = 0; i < this.meetingList.length; i++)
        if (this.meetingList[i].id == meeting_id) {
          index = i;
          break;
        }
      if (index >= 0) this.meetingList.splice(index, 1);
      // this.filterMeetings();
    },
    updateToMeetingList(meeting) {
      this.removeFromMeetingList(meeting.id);
      this.appendToMeetingList(meeting);
    },
    filterMeetings() {
      function getMeetingState(meeting) {
        if (meeting.meeting_startdate == "" || meeting.meeting_finishdate == "")
          return "未知";
        var nowDate = new Date();
        var meeting_startDate = new Date(meeting.meeting_startdate);
        var meeting_finishDate = new Date(meeting.meeting_finishdate);
        if (meeting.meeting_startdate && meeting.meeting_finishdate) {
          if (meeting_startDate > nowDate) return "未开始";
          else if (meeting_finishDate > nowDate) return "进行中";
          else return "已结束";
        }
      }
      function sortMeeting(m1, m2) {
        return m1.adddate < m2.adddate ? 1 : -1;
      }
      this.meetingList.sort(sortMeeting);
      this.meetingList.forEach((meeting, index) => {
        // console.log(index, meeting);
        this.meetingList[index].link = "/meeting/" + meeting.id;
        this.meetingList[index].state = getMeetingState(meeting);
        // console.log(meeting, index);
      });
    },
    updateMeeting(meeting) {
      console.log("updateMeeting", meeting.id);
      this.openUpdateMeetingDialog(meeting);
    },
    removeMeeting(meeting) {
      console.log("removeMeeting", meeting.id);
      if (confirm("确认删除？删除后将无法恢复")) {
        this.removeMeetingService(meeting.id);
      } else {
      }
    },
    openMeetingDetail(meeting) {
      this.$router.push({ path: meeting.link });
    },

    tableRowClassName({ row, rowIndex }) {
      switch (row.state) {
        case "进行中":
          return "success-row";
        case "已结束":
          return "";
        case "未开始":
          return "primary-row";
        default:
          return "warning-row";
      }
    }
  },
  mounted() {
    this.refreshMeetingService();
  },
  watch: {}
};
</script>

<style lang="scss">
#meeting {
  margin-left: 5%;
  margin-right: 5%;
}
.meetings {
  min-height: 10rem;
}
.el-table {
  p {
    .organizer {
      color: black;
    }
    .co_organizer {
      color: gray;
    }
  }
  .notstart {
    color: #22498b;
  }
  .started {
    color: #228b49;
  }
  .finished {
    color: #000000;
  }
  .unknown {
    color: #8b3522;
  }
}

// .el-table p {
//   white-space: nowrap;
// }
</style>
