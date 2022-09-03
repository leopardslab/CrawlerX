<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="mb-4 card">
          <div class="p-3 pb-0 card-header">
            <h6 class="mb-1">Projects</h6>
            <p class="text-sm">Setup Crawling Project List</p>
          </div>
          <div class="p-3 card-body">
            <div class="row">
             <default-project-card
                title="Research Data"
                :image="img2"
                label="Project #1"
                description="This project has crawling data related to Researches."
                :authors="[]"
                :action="{
                  color: 'success',
                  label: 'View Project',
                }"
              />

              <default-project-card
                title="Article Data"
                :image="img1"
                label="Project #2"
                description="This project has crawling data related to Articles."
                :authors="[]"
                :action="{
                  color: 'success',
                  label: 'View Project',
                }"
              />

              <default-project-card
                title="Social Media Data"
                :image="img3"
                label="Project #3"
                description="This project has crawling data related to Social Media."
                :authors="[]"
                :action="{
                  color: 'success',
                  label: 'View Project',
                }"
              />

              <div class="mb-4 col-xl-3 col-md-6 mb-xl-0">
                <place-holder-card
                  :title="{ text: 'New project', variant: 'h5' }"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DefaultProjectCard from "./components/DefaultProjectCard.vue";
import img1 from "@/assets/img/home-decor-1.jpg";
import img2 from "@/assets/img/home-decor-2.jpg";
import img3 from "@/assets/img/home-decor-3.jpg";
import PlaceHolderCard from "@/examples/Cards/PlaceHolderCard.vue";

export default {
  name: "projects",
  components: {
    DefaultProjectCard,
    PlaceHolderCard,
  },
  data() {
    return {
      img1,
      img2,
      img3,
    }
  }
};
</script>
