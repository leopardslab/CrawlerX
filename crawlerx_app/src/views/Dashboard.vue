<template>
    <div
            id="demo"
            :class="[{'collapsed' : collapsed}, {'onmobile' : isOnMobile}]"
    >
        <div class="">
            <md-toolbar md-get-palette-color="red" md-elevation="1">
                <h3 class="md-title" style="flex: 1"><b>CrawlerX</b> - Open-Source Crawling Platform</h3>
                <b-button v-b-modal.modal-new-project variant="outline-secondary">Create a Project</b-button>
                <b-button v-b-modal.modal-new-job variant="outline-secondary" class="ml-2">Schedule a Job</b-button>
                <b-button variant="primary" class="ml-2" @click="logout">Logout</b-button>
            </md-toolbar>
            <sidebar-menu
                    :menu="menu"
                    :collapsed="collapsed"
                    :theme="selectedTheme"
                    :show-one-child="true"
                    @toggle-collapse="onToggleCollapse"
                    @item-click="onItemClick"
            />
            <router-view/>
            <div
                    v-if="isOnMobile && !collapsed"
                    class="sidebar-overlay"
                    @click="collapsed = true"></div>
        </div>

        <b-modal id="modal-new-project" ref="modal" size="lg" title="Create a new project"
                 @show="resetProjectCreateModal" @hidden="resetProjectCreateModal" @ok="handleProjectCreateOk">
            <b-form ref="form" v-on:submit.prevent="createProject">
                <b-form-group
                        :state="projectNameState"
                        label="Project Name:"
                        label-for="name-input"
                        invalid-feedback="Name is required"
                >
                    <b-form-input
                            id="name-input"
                            v-model="projectForm.projectName"
                            :state="projectNameState"
                            required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                        label="Project Description:"
                        label-for="description-input"
                >
                    <b-form-textarea
                            id="description"
                            v-model="projectForm.description"
                            placeholder="About the project..."
                            rows="3"
                            max-rows="6"
                    ></b-form-textarea>
                </b-form-group>
            </b-form>
        </b-modal>

        <b-modal id="modal-new-job" size="lg" title="Create a new crawl job"
                 @show="resetJobCreateModal" @hidden="resetJobCreateModal" @ok="handleJobCreateOk">
            <form ref="form" @submit.stop.prevent="createJob">
                <b-form-group
                        :state="jobNameState"
                        label="Job Name:"
                        label-for="name-input"
                        invalid-feedback="Name is required"
                >
                    <b-form-input
                            id="name-input"
                            v-model="jobForm.jobName"
                            :state="jobNameState"
                            required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                        label="Project:"
                        label-for="project-input"
                >
                    <b-form-select v-model="jobForm.projectName" :options="projectOptions"/>
                </b-form-group>
                <b-form-group
                        label="Crawling Type:"
                        label-for="crawl-type-input"
                >
                    <b-form-select v-model="jobForm.crawler" :options="crawlerOptions"/>
                </b-form-group>
                <b-form-group>
                    <b-card no-body>
                        <b-tabs card>
                            <b-tab title="Enter URLs" active>
                                <b-form-group
                                        label="URLs:"
                                        :state="urlsState"
                                        label-for="url-input"
                                        invalid-feedback="Enter multiple HTTP or HTTPS valid URLs "
                                >
                                    <b-form-tags
                                            input-id="url-tags"
                                            :input-attrs="{ 'aria-describedby': 'tags-remove-on-delete-help' }"
                                            v-model="jobForm.urlValue"
                                            separator=" "
                                            placeholder="Enter new urls separated by space"
                                            remove-on-delete
                                            no-add-on-enter
                                            :state="urlsState"
                                            class="mb-2"
                                    ></b-form-tags>
                                    <b-form-text id="tags-remove-on-delete-help">
                                        Press <kbd>Backspace</kbd> to remove the last url entered
                                    </b-form-text>
                                </b-form-group>
                            </b-tab>
                            <b-tab title="Bulk Import URLs">
                                <b-form-group
                                        label="Load URLs from a File:"
                                        label-for="file-input"
                                >
                                    <b-form-tags
                                            input-id="url-tags"
                                            :input-attrs="{ 'aria-describedby': 'tags-remove-on-delete-help' }"
                                            v-model="jobForm.urlValue"
                                            separator=" "
                                            placeholder="Enter new urls separated by space"
                                            remove-on-delete
                                            no-add-on-enter
                                            :state="urlsState"
                                            class="mb-2"
                                    ></b-form-tags>
                                    <input type="file" @change="loadTextFromFile">
                                </b-form-group>
                            </b-tab>
                        </b-tabs>
                    </b-card>
                </b-form-group>
                <hr/>
                <b-form-group>
                    <b-card no-body>
                        <b-tabs card v-model="selectedScheduleType">
                            <b-tab title="Instant Scheduler" active>
                                <b-card-text>Crawl job is scheduled that run instantly</b-card-text>
                            </b-tab>
                            <b-tab title="Interval Scheduler">
                                <b-card-text>Crawl job is scheduled that run at a specific interval</b-card-text>
                                <b-row style="margin-top: -50px">
                                    <b-col cols="6" class="mt-5">
                                        <b-form-group
                                                :state="intervalOccurrence"
                                                label="Occurrence:"
                                                label-for="occurrence-input"
                                                invalid-feedback="Occurrence is required"
                                        >
                                            <b-form-input
                                                    id="occurrence-input"
                                                    v-model="jobForm.interval.occurrence"
                                                    :state="intervalOccurrence"
                                                    required
                                            ></b-form-input>
                                        </b-form-group>
                                    </b-col>
                                    <b-col cols="6" class="mt-5">
                                        <b-form-group
                                                label="Granularity:"
                                                label-for="granularity-input"
                                                invalid-feedback="Granularity is required"
                                        >
                                            <b-form-select v-model="selectedGranularity"
                                                           :options="granularityOptions"></b-form-select>
                                        </b-form-group>
                                    </b-col>
                                </b-row>
                            </b-tab>
                            <b-tab title="Cron Scheduler">
                                <b-card-text>Crawl job is scheduled that run as a cron job</b-card-text>
                                <b-row style="margin-top: -50px">
                                    <b-col cols="6" class="mt-5">
                                        <b-form-group
                                                :state="scheduleMinute"
                                                label="Schedule Minute:"
                                                label-for="schedule_minute-input"
                                                invalid-feedback="Minute is required"
                                        >
                                            <b-form-input
                                                    id="schedule_minute-input"
                                                    v-model="jobForm.periodic.schedule_minute"
                                                    :state="scheduleMinute"
                                                    required
                                            ></b-form-input>
                                        </b-form-group>
                                    </b-col>
                                    <b-col cols="6" class="mt-5">
                                        <b-form-group
                                                :state="scheduleHour"
                                                label="Schedule Hour:"
                                                label-for="schedule_hour-input"
                                                invalid-feedback="Hour is required"
                                        >
                                            <b-form-input
                                                    id="schedule_hour-input"
                                                    v-model="jobForm.periodic.schedule_hour"
                                                    :state="scheduleHour"
                                                    required
                                            ></b-form-input>
                                        </b-form-group>
                                    </b-col>
                                </b-row>
                                <b-row style="margin-top: -50px">
                                    <b-col cols="6" class="mt-5">
                                        <b-form-group
                                                :state="dayMonth"
                                                label="Day of Month:"
                                                label-for="day_of_month-input"
                                                invalid-feedback="Month is required"
                                        >
                                            <b-form-input
                                                    id="day_of_month-input"
                                                    v-model="jobForm.periodic.day_of_month"
                                                    :state="dayMonth"
                                                    required
                                            ></b-form-input>
                                        </b-form-group>
                                    </b-col>
                                    <b-col cols="6" class="mt-5">
                                        <b-form-group
                                                :state="monthYear"
                                                label="Month of Year:"
                                                label-for="month_of_year-input"
                                                invalid-feedback="Year is required"
                                        >
                                            <b-form-input
                                                    id="month_of_year-input"
                                                    v-model="jobForm.periodic.month_of_year"
                                                    :state="monthYear"
                                                    required
                                            ></b-form-input>
                                        </b-form-group>
                                    </b-col>
                                </b-row>
                                <b-row style="margin-top: -50px">
                                    <b-col cols="6" class="mt-5">
                                        <b-form-group
                                                :state="dayWeek"
                                                label="Day of Week:"
                                                label-for="day_of_week-input"
                                                invalid-feedback="Date of Week is required"
                                        >
                                            <b-form-input
                                                    id="day_of_week-input"
                                                    v-model="jobForm.periodic.day_of_week"
                                                    :state="dayWeek"
                                                    required
                                            ></b-form-input>
                                        </b-form-group>
                                    </b-col>
                                    <b-col cols="6" class="mt-5"></b-col>
                                </b-row>
                            </b-tab>
                        </b-tabs>
                    </b-card>
                </b-form-group>
            </form>
        </b-modal>
        <b-toast id="my-toast" variant="warning" solid>
            <template>
                <div class="d-flex flex-grow-1 align-items-baseline">
                    <b-img blank blank-color="#ff5555" class="mr-2" width="12" height="12"></b-img>
                    <strong class="mr-auto">Notice!</strong>
                    <small class="text-muted mr-2">42 seconds ago</small>
                </div>
            </template>
            This is the content of the toast.
            It is short and to the point.
        </b-toast>
    </div>
</template>

<script>
  import firebase from 'firebase/compat/app';
  import 'firebase/compat/auth';
  import 'firebase/compat/firestore';
  import {EventBus} from '@/router/bus'

  const separator = {
    template: `<hr style="border-color: rgba(0, 0, 0, 0.1); margin: 20px;">`
  };

  export default {
    name: 'Home',
    components: {}, created() {
      EventBus.$on('project_data', data => {
        const currentProjectData = [];
        data.forEach(function (obj) {
          currentProjectData.push(obj.project_name);
        });

        this.projectOptions = currentProjectData;
        if (this.projectOptions.length !== 0) {
          this.jobForm.projectName = this.projectOptions[currentProjectData.length - 1]
        }
      });
    },
    computed: {
      projectNameState() {
        return this.projectForm.projectName.length > 0
      },
      urlsState() {
        let regex = new RegExp(/^(http|https):\/\/[^ "]+$/);
        if (this.jobForm.urlValue.length > 0) {
          let isValidUrl = true;
          this.jobForm.urlValue.forEach(function (obj) {
            if (!regex.test(obj.toString())) {
              isValidUrl = false;
            }
          });
          return isValidUrl;
        }

        return false;
      },
      jobNameState() {
        return this.jobForm.jobName.length > 0
      },
      intervalOccurrence() {
        return this.jobForm.interval.occurrence > 0
      },
      scheduleMinute() {
        let cronRegex = new RegExp(/^(\*|[1-5]?[0-9](-[1-5]?[0-9])?)(\/[1-9][0-9]*)?(,(\*|[1-5]?[0-9](-[1-5]?[0-9])?)(\/[1-9][0-9]*)?)*$/
        );
        return cronRegex.test(this.jobForm.periodic.schedule_minute);
      },
      scheduleHour() {
        let cronRegex = new RegExp(/^(\*|(1?[0-9]|2[0-3])(-(1?[0-9]|2[0-3]))?)(\/[1-9][0-9]*)?(,(\*|(1?[0-9]|2[0-3])(-(1?[0-9]|2[0-3]))?)(\/[1-9][0-9]*)?)*$/);
        return cronRegex.test(this.jobForm.periodic.schedule_hour)
      },
      dayMonth() {
        let cronRegex = new RegExp(/^(\*|([1-9]|[1-2][0-9]?|3[0-1])(-([1-9]|[1-2][0-9]?|3[0-1]))?)(\/[1-9][0-9]*)?(,(\*|([1-9]|[1-2][0-9]?|3[0-1])(-([1-9]|[1-2][0-9]?|3[0-1]))?)(\/[1-9][0-9]*)?)*$/);
        return cronRegex.test(this.jobForm.periodic.day_of_month)
      },
      monthYear() {
        let cronRegex = new RegExp(/^(\*|([1-9]|1[0-2]?)(-([1-9]|1[0-2]?))?)(\/[1-9][0-9]*)?(,(\*|([1-9]|1[0-2]?)(-([1-9]|1[0-2]?))?)(\/[1-9][0-9]*)?)*$/);
        return cronRegex.test(this.jobForm.periodic.month_of_year)
      },
      dayWeek() {
        let cronRegex = new RegExp(/^(\*|[0-6](-[0-6])?)(\/[1-9][0-9]*)?(,(\*|[0-6](-[0-6])?)(\/[1-9][0-9]*)?)*$/);
        return cronRegex.test(this.jobForm.periodic.day_of_week)
      },
    },
    data() {
      return {
        jobForm: {
          jobName: '',
          crawler: 'crawlerx',
          projectName: null,
          urlValue: [],
          interval: {
            occurrence: 1,
          },
          periodic: {
            schedule_minute: '1',
            schedule_hour: '*',
            day_of_week: '*',
            day_of_month: '*',
            month_of_year: '*'
          },
        },
        projectForm: {
          projectName: '',
          description: ''
        },
        user_id: '',
        menu: [
          {
            header: true,
            title: 'Configurations',
            hiddenOnCollapse: true
          },
          {
            href: '/dashboard',
            title: 'Dashboard',
            icon: 'fa fa-desktop'
          },
          {
            header: true,
            title: 'Features',
            hiddenOnCollapse: true
          },
          {
            href: '/dashboard/projects',
            title: 'Projects',
            icon: 'fa fa-briefcase'
          },
          {
            href: '/dashboard/jobs',
            title: 'Instant Jobs',
            icon: 'fa fa-bell'
          },
          {
            href: '/dashboard/interval-jobs',
            title: 'Interval Jobs',
            icon: 'fa fa-clock'
          },
          {
            href: '/dashboard/cron-jobs',
            title: 'Cron Jobs',
            icon: 'fa fa-calendar'
          },
          {
            component: separator
          },
          {
            header: true,
            title: 'Analysis',
            hiddenOnCollapse: true
          },
          {
            href: '/dashboard/analysis',
            title: 'Elasticsearch Analysis',
            icon: 'fa fa-search-plus'
          }
        ],
        collapsed: false,
        selectedTheme: 'Default theme',
        isOnMobile: false,
        projectOptions: [],
        selectedProject: null,
        crawlerOptions: ["crawlerx", "stackoverflow", "wikipedia", "reddit", "github_trending", "tor_onion", "medium", "research_gate"],
        selectedGranularity: "HOURS",
        granularityOptions: ["MINUTES", "HOURS", "DAYS"],
        selectedScheduleType: 0,
      }
    },
    mounted() {
      this.onResize();
      window.addEventListener('resize', this.onResize);
      this.getProjects();
    },
    methods: {
      logout: function () {
        firebase.auth().signOut().then(() => {
          this.$router.replace('login');
        })
      },
      onToggleCollapse(collapsed) {
        this.collapsed = collapsed;
      },
      onResize() {
        if (window.innerWidth <= 767) {
          this.isOnMobile = true;
          this.collapsed = true;
        } else {
          this.isOnMobile = false;
          this.collapsed = false;
        }
      },
      checkProjectCreateFormValidity() {
        return this.projectForm.projectName.length > 0;
      },
      resetProjectCreateModal() {
        this.projectForm.projectName = '';
        this.projectForm.description = '';
      },
      handleProjectCreateOk(bvModalEvt) {
        // Prevent modal from closing
        bvModalEvt.preventDefault();
        // Trigger submit handler
        this.createProject()
      },
      createProject: function () {
        // Exit when the form isn't valid
        if (!this.checkProjectCreateFormValidity()) {
          return
        }

        this.$http.post(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/project/create',
          JSON.stringify({
            'user_id': this.$USER_ID, 'project_name': this.projectForm.projectName,
            'project_description': this.projectForm.description
          }),
          {headers: {'Content-Type': 'application/x-www-form-urlencoded', 'Access-Control-Allow-Origin': '*', 'Token': this.$TOKEN_ID}})
          .then(response => {
            this.$bvToast.toast(response.data['Message'], {
              title: 'Project Creation',
              toaster: 'b-toaster-top-right',
              solid: true,
              variant: 'success',
              appendToast: false
            });

            this.emitGlobalClickEventWhenProjectCreated()
          })
          .catch(e => {
            this.$bvToast.toast(e.response.data['Error'], {
              title: 'Project Creation',
              toaster: 'b-toaster-top-right',
              solid: true,
              variant: 'danger',
              appendToast: false
            });
          });

        // Hide the modal manually
        this.$nextTick(() => {
          this.$bvModal.hide('modal-new-project')
        })
      },
      checkJobCreateFormValidity() {
        return !(!this.jobForm.jobName.length > 0 || !this.jobForm.crawler.length > 0
          || !this.jobForm.projectName.length > 0 || !this.jobForm.urlValue.length > 0);
      },
      resetJobCreateModal() {
        this.jobForm.jobName = '';
        this.jobForm.urlValue = [];
        this.jobForm.interval.occurrence = 1;
      },
      handleJobCreateOk(bvModalEvt) {
        // Prevent modal from closing
        bvModalEvt.preventDefault();
        // Trigger submit handler
        this.createJob()
      },
      createJob: function () {
        // Exit when the form isn't valid
        if (!this.checkJobCreateFormValidity()) {
          return
        }

        if (this.selectedScheduleType === 1) {
          if (!(!this.jobForm.interval.occurrence.length > 0)) {
            return
          }
        }

        if (this.selectedScheduleType === 2) {
          if (!(!(!this.jobForm.periodic.schedule_minute.length > 0 || !this.jobForm.periodic.schedule_hour.length > 0
            || !this.jobForm.periodic.day_of_month.length > 0 || !this.jobForm.periodic.month_of_year.length > 0
            || !this.jobForm.periodic.day_of_week.length > 0))) {
            return
          }
        }

        let payload = {
          'user_id': this.$USER_ID, 'project_name': this.jobForm.projectName,
          'urls': this.jobForm.urlValue, 'crawler_name': this.jobForm.crawler,
          'job_name': this.jobForm.jobName
        };

        if (this.selectedScheduleType === 0) {
          payload['schedule_type'] = 'HOT_TASK';
          payload['schedule_data'] = {};
        } else if (this.selectedScheduleType === 1) {
          payload['schedule_type'] = 'INTERVAL_TASK';
          payload['schedule_data'] = {
            "occurrence" : this.jobForm.interval.occurrence,
            "granularity" : this.selectedGranularity
          };
        } else {
          payload['schedule_type'] = 'SCHEDULE_TASK';
          payload['schedule_data'] = {
            "schedule_minute" : this.jobForm.periodic.schedule_minute,
            "schedule_hour" : this.jobForm.periodic.schedule_hour,
            "day_of_month" : this.jobForm.periodic.day_of_month,
            "month_of_year" : this.jobForm.periodic.month_of_year,
            "day_of_week" : this.jobForm.periodic.day_of_week,
          };
        }

        this.$http.post(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/crawl/execute_job',
          JSON.stringify(payload),
          {headers: {'Content-Type': 'application/json'}})
          .then(response => {
            this.$bvToast.toast(response.data['Message'], {
              title: 'Crawl Job Schedule',
              toaster: 'b-toaster-top-right',
              solid: true,
              variant: 'success',
              appendToast: false
            });

            this.emitGlobalClickEventWhenJobCreated();
          })
          .catch(e => {
            this.$bvToast.toast(e.response.data['Error'], {
              title: 'Crawl Job Schedule',
              toaster: 'b-toaster-top-right',
              solid: true,
              variant: 'danger',
              appendToast: false
            });
          });

        // Hide the modal manually
        this.$nextTick(() => {
          this.$bvModal.hide('modal-new-job')
        })
      },
      getProjects() {
        if (this.projectOptions.length === 0) {
          this.$http.post(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/projects',
            JSON.stringify({'user_id': this.$USER_ID}),
            {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
            .then(response => {
              var projects = [];
              response.data.data.forEach(function (obj) {
                projects.push(obj.project_name)
              });
              this.projects = projects;
              this.projectOptions = projects;
              if (this.projectOptions.length !== 0) {
                this.jobForm.projectName = this.projectOptions[projects.length - 1]
              }
            })
            .catch(e => {
              this.$bvToast.toast(e.response.data['Error'], {
                title: 'Crawl Job Projects',
                toaster: 'b-toaster-top-right',
                solid: true,
                variant: 'danger',
                appendToast: false
              });
            });
        }
      },
      emitGlobalClickEventWhenProjectCreated() {
        EventBus.$emit('project_created', 'data');
      },
      emitGlobalClickEventWhenJobCreated() {
        EventBus.$emit('job_created', 'data');
      },
      loadTextFromFile(ev) {
        const file = ev.target.files[0];
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = evt => {
          var read = evt.target.result;
          var links = read.split("\n");
          let regex = new RegExp(/^(http|https):\/\/[^ "]+$/);
          var loadedUrls = this.jobForm.urlValue;
          links.forEach(function (url) {
            url = url.trim();
            var isValidUrl = regex.test(url);
            if (isValidUrl) {
              loadedUrls.push(url);
            }

          });

          this.jobForm.urlValue = loadedUrls;
        }
      }
    }
  }
</script>

<style lang="scss">
    body {
        font-family: 'Source Sans Pro', sans-serif;
        background-color: #f2f4f7;
    }

    #demo {
        padding-left: 350px;
        transition: 0.3s ease;
    }

    #demo.collapsed {
        padding-left: 50px;
    }

    #demo.onmobile {
        padding-left: 50px;
    }

    .sidebar-overlay {
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        background-color: #000;
        opacity: 0.5;
        z-index: 900;
    }

    /*.demo {*/
    /*padding: 50px;*/
    /*}*/

    .container {
        max-width: 900px;
    }

    pre {
        font-family: Consolas, monospace;
        color: #000;
        background: #fff;
        border-radius: 2px;
        padding: 15px;
        line-height: 1.5;
        overflow: auto;
    }
</style>