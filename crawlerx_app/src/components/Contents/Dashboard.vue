<template>
    <b-container fluid>
        <b-row>
            <b-col cols="12" class="mt-4">
                <b-card-group deck>
                    <b-card bg-variant="secondary" text-variant="white" header="Projects Count" class="text-center">
                        <b-card-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</b-card-text>
                    </b-card>

                    <b-card bg-variant="success" text-variant="white" header="Completed Job Count" class="text-center">
                        <b-card-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</b-card-text>
                    </b-card>

                    <b-card bg-variant="warning" text-variant="white" header="Pending Job Count" class="text-center">
                        <b-card-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</b-card-text>
                    </b-card>
                </b-card-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="12" class="mt-5">
                <h6>Crawling Job Details:</h6>
            </b-col>
        </b-row>
        <b-row>
            <b-col cols="12" class="mt-3">
                <b-table striped hover :items="items"></b-table>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
    export default {
        name: 'DashboardPage',
        data() {
            return {
                items: []
            }
        }, mounted() {
            this.getCrawledJobData();
        }, methods: {
            getCrawledJobData: function () {
                this.$http.post('http://localhost:8000/api/project/jobs',
                    JSON.stringify({'user_id': this.$USER_ID}),
                    {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
                    .then(response => {
                        var job_items = [];
                        response.data.data.forEach(function(obj) {
                            job_items.push({project_name: obj.project_id, job_id: obj.task_id, crawler_type: obj.crawler_name, status: obj.status})
                        });
                        this.items = job_items;
                    })
                    .catch(e => {
                        alert(e.getError().toString())
                    });
            }
        }
    }
</script>