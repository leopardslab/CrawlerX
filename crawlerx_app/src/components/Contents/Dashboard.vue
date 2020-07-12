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
      <b-col cols="12"  class="mt-5">
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
        items: [
          {project_name: 40, job_id: 'Dickerson', crawler_type: 'Macdonald', status: 'Done'},
          {project_name: 21, job_id: 'Larsen', crawler_type: 'Shaw', status: 'Done'},
          {project_name: 89, job_id: 'Geneva', crawler_type: 'Wilson', status: 'Done'},
          {project_name: 38, job_id: 'Jami', crawler_type: 'Carney', status: 'Done'}
        ]
      }
    }
  }
</script>