<template>
  <div class="card">
    <div class="card-header pb-0">
      <div class="row">
        <div class="col-lg-6 col-7">
          <h6>Projects</h6>
          <p class="text-sm mb-0">
            <i class="fa fa-check text-info" aria-hidden="true"></i>
            <span class="font-weight-bold ms-1">30</span> jobs have been scheduled
          </p>
        </div>
      </div>
    </div>
    <div class="card-body px-0 pb-2">
      <div class="table-responsive" style="height: 400px">
        <table class="table align-items-center mb-0">
          <thead>
            <tr>
              <th
                class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                Project
              </th>
              <th
                class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                Job Name
              </th>
              <th
                class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                Job ID
              </th>
              <th
                class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                Spider Type
              </th>
              <th
                class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                Scheduler
              </th>
              <th
                class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                Status
              </th>
              <th
                class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                Action
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <div class="d-flex px-2 py-1">
                  <div>
                    <soft-avatar :img="img1" size="sm" class="me-3" alt="xd" />
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">Soft UI XD Version</h6>
                  </div>
                </div>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <button
                  type="button"
                  class="mb-0 btn btn-sm btn-outline-danger"
                >
                  Delete
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2 py-1">
                  <div>
                    <soft-avatar :img="img1" size="sm" class="me-3" alt="xd" />
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">Soft UI XD Version</h6>
                  </div>
                </div>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <button
                  type="button"
                  class="mb-0 btn btn-sm btn-outline-danger"
                >
                  Delete
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2 py-1">
                  <div>
                    <soft-avatar :img="img1" size="sm" class="me-3" alt="xd" />
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">Soft UI XD Version</h6>
                  </div>
                </div>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <span class="text-xs font-weight-bold">$14,000</span>
              </td>
              <td class="align-middle text-center text-sm">
                <button
                  type="button"
                  class="mb-0 btn btn-sm btn-outline-danger"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import setTooltip from "@/assets/js/tooltip.js";
import SoftAvatar from "@/components/SoftAvatar.vue";
import img1 from "../../assets/img/small-logos/logo-xd.svg";
import img2 from "../../assets/img/team-1.jpg";
import img3 from "@/assets/img/team-2.jpg";
import img4 from "../../assets/img/team-3.jpg";
import img5 from "../../assets/img/team-4.jpg";
import img6 from "../../assets/img/small-logos/logo-atlassian.svg";
import img7 from "../../assets/img/team-2.jpg";
import img8 from "../../assets/img/team-4.jpg";
import img9 from "../../assets/img/small-logos/logo-slack.svg";
import img10 from "../../assets/img/team-3.jpg";
import img11 from "../../assets/img/team-1.jpg";
import img12 from "../../assets/img/small-logos/logo-spotify.svg";
import img13 from "../../assets/img/team-4.jpg";
import img14 from "../../assets/img/team-3.jpg";
import img15 from "../../assets/img/team-4.jpg";
import img16 from "../../assets/img/team-1.jpg";
import img17 from "../../assets/img/small-logos/logo-jira.svg";
import img18 from "../../assets/img/team-4.jpg";
import img19 from "../../assets/img/small-logos/logo-invision.svg";
import img20 from "../../assets/img/team-1.jpg";
import img21 from "../../assets/img/team-4.jpg";

export default {
  name: "projects-card",
  data() {
    return {
      img1,
      img2,
      img3,
      img4,
      img5,
      img6,
      img7,
      img8,
      img9,
      img10,
      img11,
      img12,
      img13,
      img14,
      img15,
      img16,
      img17,
      img18,
      img19,
      img20,
      img21,
    };
  },
  components: {
    SoftAvatar,
  },
  mounted() {
    setTooltip();
  },
};
</script>
