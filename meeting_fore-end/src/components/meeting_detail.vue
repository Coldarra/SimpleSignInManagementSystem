<template>
  <div id="meeting_detail" class="margin10">
    <div v-loading="loading_meeting">
      <el-card shadow="hover">
        <div slot="header" class="clearfix">
          <span>{{meeting.name||"会议名称"}}</span>
          <el-button style="float: right; padding: 3px 0" type="text">{{"会议"+meeting.state||"会议状态未知"}}</el-button>
        </div>
        <el-row :gutter="20">
          <el-col :span="18">
            <div>会议时间: {{meeting.meeting_startdate||"待定"}} ~ {{meeting.meeting_finishdate||"待定"}}</div>
            <div>当前时间: {{timenow}}</div>
            <div>会议地点: {{meeting.venue||"待定"}}</div>
            <div>主办单位: {{meeting.organizer||"暂无"}}</div>
            <div>协办单位: {{meeting.co_organizer||"暂无"}}</div>
            <div>会议内容: {{meeting.content||"待定"}}</div>
            <div>参会成员: {{participants.unarrived.length+participants.arrived.length}} 人</div>
            <div v-if="longUrl">
              签到链接:
              <el-link type="primary" :href="longUrl" :underline="false" target="_blank">{{shortUrl||"二维码加载中"}}</el-link>
            </div>
            <!-- <div>{{meeting}}</div> -->
          </el-col>
          <el-col :span="6">
            <div class="block">
              <div id="qrcode"></div>
              <!-- <el-image :src="meeting.logo" class="pull-center" fit="contain" id="logo">
                <div slot="error" class="image-slot">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>-->
            </div>
          </el-col>
        </el-row>
      </el-card>
    </div>
    <br>
    <br>
    <div>
      <!-- <el-button plain :loading="loading_excel" @click="choiceExcel">{{"上传参会人员表"}}</el-button>
      <el-button plain @click="downloadExcelTemplate">下载参会人员模板</el-button>-->
      <input ref="excelinput" type="file" accept=".xls, .xlsx" style="display:none;" @change="getExcel">

      <el-card shadow="hover" v-loading="loading_excel">
        <div slot="header" class="clearfix">
          <span>
            参会成员
            <el-button @click="getParticipants" type="text">
              &nbsp;
              <i class="el-icon-refresh"></i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            </el-button>
            <small style="color:grey">
              自动刷新:
              <el-switch v-model="autoRefresh"></el-switch>
            </small>
            &nbsp;&nbsp;
          </span>
          <el-button-group class="pull-right">
            <!-- <el-button style="float: right; padding: 3px 3px" type="text">下载成员信息</el-button> -->
            <el-button style="float: right; padding: 3px 3px" type="text" @click="downloadExcelTemplate">下载模板</el-button>
            <el-button style="float: right; padding: 3px 3px" type="text" @click="choiceExcel">批量添加</el-button>
            <el-button style="float: right; padding: 3px 3px" type="text" @click="dialog_appendParticipant=true">添加成员</el-button>
          </el-button-group>
        </div>
        <div v-loading="loading_participants">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card shadow="hover">
                <div>
                  <el-badge
                    :value="participants.unarrived.length"
                    type="warning"
                    :hidden="participants.unarrived.length==0"
                  >未签到&nbsp;&nbsp;</el-badge>
                </div>
                <div>
                  <!-- {{participants.signup}} -->
                  <el-button
                    v-for="(item,id) in participants.unarrived"
                    :key="id"
                    type="text"
                    @click="openParticipantInfoDialog(item)"
                  >{{item.name}}</el-button>
                  <el-button v-show="participants.unarrived.length==0" type="text">无</el-button>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card shadow="hover">
                <div>
                  <el-badge
                    :value="participants.arrived.length"
                    type="primary"
                    :hidden="participants.unarrived.length==0"
                  >已签到&nbsp;&nbsp;</el-badge>
                </div>
                <div>
                  <!-- {{participants.arrived}} -->
                  <el-button
                    v-for="(item,id) in participants.arrived"
                    :key="id"
                    type="text"
                    @click="openParticipantInfoDialog(item)"
                  >{{item.name}}</el-button>
                  <el-button v-show="participants.arrived.length==0" type="text">无</el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-card>
      <br>

      <el-card shadow="hover">
        <div slot="header" class="clearfix">
          <span>成员信息</span>
          <el-button style="float: right; padding: 3px 3px" type="text" @click="downloadParticipantsInfo">下载</el-button>
        </div>
        <div>
          <el-table
            :data="participants.unarrived.concat(participants.arrived)"
            style="width: 100%"
            :row-class-name="tableRowClassName"
            v-loading="loading_participants"
            id="participantsInfo"
          >
            <el-table-column prop="name" label="姓名" sortable></el-table-column>
            <el-table-column prop="company" label="班级" sortable>
              <template slot-scope="scope">{{ scope.row.company || "无"}}</template>
            </el-table-column>
            <el-table-column prop="phonenumber" label="手机号" sortable></el-table-column>
            <el-table-column prop="arrivedate" label="签到时间" sortable>
              <template slot-scope="scope">{{ scope.row.arrivedate || "未签到"}}</template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>

    <el-dialog
      title="添加成员"
      :visible.sync="dialog_appendParticipant"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      v-loading="loading_appendParticipant"
      width="30%"
    >
      <el-form ref="participantForm" :model="participantForm" :rules="rules">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="participantForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phonenumber">
          <el-input v-model="participantForm.phonenumber" type="number" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialog_appendParticipant = false">取 消</el-button>
        <el-button type="primary" @click="appendParticipant">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="会议成员" :visible.sync="dialog_participantInfo" width="280px">
      <div>姓名: {{participantInfo.name}}</div>
      <div>班级: {{participantInfo.company || "无"}}</div>
      <div>手机号: {{participantInfo.phonenumber}}</div>
      <div>签到时间: {{participantInfo.arrivedate || "未签到"}}</div>
      <el-divider></el-divider>

      <div v-loading="loading_participantInfo">
        <el-button
          plain
          :loading="false"
          type="warning"
          v-if="participantInfo.arrivedate"
          @click="setParticipantArrived(participantInfo.phonenumber,'unarrived')"
        >设为未到</el-button>
        <el-button
          plain
          :loading="false"
          type="success"
          v-else
          @click="setParticipantArrived(participantInfo.phonenumber,'arrived')"
        >设为已到</el-button>
        <el-button
          plain
          :loading="false"
          @click="setParticipantArrived(participantInfo.phonenumber,'remove')"
          type="danger"
        >删除成员</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>
import XLSX from "xlsx";
import QRCode from "qrcodejs2";

export default {
  name: "name_detail",
  data() {
    return {
      autoRefresh: false,
      updateTime: new Date().getTime(),
      loading_meeting: false,
      loading_participants: false,
      loading_excel: false,
      dialog_participantInfo: false,
      loading_participantInfo: false,
      participantInfo: {
        name: "",
        phonenumber: "",
        arrivedate: ""
      },
      dialog_appendParticipant: false,
      loading_appendParticipant: false,
      participantForm: {
        name: "",
        company: "",
        phonenumber: ""
      },
      timenow: "",
      meeting_id: this.$route.params.meeting_id,
      meeting: {},
      participants: {
        arrived: [],
        unarrived: []
      },
      longUrl: "",
      shortUrl: "",
      rules: {
        name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
        phonenumber: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          { min: 11, message: "请输入11位手机号", trigger: "blur" },
          { max: 11, message: "请输入11位手机号", trigger: "blur" }
        ]
      },
      users: []
    };
  },
  computed: {},
  methods: {
    getMeetingInfo() {
      var that = this;
      function getMeetingState() {
        if (
          that.meeting.meeting_startdate == "" ||
          that.meeting.meeting_finishdate == ""
        )
          return "状态未知";
        var nowDate = new Date();
        var meeting_startDate = new Date(that.meeting.meeting_startdate);
        var meeting_finishDate = new Date(that.meeting.meeting_finishdate);
        if (that.meeting.meeting_startdate && that.meeting.meeting_finishdate) {
          if (meeting_startDate > nowDate) return "未开始";
          else if (meeting_finishDate > nowDate) return "进行中";
          else return "已结束";
        }
      }
      function getMeetingDate() {
        function conver(s) {
          return s < 10 ? "0" + s : s;
        }
        function dateToString(date) {
          return `${conver(date.getMonth() + 1)}-${conver(
            date.getDate()
          )} ${conver(date.getHours())}:${conver(date.getMinutes())}`;
        }

        if (
          that.meeting.meeting_startdate == "" ||
          that.meeting.meeting_finishdate == ""
        )
          return "";
        var meeting_startDate = new Date(that.meeting.meeting_startdate);
        var meeting_finishDate = new Date(that.meeting.meeting_finishdate);
        if (
          meeting_startDate.getDate() == meeting_finishDate.getDate() &&
          meeting_startDate.getMonth() == meeting_finishDate.getMonth()
        ) {
          return `${dateToString(meeting_startDate)}~${conver(
            meeting_finishDate.getHours()
          )}:${conver(meeting_finishDate.getMinutes())}`;
        } else
          return `${dateToString(meeting_startDate)} ~ ${dateToString(
            meeting_finishDate
          )}`;
      }

      this.loading_meeting = true;
      this.$ajax
        .post("/api/meeting/info", { meeting_id: this.meeting_id })
        .then(res => {
          this.loading_meeting = false;
          if (res.data.ret == "0") {
            this.meeting = res.data.data.meeting;
            this.meeting.state = getMeetingState();
            this.meeting.date = getMeetingDate();
            console.log(this.meeting);
            this.getShortUrl();
            document.title = "会议详情 - " + this.meeting.name;
          } else {
            // this.$message({
            //   message: "数据加载失败，请重试",
            //   type: "error"
            // });
          }
        });
    },
    getUsers() {
      this.$ajax.post("/api/user/all").then(res => {
        if (res.data.ret == "0") {
          this.users = res.data.data.users;
          // console.log(this.users);
          this.combineUserWithParticipants();
        } else {
        }
      });
    },
    combineUserWithParticipants() {
      var users = this.users;
      function getCpmpany(phonenumber) {
        var usersLength = users.length;
        for (var i = 0; i < usersLength; i++)
          if (users[i].phonenumber == phonenumber) return users[i].company;
        // return "无";
      }
      var arrivedLength = this.participants.arrived.length;
      var unarrivedLength = this.participants.unarrived.length;
      for (var i = 0; i < arrivedLength; i++)
        this.participants.arrived[i].company = getCpmpany(
          this.participants.arrived[i].phonenumber
        );
      for (var i = 0; i < unarrivedLength; i++)
        this.participants.unarrived[i].company = getCpmpany(
          this.participants.unarrived[i].phonenumber
        );
      console.log(this.participants);
    },
    getParticipants(loading = true) {
      // console.log("getParticipants()");
      this.loading_participants = loading;
      this.updateTime = new Date().getTime();
      this.$ajax
        .post("/api/meeting/participant", { meeting_id: this.meeting_id })
        .then(res => {
          this.loading_participants = false;
          if (res.data.ret == "0") {
            this.participants = res.data.data.participants;
          } else {
          }
        });
    },
    appendParticipant() {
      this.$refs["participantForm"].validate(valid => {
        if (valid) {
          this.loading_appendParticipant = true;
          this.updateTime = new Date().getTime();
          this.$ajax
            .post("/api/meeting/participant/append", {
              meeting_id: this.meeting_id,
              name: this.participantForm.name,
              phonenumber: this.participantForm.phonenumber
            })
            .then(res => {
              this.loading_appendParticipant = false;
              if (res.data.ret == "0") {
                this.$message({
                  message: "添加成功",
                  type: "success"
                });
                this.dialog_appendParticipant = false;
                this.participants = res.data.data.participants;
                this.participantForm = {};
              } else {
              }
            });
        } else {
          // console.log("error submit!!");
          return false;
        }
      });
      return;
    },
    refreshParticipants() {
      if (new Date().getTime() - this.updateTime > 7500 && this.autoRefresh) {
        // console.log(this.autoRefresh);
        // console.log(
        //   new Date().getTime(),
        //   this.updateTime,
        //   new Date().getTime() - this.updateTime
        // );
        this.updateTime = new Date().getTime();
        this.getParticipants(false);
      }
    },
    updateTimeNow() {
      var that = this;
      function conver(s) {
        return s < 10 ? "0" + s : s;
      }
      function getTimeNow() {
        that.refreshParticipants();
        var myDate = new Date();
        var year = myDate.getFullYear();
        var month = myDate.getMonth() + 1;
        var date = myDate.getDate();
        var h = myDate.getHours();
        var m = myDate.getMinutes();
        var s = myDate.getSeconds();
        that.timenow =
          year +
          "-" +
          conver(month) +
          "-" +
          conver(date) +
          " " +
          conver(h) +
          ":" +
          conver(m) +
          ":" +
          conver(s);
      }
      setInterval(getTimeNow, 1000);
    },
    choiceExcel() {
      this.$refs.excelinput.dispatchEvent(new MouseEvent("click"));
    },
    getExcel() {
      //获取到管理员上传的excel文件
      this.loading_excel = true;
      var fileObj = this.$refs.excelinput.files[0];
      var reader = new FileReader();
      reader.readAsBinaryString(fileObj);
      reader.onload = ev => {
        const data = ev.target.result;
        const workbook = XLSX.read(data, {
          type: "binary"
        });
        const wsname = workbook.SheetNames[0]; //取第一张表
        console.log(workbook.Sheets[wsname]);

        const ws = XLSX.utils.sheet_to_json(workbook.Sheets[wsname]); //生成json表格内容
        console.log(ws);
        this.$ajax
          .post("/api/meeting/participant/add", {
            meeting_id: this.meeting_id,
            participants: JSON.stringify(ws)
          })
          .then(res => {
            this.loading_excel = false;
            this.$refs.excelinput.value = "";
            if (res.data.ret == "0") {
              this.$message({
                message: "添加成功",
                type: "success"
              });
              this.participants = res.data.data.participants;
            } else {
            }
          });
      };
      reader.onerror = function(error) {
        console.log("Error: ", error);
      };
    },
    downloadExcelTemplate() {
      const workbook = {
          SheetNames: ["Sheet1"],
          Sheets: {
            Sheet1: {
              "!ref": "A1:B1", // 必须要有这个范围才能输出，否则导出的 excel 会是一个空表
              A1: { v: "姓名" },
              B1: { v: "手机号" }
            }
          }
        },
        filename =
          this.meeting.name + ".参会人员." + new Date().getTime() + ".xlsx";
      XLSX.writeFile(workbook, filename);
    },
    downloadParticipantsInfo() {
      const workbook = XLSX.utils.table_to_book(
          document.getElementById("participantsInfo")
        ),
        wopts = {
          bookType: "xlsx",
          bookSST: false,
          type: "binary"
        },
        wbout = XLSX.write(workbook, wopts),
        filename = this.meeting.name + ".参会人员统计" + ".xlsx";
      XLSX.writeFile(workbook, filename);
    },
    openParticipantAppendDialog() {
      this.dialog_appendParticipant = true;
    },
    openParticipantInfoDialog(participant) {
      // console.log(name, phonenumber, arrivedate);
      this.dialog_participantInfo = true;
      this.participantInfo = participant;
    },
    setParticipantArrived(phonenumber, type = "arrived") {
      this.loading_participantInfo = true;
      var url = "/api/meeting/participant/" + type;
      this.$ajax
        .post(url, {
          meeting_id: this.meeting_id,
          phonenumber: phonenumber
        })
        .then(res => {
          this.loading_participantInfo = false;
          if (res.data.ret == "0") {
            this.dialog_participantInfo = false;
            this.participants = res.data.data.participants;
          } else {
          }
        });
    },
    getShortUrl() {
      const baseUrl = "http://cdn.clodia.cn/index.html";
      this.longUrl = `${baseUrl}?id=${this.meeting_id}&name=${
        this.meeting.name
      }&venue=${this.meeting.venue}&date=${this.meeting.date}`;
      // console.log(url);
      // console.log(encodeURI(url));

      var ajax = new XMLHttpRequest();
      ajax.open("post", "https://dwz.cn/admin/v2/create", "true");
      ajax.setRequestHeader("Content-Type", "application/json");
      ajax.setRequestHeader("Token", "fc71aaaa8e36cb84283ef1392cfbeec5");
      ajax.send(
        JSON.stringify({
          Url: encodeURI(this.longUrl),
          TermOfValidity: "1-year"
        })
      );

      ajax.onreadystatechange = () => {
        if (ajax.readyState === 4 && ajax.status === 200) {
          // 获取缩短后的网址
          const res = JSON.parse(ajax.responseText);
          console.log(res);
          switch (res.Code) {
            case 0:
              this.shortUrl = res.ShortUrl;
              this.makeQRCode();
              break;
            case -7:
              var minute = res.ErrMsg.substr(49, 2).replace(" ", "");
              this.$message({
                message: `更新签到链接中，请在${minute}分钟后刷新重试`,
                type: "warning"
              });
              break;

            default:
              this.$message({
                message: `二维码获取失败(${res.ErrMsg})`,
                type: "warning"
              });
              break;
          }
        }
      };
    },
    makeQRCode() {
      const qrcode = new QRCode("qrcode", {
        width: 132,
        height: 132,
        text: this.shortUrl, // 二维码地址
        colorDark: "#000",
        colorLight: "#fff"
      });
    },

    tableRowClassName({ row, rowIndex }) {
      return "";
      // if (row.arrivedate) return "";
      // else return "warning-row";
    }
  },
  props: ["mid"],
  mounted() {
    if (this.mid) {
      // console.log(this.mid);
      this.meeting_id = this.mid;
    }
    this.getMeetingInfo();
    this.getParticipants();
    this.updateTimeNow();
    this.getUsers();
  },
  watch: {
    autoRefresh() {
      if (this.autoRefresh) {
        this.getParticipants();
      }
    },
    participants() {
      this.combineUserWithParticipants();
    }
  }
};
</script>
<style lang="scss">
#logo {
  height: 10rem;
  width: 100%;
}
.badge {
  margin-top: 10px;
  margin-right: 40px;
}
</style>
