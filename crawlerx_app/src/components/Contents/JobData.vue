<template>
    <b-container fluid>
        <b-row>
            <b-col cols="12" class="mt-5">
                <h5><b>Job Id:</b> {{this.$route.params.jobId}}</h5>
                <b-button variant="outline-info" style="float: right; margin-top:-40px;"
                          @click="getCurrentJobData">
                    <b-icon icon="arrow-repeat" font-scale="1"></b-icon>
                    Refresh
                </b-button>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="12" class="mt-3">
                <b-table striped hover :bordered="bordered" :borderless="borderless" :head-variant="headVariant" :items="jobData"></b-table>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="12" class="mt-3">
                <h5><b>Crawled Data:</b></h5>
                <pre style="min-height: 300px; max-height: 60vh; overflow-y: scroll;"><code>{{ crawledData }}</code></pre>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
    export default {
        name: 'JobData',
        data() {
            return {
                borderless: false,
                headVariant: 'dark',
                bordered: true,
                jobData: [],
                taskId: null,
                jobStatus: null,
                crawledData: null
            }
        }, mounted() {
            this.getCurrentJobData();
        }, methods: {
            getCurrentJobData: function () {
                this.$http.post('http://localhost:8000/api/job',
                    JSON.stringify({'user_id': this.$USER_ID, 'unique_id': this.$route.params.jobId}),
                    {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
                    .then(response => {
                        var project = [];
                        var objectTaskId = null;
                        var objectTaskStatus = null;
                        response.data.data.forEach(function(obj) {
                            objectTaskId = obj.task_id;
                            if (objectTaskId === undefined || objectTaskId == null || objectTaskId === '') {
                                objectTaskId = "STILL_PROCESSING";
                            }
                            project.push({project_name: obj.project_name, job_name:obj.job_name, task_id: objectTaskId, URL: obj.url,
                                crawler_type: obj.crawler_name, status: obj.status});
                            objectTaskStatus = obj.status;
                        });
                        this.taskId = objectTaskId;
                        this.jobStatus = objectTaskStatus;

                        if (this.taskId !== null && this.jobStatus === 'COMPLETED') {
                            this.$http.post('http://localhost:8000/api/job/crawldata',
                                JSON.stringify({'user_id': this.$USER_ID, 'unique_id': this.$route.params.jobId, 'task_id': this.taskId}),
                                {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
                                .then(response => {
                                    this.crawledData = JSON.stringify({ 'data' : response.data.data[0].data }, undefined, 4);
                                })
                                .catch(e => {
                                    alert(e.getError().toString())
                                });
                        }

                        this.jobData = project;
                    })
                    .catch(e => {
                        alert(e.getError().toString())
                    });
            }
        }
    }
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
</style>