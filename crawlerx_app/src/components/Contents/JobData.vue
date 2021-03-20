<template>
  <b-container fluid>
    <b-row>
      <b-col cols="12" class="mt-5">
        <h5>
          <b>Job Id:</b>
          {{this.$route.params.jobId}}
        </h5>
        <b-button
          variant="outline-info"
          style="float: right; margin-top:-40px;"
          @click="getCurrentJobData"
        >
          <b-icon icon="arrow-repeat" font-scale="1"></b-icon>Refresh
        </b-button>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" class="mt-3">
        <b-table
          striped
          hover
          :bordered="bordered"
          :borderless="borderless"
          :head-variant="headVariant"
          :items="jobData"
        ></b-table>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" class="mt-3">
        <h5>
          <b>Crawled Data:</b>
        </h5>

        <div style=" position:absolute; top:0; right:10vh;">
          <b-button
            class="copybutton"
            variant="success"
            type="button"
            @click="doCopy"
          >Copy Selected Data only</b-button>
          <b-button
            class="copybutton"
            variant="danger"
            type="button"
            v-clipboard:copy="crawledData"
            v-clipboard:success="clipboardSuccessHandler"
            v-clipboard:error="clipboardErrorHandler"
          >Copy All</b-button>
        </div>

        <div class="window" style="min-height: 300px; max-height: 80vh; overflow-y: scroll;">
          <div v-if="loading" style=" text-align: center;  padding: 80px 0;">Loading...</div>
          <div v-else>
            <vue-json-pretty
              :path="path"
              :data="crawledDataJson"
              :show-double-quotes="showDoubleQuotes"
              :highlight-mouseover-node="highlightMouseoverNode"
              :highlight-selected-node="highlightSelectedNode"
              :show-length="showLength"
              :show-line="showLine"
              :select-on-click-node="selectOnClickNode"
              :collapsed-on-click-brackets="collapsedOnClickBrackets"
              :selectable-type="selectableType"
              :show-select-controller="showSelectController"
              :path-selectable="((path, data) => typeof data !== 'number')"
              @click="handleClick(...arguments, 'complexTree')"
            />
          </div>
        </div>

        <!-- <pre style="min-height: 300px; max-height: 60vh; overflow-y: scroll;"><code>{{ crawledData }}</code></pre> -->
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import VueJsonPretty from "vue-json-pretty";
import "vue-json-pretty/lib/styles.css";
import Vue from "vue";
export default {
  name: "JobData",
  components: {
    VueJsonPretty,
  },
  data() {
    return {
      borderless: false,
      headVariant: "dark",
      bordered: true,
      jobData: [],
      taskId: null,
      jobStatus: null,
      crawledData: null,
      crawledDataJson: null,
      path: "this.crawledDataJson[0][0]",
      selectableType: "multiple",
      showSelectController: true,
      showLength: true,
      showLine: true,
      showDoubleQuotes: true,
      highlightMouseoverNode: true,
      highlightSelectedNode: true,
      selectOnClickNode: true,
      collapsedOnClickBrackets: true,
      useCustomLinkFormatter: false,
      itemData: {},
      itemPath: "",
      copyData: "",
      loading: true,
    };
  },
  mounted() {
    this.getCurrentJobData();
  },

  methods: {
    getCurrentJobData: function () {
      this.$http
        .post(
          "http://localhost:8000/api/job",
          JSON.stringify({
            user_id: this.$USER_ID,
            unique_id: this.$route.params.jobId,
          }),
          { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
        )
        .then((response) => {
          var project = [];
          var objectTaskId = null;
          var objectTaskStatus = null;
          response.data.data.forEach(function (obj) {
            objectTaskId = obj.task_id;
            if (
              objectTaskId === undefined ||
              objectTaskId == null ||
              objectTaskId === ""
            ) {
              objectTaskId = "STILL_PROCESSING";
            }
            project.push({
              project_name: obj.project_name,
              job_name: obj.job_name,
              task_id: objectTaskId,
              URL: obj.url,
              crawler_type: obj.crawler_name,
              status: obj.status,
            });
            objectTaskStatus = obj.status;
          });
          this.taskId = objectTaskId;
          this.jobStatus = objectTaskStatus;

          if (this.taskId !== null && this.jobStatus === "COMPLETED") {
            this.$http
              .post(
                "http://localhost:8000/api/job/crawldata",
                JSON.stringify({
                  user_id: this.$USER_ID,
                  unique_id: this.$route.params.jobId,
                  task_id: this.taskId,
                }),
                {
                  headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                  },
                }
              )
              .then((response) => {
                this.crawledData = JSON.stringify(
                  { data: response.data.data[0].data },
                  undefined,
                  4
                );
                this.loading = false;
                this.crawledDataJson = response.data.data[0].data;
              })
              .catch((e) => {
                alert(e.getError().toString());
              });
          }

          this.jobData = project;
        })
        .catch((e) => {
          alert(e.getError().toString());
        });
    },
    containsKey(obj, key) {
      return Object.keys(obj).includes(key);
    },

    handleClick(path, data, treeName = "") {
      this.itemPath = path;
      if (this.containsKey(this.itemData, path)) {
        Vue.delete(this.itemData, this.itemPath);
      } else {
        Vue.set(this.itemData, path, data);
      }
    },

    clipboardSuccessHandler() {
      this.$bvToast.toast("Copied To Clipboard ✓", {
        title: "Successful",
        toaster: "b-toaster-top-right",
        solid: true,
        variant: "success",
        appendToast: false,
        autoHideDelay: 5000,
      });
    },

    clipboardErrorHandler() {
      this.$bvToast.toast("Unable To Copy ✘", {
        title: "Error",
        toaster: "b-toaster-top-right",
        solid: true,
        variant: "danger",
        appendToast: false,
        autoHideDelay: 5000,
      });
    },
    doCopy: function () {
      for (var key in this.itemData) {
        this.copyData = this.copyData + this.itemData[key];
      }
      this.$copyText(this.copyData)
        .then(() => {
          this.clipboardSuccessHandler();
          this.copyData = "";
        })
        .catch(() => {
          this.clipboardErrorHandler();
          this.copyData = "";
        });
    },
  },
};
</script>

<style>
pre {
  width: 100%;
  padding: 0;
  margin: 0;
  overflow: auto;
  overflow-y: hidden;
  font-size: 12px;
  line-height: 20px;
  background: #efefef;
  border: 1px solid #777;
}
pre code {
  padding: 10px;
  color: #333;
}

.window {
  background: #272822;
  color: rgb(247, 247, 247);
  margin: auto;
  margin-top: 5vh;
  margin-bottom: 5vh;
  border: 1px solid #acacac;
  border-radius: 6px;
  box-shadow: 0px 0px 20px #acacac;
}

.vjs-tree .vjs-value__string {
  color: rgb(213, 248, 58);
}

.vjs-tree.has-selectable-control.is-selectable.is-mouseover {
  background: #0e922a;
  cursor: pointer;
}
.copybutton {
  margin-left: 1rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>