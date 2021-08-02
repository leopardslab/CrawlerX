<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <b-container fluid>
        <b-row>
            <b-col cols="12" class="mt-5">
                <h5>Crawled Job Details:</h5>
                <b-button variant="outline-info" style="float: right; margin-top:-40px;"
                          @click="getCrawledJobDataProjectWise">
                    <b-icon icon="arrow-repeat" font-scale="1"></b-icon>
                    Refresh
                </b-button>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="12" class="mt-3">
                <b-list-group>
                    <b-list-group-item class="flex-column align-items-start"
                                       v-for="item in projectsWiseJobs" :key="item.project_name">
                        <h6>Project - {{item.project_name}}</h6>
                        <b-table striped hover :bordered="bordered" :borderless="borderless" :head-variant="headVariant"
                                 :items="item.jobs">
                            <template v-slot:cell(job_id)="data">
                                <router-link :to="'/dashboard/job/' + data.value">{{data.value}}</router-link>
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
                        </b-table>
                    </b-list-group-item>
                </b-list-group>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
    import {EventBus} from '../../router/bus';

    export default {
        name: 'JobsPage',
        data() {
            return {
                borderless: false,
                headVariant: 'dark',
                bordered: true,
                jobItems: [],
                projectsWiseJobs: [],
            }
        }, created() {
            EventBus.$on('project_created', data => {
                this.getCrawledJobDataProjectWise();
            });

            EventBus.$on('job_created', data => {
                this.getCrawledJobDataProjectWise();
            });
        }, mounted() {
            this.getCrawledJobDataProjectWise();
        }, methods: {
            getCrawledJobDataProjectWise: function () {
                var project_drilldown = [];
                this.$http.post(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/projects',
                    JSON.stringify({'user_id': this.$USER_ID}),
                    {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
                    .then(response => {
                        response.data.data.forEach(function (obj) {
                            project_drilldown.push({project_name: obj.project_name, jobs: []})
                        });

                        this.$http.post(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/jobs',
                            JSON.stringify({'user_id': this.$USER_ID, 'schedule_category': 'Instant'}),
                            {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
                            .then(response => {
                                response.data.data.forEach(function (obj) {
                                    project_drilldown.forEach(function (item) {
                                        if (item.project_name === obj.project_name) {
                                            item.jobs.push({
                                                job_name: obj.job_name, job_id: obj.unique_id, URL: obj.url,
                                                crawler_type: obj.crawler_name, status: obj.status
                                            });
                                        }
                                    });
                                });

                                project_drilldown.forEach(function (item) {
                                    if (item.jobs.length === 0) {
                                        item.jobs.push({job_name: "-", job_id: "-", crawler_type: "-", status: "-"});
                                    }
                                });
                            })
                            .catch(e => {
                                alert(e.getError().toString())
                            });
                    })
                    .catch(e => {
                        alert(e.getError().toString())
                    });
                this.projectsWiseJobs = project_drilldown;
            }
        }
    }
</script>