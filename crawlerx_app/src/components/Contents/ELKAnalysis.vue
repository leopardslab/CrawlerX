<template>
    <b-container fluid>
        <b-row>
            <b-col cols="12" class="mt-5">
                <h5><b>Enter the Query:</b></h5>
            </b-col>
        </b-row>
        <b-input-group prepend="Search by Query" class="mt-3">
            <b-form-input v-model="query"></b-form-input>
            <b-input-group-append>
                <b-button variant="info" @click="getAnalysisByQuery">Submit Query</b-button>
            </b-input-group-append>
        </b-input-group>
        <hr/>
        <b-row>
            <b-col cols="12" class="mt-3">
                <h5><b>ElasticSearch Result:</b></h5>
                <pre style="min-height: 300px; max-height: 60vh; overflow-y: scroll;"><code>{{ searchedData }}</code></pre>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
    export default {
        name: 'ELKAnalysis',
        data() {
            return {
                searchedData: null,
                query: ''
            }
        }, methods: {
            getAnalysisByQuery: function () {
                this.$http.post(process.env.VUE_APP_DJANGO_PROTOCOL + '://' + process.env.VUE_APP_DJANGO_HOSTNAME + ':' +  process.env.VUE_APP_DJANGO_PORT + '/api/elasticdata',
                    JSON.stringify({'user_id': this.$USER_ID, 'query': this.query}),
                    {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
                    .then(response => {
                        this.searchedData = response;
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