<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
        <mini-statistics-card
          title="Total Projects"
          :value="{
            text: projectCount,
          }"
          :percentage="{
            value: '+505%',
            color: 'text-success',
          }"
          :icon="{
            component: 'ni ni-folder-17',
            background: iconBackgroundPrimary,
          }"
          direction-reverse
        />
      </div>
      <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
        <mini-statistics-card
          title="Running Jobs"
          :value="{
            text: pendingJobCount,
          }"
          :percentage="{
            value: '+3%',
            color: 'text-warning',
          }"
          :icon="{
            component: 'ni ni-delivery-fast',
            background: iconBackgroundWarning,
          }"
          direction-reverse
        />
      </div>
      <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
        <mini-statistics-card
          title="Completed Jobs"
          :value="{
            text: completedJobCount,
          }"
          :percentage="{
            value: '-2%',
            color: 'text-danger',
          }"
          :icon="{
            component: 'ni ni-satisfied',
            background: iconBackgroundSuccess,
          }"
          direction-reverse
        />
      </div>
      <div class="col-xl-3 col-sm-6 mb-xl-0">
        <mini-statistics-card
          title="Failed Jobs"
          :value="{
            text: failedJobCount,
          }"
          :percentage="{
            value: '+5%',
            color: 'text-success',
          }"
          :icon="{
            component: 'ni ni-fat-remove',
            background: iconBackgroundDanger,
          }"
          direction-reverse
        />
      </div>
    </div>
    <div class="mt-4 row">
      <div class="col-lg-12">
        <!-- line chart -->
        <div class="card z-index-2">
          <gradient-line-chart
            id="chart-line"
            title="Jobs Scheduling Timeline"
            description="<i class='fa fa-arrow-up text-success'></i>
      <span class='font-weight-bold'>Data in 2022"
            :chart="{
              labels: [
                'Apr',
                'May',
                'Jun',
                'Jul',
                'Aug',
                'Sep',
                'Oct',
                'Nov',
                'Dec',
              ],
              datasets: [
                {
                  label: 'Mobile Apps',
                  data: [50, 40, 0, 220, 500, 250, 400, 230, 500],
                },
                {
                  label: 'Websites',
                  data: [30, 90, 40, 140, 290, 290, 340, 230, 400],
                },
              ],
            }"
          />
        </div>
      </div>
    </div>
    <div class="row my-4">
      <div class="col-lg-12 col-md-12 mb-md-0 mb-12">
        <projects-card />
      </div>
    </div>
  </div>
</template>
<script>
import MiniStatisticsCard from "@/examples/Cards/MiniStatisticsCard.vue";
import GradientLineChart from "@/examples/Charts/GradientLineChart.vue";
import ProjectsCard from "./components/ProjectsCard.vue";
import {
  faHandPointer,
  faUsers,
  faCreditCard,
  faScrewdriverWrench,
} from "@fortawesome/free-solid-svg-icons";
export default {
  name: "dashboard-default",
  data() {
    return {
      iconBackgroundPrimary: "bg-gradient-primary",
      iconBackgroundSuccess: "bg-gradient-success",
      iconBackgroundDanger: "bg-gradient-danger",
      iconBackgroundWarning: "bg-gradient-warning",
      faCreditCard,
      faScrewdriverWrench,
      faUsers,
      faHandPointer,
      projectCount: 0,
      completedJobCount: 0,
      pendingJobCount: 0,
      failedJobCount: 0,
    };
  },
  components: {
    MiniStatisticsCard,
    GradientLineChart,
    ProjectsCard,
  },
};
</script>
