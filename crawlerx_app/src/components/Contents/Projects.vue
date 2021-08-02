<template>
    <b-container fluid>
        <b-row>
            <b-col cols="12" class="mt-4">
                <h5>Owned Projects</h5>
                <hr/>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="3" class="mt-4" v-for="item in projects" :key="item.project_name">
                <b-card bg-variant="light" no-body :header='item.project_name' style="font-weight: bold;" icon="exclamation-circle-fill"
                        v-b-toggle="'test'">
                    <b-collapse :id="'test'" visible class="mt-2">
                        <b-list-group flush style="font-weight: lighter;">
                            <b-list-group-item class="d-flex justify-content-between align-items-center">
                                Total Crawled Jobs
                                <b-badge variant="primary" pill>{{item.total_jobs}}</b-badge>
                            </b-list-group-item>
                            <b-list-group-item class="d-flex justify-content-between align-items-center">Completed
                                Crawled Jobs
                                <b-badge variant="success" pill>{{item.completed_jobs}}</b-badge>
                            </b-list-group-item>
                            <b-list-group-item class="d-flex justify-content-between align-items-center">Pending Crawled
                                Jobs
                                <b-badge variant="warning" pill>{{item.pending_jobs}}</b-badge>
                            </b-list-group-item>
                            <b-list-group-item class="d-flex justify-content-between align-items-center">Failed Crawled
                                Jobs
                                <b-badge variant="danger" pill>{{item.failed_jobs}}</b-badge>
                            </b-list-group-item>
                        </b-list-group>
                    </b-collapse>

                    <b-card-body
                            style="font-weight: lighter; border-top:1px solid #e3e3e3; max-height: 100px; min-height: 100px;
                            overflow: auto; padding-top:6px; padding-bottom:6px;">
                        {{item.project_description}}
                    </b-card-body>
                </b-card>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
    import { EventBus } from '../../router/bus';

    export default {
        name: 'Projects',
        data() {
            return {
                projects: []
            }
        }, mounted() {
            this.getCrawledProjectData();
        },created() {
            EventBus.$on('project_created', data => {
                this.getCrawledProjectData();
            });

            EventBus.$on('job_created', data => {
                this.getCrawledProjectData();
            });
        },
        methods: {
            getCrawledProjectData: function () {
                var project_items = [];

                this.$http.post(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/projects',
                    JSON.stringify({'user_id': this.$USER_ID}),
                    {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
                    .then(response => {
                        response.data.data.forEach(function (obj) {
                            project_items.push({
                                project_name: obj.project_name, project_description: obj.project_description,
                                total_jobs: 0, completed_jobs: 0, pending_jobs: 0, failed_jobs: 0
                            })
                        });

                        this.$http.post(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/jobs',
                            JSON.stringify({'user_id': this.$USER_ID}),
                            {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
                            .then(response => {
                                response.data.data.forEach(function (obj) {
                                    var project_name = obj.project_name;
                                    project_items.forEach(function (item) {
                                        if (item.project_name === project_name) {
                                            item.total_jobs += 1;
                                            if (obj.status === "COMPLETED") {
                                                item.completed_jobs += 1;
                                            } else if (obj.status === "PENDING" || obj.status === "RUNNING") {
                                                item.pending_jobs += 1;
                                            } else if (obj.status === "FAILED") {
                                                item.failed_jobs += 1;
                                            }
                                        }
                                    });
                                });
                            })
                            .catch(e => {
                                alert(e.getError().toString())
                            });
                    })
                    .catch(e => {
                        alert(e.getError().toString())
                    });

                this.projects = project_items;
            }
        }
    }
</script>