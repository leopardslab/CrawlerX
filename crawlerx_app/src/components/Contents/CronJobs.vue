<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <b-container fluid>
        <b-row>
            <b-col cols="12" class="mt-5">
                <h5>Crawled Cron Job Details:</h5>
                <b-button variant="outline-info" style="float: right; margin-top:-40px;"
                          @click="getCrawledIntervalJobDataProjectWise">
                    <b-icon icon="arrow-repeat" font-scale="1"></b-icon>
                    Refresh
                </b-button>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="12" class="mt-3">
                <b-table id="cron-job-table" striped hover size="sm" :per-page="perPage"
                         :current-page="currentPage" :fields="fields" :bordered="bordered" :borderless="borderLess"
                         :head-variant="headVariant" :items="projectsWiseJobs">
                    <template v-slot:cell(url)="data">
                        <b-link :href="data.value" target="_blank">{{data.value}}</b-link>
                    </template>
                    <template #cell(status)="row">
                        <center>
                            <b-icon v-if="row.value == 'COMPLETED'" icon="check-circle-fill" style="color:green;"></b-icon>
                            <b-icon v-if="row.value == 'RUNNING'" icon="arrow-repeat" style="color:orange;"></b-icon>
                            <b-icon v-if="row.value == 'FAILED'" icon="exclamation-circle-fill" style="color:red;"></b-icon>
                            <b-icon v-if="row.value == 'DISABLED'" icon="exclamation-circle-fill" style="color:dodgerblue;"></b-icon>
                            <b-icon v-if="row.value == 'PENDING'" icon="circle-fill" style="color:goldenrod;"></b-icon>
                            {{row.value}}
                        </center>
                    </template>
                    <template #cell(allow)="row">
                        <center>
                            <b-button size="sm" variant="outline-warning" class="mb-2"
                                      @click="changeSchedulerState(row.value)">
                                {{ (row.value.includes("DISABLED")) ? "Enable" : "Disable"}}
                            </b-button>
                        </center>
                    </template>
                    <template #cell(action)="row">
                        <center>
                            <b-button size="sm" variant="outline-danger" class="mb-2" @click="showModal(row.value)">
                                Delete
                                <b-icon icon="x-circle" aria-hidden="true"></b-icon>
                            </b-button>
                        </center>
                    </template>
                </b-table>
                <b-modal ref="myModalRefJob" centered title="Delete Crawl Job" @ok="deleteCrawlJob"
                         @cancel="hideModal">
                    <p class="my-4">Are you sure you want to delete <b>{{deletingJobId}}</b> job?</p>
                </b-modal>
                <b-pagination
                        size="sm"
                        align="right"
                        v-model="currentPage"
                        :total-rows="rows"
                        :per-page="perPage"
                        aria-controls="cron-job-table"
                ></b-pagination>

                <h6>Cron Schedule Jobs</h6>
                <b-row>
                    <b-col md="4" class="my-2">
                        <b-form-group
                                label="Sort"
                                label-for="sort-by-select"
                                label-cols-sm="1"
                                label-align-sm="right"
                                label-size="sm"
                                class="mb-0"
                        >
                            <b-input-group size="sm">
                                <b-form-select
                                        id="sort-by-select"
                                        v-model="sortBy"
                                        :options="sortOptions"
                                        class="w-75"
                                >
                                    <template #first>
                                        <option value="">-- none --</option>
                                    </template>
                                </b-form-select>

                                <b-form-select
                                        v-model="sortDesc"
                                        :disabled="!sortBy"
                                        size="sm"
                                        class="w-25"
                                >
                                    <option :value="false">Asc</option>
                                    <option :value="true">Desc</option>
                                </b-form-select>
                            </b-input-group>
                        </b-form-group>
                    </b-col>
                    <b-col md="4"/>
                    <b-col md="4" class="my-2">
                        <b-form-group
                                label="Filter"
                                label-for="filter-input"
                                label-cols-sm="3"
                                label-align-sm="right"
                                label-size="sm"
                                class="mb-0"
                        >
                            <b-input-group size="sm">
                                <b-form-input
                                        id="filter-input"
                                        v-model="filter"
                                        type="search"
                                        placeholder="Type to Filter"
                                ></b-form-input>
                                <b-input-group-append>
                                    <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                                </b-input-group-append>
                            </b-input-group>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-table id="cron-job-table-data" striped hover size="sm" :per-page="perDataPage"
                         :current-page="currentDataPage" :fields="jobDataFields" :bordered="bordered"
                         :borderless="borderLess"
                         :filter="filter"
                         :sort-by.sync="sortBy"
                         :sort-desc.sync="sortDesc"
                         :sort-direction="sortDirection"
                         :head-variant="headVariant" :items="projectsWiseSchedulerJobs">
                    <template v-slot:cell(task_id)="data">
                        <router-link :to="'/dashboard/schedule-job/' + data.value">{{data.value}}</router-link>
                    </template>
                    <template #cell(status)="row">
                        <center>
                            <b-icon v-if="row.value == 'COMPLETED'" icon="check-circle-fill" style="color:green;"></b-icon>
                            <b-icon v-if="row.value == 'RUNNING'" icon="arrow-repeat" style="color:orange;"></b-icon>
                            <b-icon v-if="row.value == 'FAILED'" icon="exclamation-circle-fill" style="color:red;"></b-icon>
                            <b-icon v-if="row.value == 'DISABLED'" icon="exclamation-circle-fill" style="color:dodgerblue;"></b-icon>
                            <b-icon v-if="row.value == 'PENDING'" icon="circle-fill" style="color:goldenrod;"></b-icon>
                            {{row.value}}
                        </center>
                    </template>
                    <template #cell(action)="row">
                        <center>
                            <b-button size="sm" variant="outline-danger" class="mb-2" @click="showModalTaskDelete(row.value)">
                                Delete
                                <b-icon icon="x-circle" aria-hidden="true"></b-icon>
                            </b-button>
                        </center>
                    </template>
                </b-table>
                <b-modal ref="myModalRefTask" centered title="Delete Crawl Job" @ok="deleteCrawlTask"
                         @cancel="hideModalTask">
                    <p class="my-4">Are you sure you want to delete <b>{{deletingTaskId}}</b> task?</p>
                </b-modal>
                <b-pagination
                        size="sm"
                        align="right"
                        v-model="currentDataPage"
                        :total-rows="jobDataRows"
                        :per-page="perDataPage"
                        aria-controls="cron-job-table-data"
                ></b-pagination>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
  import {EventBus} from '../../router/bus';

  export default {
    name: 'IntervalJobsPage',
    data() {
      return {
        sortDesc: false,
        sortDirection: 'desc',
        sortBy: '',
        filter: null,
        filterOn: [],
        deletingJobId: "",
        deletingTaskId: "",
        perPage: 4,
        currentPage: 1,
        perDataPage: 7,
        currentDataPage: 1,
        isDeleteButtonHidden: false,
        borderLess: false,
        headVariant: 'dark',
        bordered: true,
        projectsWiseJobs: [],
        projectsWiseSchedulerJobs: [],
        fields: [
          {key: 'project_name', label: 'Project Name'},
          {key: 'job_name', label: 'Job Name'},
          {key: 'url', label: 'URL'},
          {key: 'crawler_type', label: 'Crawler Type'},
          {key: 'status', label: 'Status'},
          {key: 'allow', label: 'Enable/Disable'},
          {key: 'action', label: 'Remove'},
        ],
        jobDataFields: [
          {key: 'project_name', label: 'Project Name'},
          {key: 'job_name', label: 'Job Name'},
          {key: 'task_id', label: 'Task ID'},
          {key: 'schedule_time', label: 'Scheduled At', sortable: true, sortDirection: 'desc'},
          {key: 'crawler_type', label: 'Crawler Type'},
          {key: 'status', label: 'Status'},
          {key: 'action', label: 'Remove'},
        ],
      }
    }, created() {
      EventBus.$on('project_created', data => {
        this.getCrawledIntervalJobDataProjectWise();
      });

      EventBus.$on('job_created', data => {
        this.getCrawledIntervalJobDataProjectWise();
      });
    }, computed: {
      sortOptions() {
        return this.jobDataFields
          .filter(f => f.sortable)
          .map(f => {
            return { text: f.label, value: f.key }
          })
      },
      rows() {
        return this.projectsWiseJobs.length
      },
      jobDataRows() {
        return this.projectsWiseSchedulerJobs.length
      }
    }, mounted() {
      this.getCrawledIntervalJobDataProjectWise();
    }, methods: {
      showModal(id) {
        this.deletingJobId = id;
        this.$refs.myModalRefJob.show()
      },
      hideModal () {
        this.$root.$emit('bv::hide::modal','myModalRefJob');
        this.$refs.myModalRefJob.hide()
      },
      showModalTaskDelete(id) {
        this.deletingTaskId = id;
        this.$refs.myModalRefTask.show()
      },
      hideModalTask () {
        this.$root.$emit('bv::hide::modal','myModalRefTask');
        this.$refs.myModalRefTask.hide()
      },
      deleteCrawlJob: function () {
        this.$http.delete(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/crawl/delete_job/' + this.deletingJobId,
          {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
          .then(response => {
            this.$bvToast.toast(response.data['Message'], {
              title: 'Crawl Job Deletion',
              toaster: 'b-toaster-top-right',
              solid: true,
              variant: 'success',
              appendToast: false
            });
            this.getCrawledIntervalJobDataProjectWise();
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
      },
      deleteCrawlTask: function () {
        this.$http.delete(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/crawl/delete_task/' + this.deletingTaskId,
          {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
          .then(response => {
            this.$bvToast.toast(response.data['Message'], {
              title: 'Crawl Job Deletion',
              toaster: 'b-toaster-top-right',
              solid: true,
              variant: 'success',
              appendToast: false
            });
            this.getCrawledIntervalJobDataProjectWise();
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
      },
      changeSchedulerState: function (celeryTaskName) {
        var spilter = celeryTaskName.split('@');
        let schedulerName = spilter[0];
        let schedulerState = spilter[1];
        if (schedulerState === "DISABLED") {
          schedulerState = true;
        } else {
          schedulerState = false;
        }
        this.$http.post(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/crawl/disable_job',
          JSON.stringify({'celery_task_name': schedulerName, 'is_enabled': schedulerState}),
          {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
          .then(response => {
            this.$bvToast.toast(response.data['Message'], {
              title: 'Crawl Scheduler State',
              toaster: 'b-toaster-top-right',
              solid: true,
              variant: 'success',
              appendToast: false
            });

            let updatedProjectsWiseJobs = [];
            this.projectsWiseJobs.forEach(function (item) {
              if (item.celery_task_name === celeryTaskName) {
                item['celery_task_name'] = schedulerName + '@' + schedulerState.toString();
              }
              updatedProjectsWiseJobs.push(item);
            });
            this.projectsWiseJobs = updatedProjectsWiseJobs;
            this.getCrawledIntervalJobDataProjectWise();
          })
          .catch(e => {
            this.$bvToast.toast(e.response.data['Error'], {
              title: 'Crawl Scheduler State',
              toaster: 'b-toaster-top-right',
              solid: true,
              variant: 'danger',
              appendToast: false
            });
          });
      },
      getCrawledIntervalJobDataProjectWise: function () {
        let projectDrillDown = [];
        let projectDrillDownData = [];
        this.$http.post(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/jobs',
          JSON.stringify({'user_id': this.$USER_ID, 'schedule_category': 'Cron'}),
          {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
          .then(response => {
            response.data.data.forEach(function (obj) {
              if (obj["schedule_time"] === undefined) {
                projectDrillDown.push({
                  project_name: obj.project_name, job_name: obj.job_name, action: obj.unique_id,
                  job_id: obj.unique_id, url: obj.url, allow: obj.celery_task_name + "@" + obj.status,
                  crawler_type: obj.crawler_name, status: obj.status
                });
              } else {
                projectDrillDownData.push({
                  project_name: obj.project_name, job_name: obj.job_name, action: obj.task_id,
                  job_id: obj.unique_id, task_id: obj.task_id, schedule_time: new Date(1000 * obj.schedule_time).toLocaleString(),
                  crawler_type: obj.crawler_name, status: obj.status,
                });
              }
            });

            if (projectDrillDown.length === 0) {
              projectDrillDown.push({
                project_name: "-", job_name: "-", job_id: "-", crawler_type: "-",
                url: "-", status: "-", allow: "-", action: "-"
              });
            }

            if (projectDrillDownData.length === 0) {
              projectDrillDownData.push({
                project_name: "-", job_name: "-", job_id: "-", crawler_type: "-",
                task_id: "-", status: "-", allow: "-", action: "-", schedule_time: "-"
              });
            }

            this.projectsWiseJobs = projectDrillDown;
            this.projectsWiseSchedulerJobs = projectDrillDownData;
          }).catch(e => {
          this.$bvToast.toast(e.response.data['Error'], {
            title: 'Crawl Schedule Job Data',
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