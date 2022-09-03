<template>
  <div class="card mb-4">
    <div class="card-header pb-0">
      <h6>Executed Jobs</h6>
    </div>
    <div class="card-body px-0 pt-0 pb-2">
      <div class="table-responsive p-0">
        <table class="table align-items-center mb-0">
          <thead>
            <tr>
              <th
                class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                Job Name
              </th>
              <th
                class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                Job Id
              </th>
              <th
                class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                URL
              </th>
              <th
                class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                Crawler Type
              </th>
              <th 
                class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
              Status
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <div class="d-flex px-2 py-1">
                  <div>
                    <soft-avatar
                      :img="img1"
                      size="sm"
                      border-radius="lg"
                      class="me-3"
                      alt="user1"
                    />
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">Onion Darkweb Data</h6>
                  </div>
                </div>
              </td>
              <td class="">
                <span class="text-secondary text-xs font-weight-bold"
                  >222ba960-bb07-48f6-8b6a-d3ce55e01954</span
                >
              </td>
              <td class="text-sm">
                <span class="text-secondary text-xs font-weight-bold"
                  >http://zerobinqmdqd236y.onion</span
                >
              </td>
              <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold"
                  >Tor Onion</span
                >
              </td>
              <td class="align-middle text-center text-sm">
                <soft-badge color="warning" variant="gradient" size="sm"
                  >Running</soft-badge
                >
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2 py-1">
                  <div>
                    <soft-avatar
                      :img="img1"
                      size="sm"
                      border-radius="lg"
                      class="me-3"
                      alt="user1"
                    />
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">Medium Darkweb Data</h6>
                  </div>
                </div>
              </td>
              <td class="">
                <span class="text-secondary text-xs font-weight-bold"
                  >322ba960-bb07-48f6-8b6a-d3ce55e019533</span
                >
              </td>
              <td class="text-sm">
                <span class="text-secondary text-xs font-weight-bold"
                  >https://medium.com/@laura.baranik/in-search-of-the-long-covid-cure-101144a1c101</span
                >
              </td>
              <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold"
                  >Medium</span
                >
              </td>
              <td class="align-middle text-center text-sm">
                <soft-badge color="success" variant="gradient" size="sm"
                  >Complete</soft-badge
                >
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2 py-1">
                  <div>
                    <soft-avatar
                      :img="img1"
                      size="sm"
                      border-radius="lg"
                      class="me-3"
                      alt="user1"
                    />
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">Link Data</h6>
                  </div>
                </div>
              </td>
              <td class="">
                <span class="text-secondary text-xs font-weight-bold"
                  >922ba960-bb07-48f6-8b6a-d3ce55e0195444</span
                >
              </td>
              <td class="text-sm">
                <span class="text-secondary text-xs font-weight-bold"
                  >https://twitter.com/Google?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor</span
                >
              </td>
              <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold"
                  >CrawlerX</span
                >
              </td>
              <td class="align-middle text-center text-sm">
                <soft-badge color="warning" variant="gradient" size="sm"
                  >Running</soft-badge
                >
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2 py-1">
                  <div>
                    <soft-avatar
                      :img="img1"
                      size="sm"
                      border-radius="lg"
                      class="me-3"
                      alt="user1"
                    />
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">Github Data</h6>
                  </div>
                </div>
              </td>
              <td class="">
                <span class="text-secondary text-xs font-weight-bold"
                  >822ba960-bb07-48f6-8b6a-d3ce55e01954423</span
                >
              </td>
              <td class="text-sm">
                <span class="text-secondary text-xs font-weight-bold"
                  >https://github.com/creativetimofficial/vue-soft-ui-dashboard</span
                >
              </td>
              <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold"
                  >Github</span
                >
              </td>
              <td class="align-middle text-center text-sm">
                <soft-badge color="danger" variant="gradient" size="sm"
                  >Failed</soft-badge
                >
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2 py-1">
                  <div>
                    <soft-avatar
                      :img="img1"
                      size="sm"
                      border-radius="lg"
                      class="me-3"
                      alt="user1"
                    />
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">Stackoverflow Data</h6>
                  </div>
                </div>
              </td>
              <td class="">
                <span class="text-secondary text-xs font-weight-bold"
                  >922ba960-bb07-48f6-8b6a-d3ce55e01954555</span
                >
              </td>
              <td class="text-sm">
                <span class="text-secondary text-xs font-weight-bold"
                  >https://stackoverflow.com/questions</span
                >
              </td>
              <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold"
                  >Stackoverflow</span
                >
              </td>
              <td class="align-middle text-center text-sm">
                <soft-badge color="success" variant="gradient" size="sm"
                  >Complete</soft-badge
                >
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2 py-1">
                  <div>
                    <soft-avatar
                      :img="img1"
                      size="sm"
                      border-radius="lg"
                      class="me-3"
                      alt="user1"
                    />
                  </div>
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">Research Gate Data</h6>
                  </div>
                </div>
              </td>
              <td class="">
                <span class="text-secondary text-xs font-weight-bold"
                  >022ba960-bb07-48f6-8b6a-d3ce55e01954533</span
                >
              </td>
              <td class="text-sm">
                <span class="text-secondary text-xs font-weight-bold"
                  >https://sresearchgate.com</span
                >
              </td>
              <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold"
                  >Research Gate</span
                >
              </td>
              <td class="align-middle text-center text-sm">
                <soft-badge color="success" variant="gradient" size="sm"
                  >Complete</soft-badge
                >
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import SoftAvatar from "@/components/SoftAvatar.vue";
import SoftBadge from "@/components/SoftBadge.vue";
import img1 from "../../assets/img/small-logos/logo-xd.svg";

export default {
  name: "authors-table",
  data() {
    return {
      img1,
    };
  },
  components: {
    SoftAvatar,
    SoftBadge,
  },
};
</script>
