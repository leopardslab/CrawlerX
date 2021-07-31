<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <b-container fluid>
        <b-row>
            <b-col cols="12" class="mt-4">
                <b-card-group deck>
                    <b-card bg-variant="secondary" text-variant="white" header="Projects Count" class="text-center">
                        <b-card-text style="font-size:35px;">{{projectCount}}</b-card-text>
                    </b-card>

                    <b-card bg-variant="warning" text-variant="white" header="Running Job Count" class="text-center">
                        <b-card-text style="font-size:35px;">{{pendingJobCount}}</b-card-text>
                    </b-card>

                    <b-card bg-variant="success" text-variant="white" header="Completed Job Count" class="text-center">
                        <b-card-text style="font-size:35px;">{{completedJobCount}}</b-card-text>
                    </b-card>

                    <b-card bg-variant="danger" text-variant="white" header="Failed Job Count" class="text-center">
                        <b-card-text style="font-size:35px;">{{failedJobCount}}</b-card-text>
                    </b-card>
                </b-card-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="12" class="mt-5">
                <h6>Crawling Job Details:</h6>
                <b-button variant="outline-info" style="float: right; margin-top:-40px;" @click="getCrawledJobData">
                    <b-icon icon="arrow-repeat" font-scale="1"></b-icon>
                    Refresh
                </b-button>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="12" class="mt-3">
                <b-table id="job-table" striped hover size="sm" :per-page="perPage" :current-page="currentPage"
                         :fields="fields" :bordered="bordered" :borderless="borderLess" :head-variant="headVariant"
                         :items="jobItems">
                    <template v-slot:cell(job_id)="data">
                        <router-link :to="'/dashboard/job/' + data.value">{{data.value}}</router-link>
                    </template>
                    <template #cell(action)="row">
                        <center>
                            <b-button v-if="!isDeleteButtonHidden" size="sm" variant="outline-danger" class="mb-2"
                                      @click="showModal(row.value)">
                                Delete
                                <b-icon icon="x-circle" aria-hidden="true"></b-icon>
                            </b-button>
                        </center>
                        <b-modal ref="myModalRef" centered title="Delete Crawl Job" @ok="deleteCrawlJob"
                                 @cancel="hideModal">
                            <p class="my-4">Are you sure you want to delete <b>{{deletingJobId}}</b> job?</p>
                        </b-modal>
                    </template>
                </b-table>
                <b-pagination
                        size="sm"
                        align="right"
                        v-model="currentPage"
                        :total-rows="rows"
                        :per-page="perPage"
                        aria-controls="job-table"
                ></b-pagination>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
  import {EventBus} from '../../router/bus';

  export default {
    name: 'DashboardPage',
    data() {
      return {
        deletingJobId: "",
        isDeleteButtonHidden: false,
        showDeletePopup: false,
        borderLess: false,
        headVariant: 'dark',
        bordered: true,
        jobItems: [],
        projectCount: 0,
        completedJobCount: 0,
        pendingJobCount: 0,
        failedJobCount: 0,
        projects: [],
        fields: [
          {key: 'project_name', label: 'Project Name'},
          {key: 'job_name', label: 'Job Name'},
          {key: 'job_id', label: 'Job ID'},
          {key: 'crawler_type', label: 'Crawler Type'},
          {key: 'scheduler', label: 'Scheduler'},
          {key: 'status', label: 'Status'},
          {key: 'action', label: 'Action'},
        ],
        perPage: 8,
        currentPage: 1,
      }
    },
    computed: {
      rows() {
        return this.jobItems.length
      }
    }, created() {
      EventBus.$on('project_created', data => {
        this.getProjectData();
      });

      EventBus.$on('job_created', data => {
        this.getCrawledJobData();
      });
    }, mounted() {
      this.getProjectData();
      this.getCrawledJobData();
    }, methods: {
      showModal(id) {
        this.deletingJobId = id;
        this.$refs.myModalRef.show()
      },
      hideModal() {
        this.$root.$emit('bv::hide::modal', 'myModalRef');
        this.$refs.myModalRef.hide()
      },
      getCrawledJobData: function () {
        this.$http.post('http://localhost:8000/api/jobs',
          JSON.stringify({'user_id': this.$USER_ID}),
          {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
          .then(response => {
            let job_items = [];
            let completedJobCount = 0;
            let pendingJobCount = 0;
            let failedJobCount = 0;
            response.data.data.forEach(function (obj) {
              if (obj['schedule_time'] === undefined || obj['schedule_category'] === "Instant") {
                job_items.push({
                  project_name: obj.project_name,
                  job_name: obj.job_name,
                  job_id: obj.unique_id,
                  crawler_type: obj.crawler_name,
                  scheduler: obj.schedule_category,
                  status: obj.status,
                  action: obj.unique_id
                });
                if (obj.status === "COMPLETED") {
                  completedJobCount += 1;
                } else if (obj.status === "PENDING" || obj.status === "RUNNING") {
                  pendingJobCount += 1;
                } else if (obj.status === "FAILED") {
                  failedJobCount += 1;
                }
              }
            });

            if (response.data.data.length === 0) {
              this.isDeleteButtonHidden = true;
              job_items.push({
                project_name: "-", job_name: "-", job_id: "-",
                crawler_type: "-", scheduler: "-", status: "-", action: "-"
              });
            } else {
              this.isDeleteButtonHidden = false;
            }

            this.completedJobCount = completedJobCount;
            this.pendingJobCount = pendingJobCount;
            this.failedJobCount = failedJobCount;
            this.jobItems = job_items;
          })
          .catch(e => {
            alert(e.getError().toString())
          });
      },
      getProjectData: function () {
        this.$http.post('http://localhost:8000/api/projects',
          JSON.stringify({'user_id': this.$USER_ID}),
          {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
          .then(response => {
            var projects = [];
            response.data.data.forEach(function (obj) {
              projects.push({project_name: obj.project_name})
            });
            this.projects = projects;
            this.projectCount = this.projects.length;
            this.emitGlobalProjectData();
          })
          .catch(e => {
            alert(e.getError().toString())
          });
      },
      emitGlobalProjectData() {
        EventBus.$emit('project_data', this.projects);
      },
      deleteCrawlJob: function () {
        this.$http.delete('http://localhost:8000/api/crawl/delete_job/' + this.deletingJobId,
          {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
          .then(response => {
            this.$bvToast.toast(response.data['Message'], {
              title: 'Crawl Job Deletion',
              toaster: 'b-toaster-top-right',
              solid: true,
              variant: 'success',
              appendToast: false
            });
            this.getCrawledJobData();
          })
          .catch(e => {
            this.$bvToast.toast(e.response.data['Error'], {
              title: 'Crawl Job Deletion',
              toaster: 'b-toaster-top-right',
              solid: true,
              variant: 'danger',
              appendToast: false
            });
          });
      }
    }
  }
</script>

<style lang="scss">
    .page-item.active .page-link {
        background-color: #343a40 !important;
        border-color: #343a40 !important;
        color: white !important;
    }

    .page-item .page-link {
        color: #343a40 !important;
    }
</style>