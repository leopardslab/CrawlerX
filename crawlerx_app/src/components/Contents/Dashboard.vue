<template>
    <b-container fluid>
        <b-row>
            <b-col cols="12" class="mt-4">
                <b-card-group deck>
                    <b-card bg-variant="secondary" text-variant="white" header="Projects Count" class="text-center">
                        <b-card-text style="font-size:35px;">{{projectCount}}</b-card-text>
                    </b-card>

                    <b-card bg-variant="success" text-variant="white" header="Completed Job Count" class="text-center">
                        <b-card-text style="font-size:35px;">{{completedJobCount}}</b-card-text>
                    </b-card>

                    <b-card bg-variant="warning" text-variant="white" header="Pending Job Count" class="text-center">
                        <b-card-text style="font-size:35px;">{{pendingJobCount}}</b-card-text>
                    </b-card>
                </b-card-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="12" class="mt-5">
                <h6>Crawling Job Details:</h6>
                <b-button variant="outline-info" style="float: right; margin-top:-40px;" @click="getCrawledJobData">
                    <b-icon icon="arrow-repeat" font-scale="1"></b-icon> Refresh
                </b-button>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="12" class="mt-3">
                <b-table striped hover :items="jobItems"></b-table>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
    import { EventBus } from '../../router/bus';

    export default {
        name: 'DashboardPage',
        data() {
            return {
                jobItems: [],
                projectCount: 0,
                completedJobCount: 0,
                pendingJobCount: 0,
                projects: [],
            }
        },created() {
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
            getCrawledJobData: function () {
                this.$http.post('http://localhost:8000/api/project/jobs',
                    JSON.stringify({'user_id': this.$USER_ID}),
                    {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
                    .then(response => {
                        var job_items = [];
                        var completedJobCount = 0;
                        var pendingJobCount = 0;
                        response.data.data.forEach(function(obj) {
                            var taskId = obj.task_id;
                            if (taskId === undefined || taskId == null || taskId === '') {
                                taskId = "STILL_PROCESSING";
                            }
                            job_items.push({project_name: obj.project_name, job_name:obj.job_name, job_id: taskId,
                                crawler_type: obj.crawler_name, status: obj.status});
                            if (obj.status === "COMPLETED") {
                                completedJobCount += 1;
                            } else if (obj.status === "PENDING" || obj.status === "RUNNING") {
                                pendingJobCount += 1;
                            }
                        });

                        if (response.data.data.length === 0) {
                            job_items.push({project_name: "-", job_name: "-", job_id: "-",
                                crawler_type: "-", status: "-"});
                        }

                        this.completedJobCount = completedJobCount;
                        this.pendingJobCount = pendingJobCount;
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
                        response.data.data.forEach(function(obj) {
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
            }
        }
    }
</script>