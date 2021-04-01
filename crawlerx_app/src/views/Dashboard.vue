<template>
    <div
            id="demo"
            :class="[{'collapsed' : collapsed}, {'onmobile' : isOnMobile}]"
    >
        <div class="">
            <md-toolbar md-get-palette-color="red" md-elevation="1">
                <h3 class="md-title" style="flex: 1"><b>CrawlerX</b> - Open-Source Crawling Platform</h3>
                <b-button v-b-modal.modal-new-project variant="outline-secondary">Create a Project</b-button>
                <b-button v-b-modal.modal-new-job variant="outline-secondary" class="ml-2">Schedule a Job</b-button>
                <b-button variant="primary" class="ml-2" @click="logout">Logout</b-button>
            </md-toolbar>
            <sidebar-menu
                    :menu="menu"
                    :collapsed="collapsed"
                    :theme="selectedTheme"
                    :show-one-child="true"
                    @toggle-collapse="onToggleCollapse"
                    @item-click="onItemClick"
            />
            <router-view/>
            <div
                    v-if="isOnMobile && !collapsed"
                    class="sidebar-overlay"
                    @click="collapsed = true"></div>
        </div>

        <b-modal id="modal-new-project" ref="modal" size="lg" title="Create a new project"
                 @show="resetProjectCreateModal" @hidden="resetProjectCreateModal" @ok="handleProjectCreateOk">
            <b-form ref="form"  v-on:submit.prevent="createProject">
                <b-form-group
                        :state="projectNameState"
                        label="Project Name:"
                        label-for="name-input"
                        invalid-feedback="Name is required"
                >
                    <b-form-input
                            id="name-input"
                            v-model="projectForm.projectName"
                            :state="projectNameState"
                            required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                        label="Project Description:"
                        label-for="description-input"
                >
                    <b-form-textarea
                            id="description"
                            v-model="projectForm.description"
                            placeholder="About the project..."
                            rows="3"
                            max-rows="6"
                    ></b-form-textarea>
                </b-form-group>
            </b-form>
        </b-modal>

        <b-modal id="modal-new-job" size="lg" title="Create a new crawl job"
                 @show="resetJobCreateModal" @hidden="resetJobCreateModal" @ok="handleJobCreateOk">
            <form ref="form" @submit.stop.prevent="createJob">
                <b-form-group
                        :state="jobNameState"
                        label="Job Name:"
                        label-for="name-input"
                        invalid-feedback="Name is required"
                >
                    <b-form-input
                            id="name-input"
                            v-model="jobForm.jobName"
                            :state="jobNameState"
                            required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                        label="Project:"
                        label-for="project-input"
                >
                    <b-form-select v-model="jobForm.projectName" :options="projectOptions" />
                </b-form-group>
                <b-form-group
                        label="Crawling Type:"
                        label-for="crawl-type-input"
                >
                    <b-form-select v-model="jobForm.crawler" :options="crawlerOptions" />
                </b-form-group>
                <b-form-group
                        label="URLs:"
                        :state="urlsState"
                        label-for="url-input"
                        invalid-feedback="Enter multiple HTTP or HTTPS valid URLs "
                >
                    <b-form-tags
                            input-id="url-tags"
                            :input-attrs="{ 'aria-describedby': 'tags-remove-on-delete-help' }"
                            v-model="jobForm.urlValue"
                            separator=" "
                            placeholder="Enter new urls separated by space"
                            remove-on-delete
                            no-add-on-enter
                            :state="urlsState"
                            class="mb-2"
                    ></b-form-tags>
                    <b-form-text id="tags-remove-on-delete-help">
                        Press <kbd>Backspace</kbd> to remove the last url entered
                    </b-form-text>
                </b-form-group>
                <b-form-group
                        label="Load URLs from a File:"
                        label-for="file-input"
                >
                    <input type="file" @change="loadTextFromFile">
                </b-form-group>
                <b-form-group
                        label="Schedule the Job:"
                        label-for="schedule-input"
                >
                    <b-form-datepicker id="example-datepicker" v-model="jobForm.scheduleDate" class="mb-2"></b-form-datepicker>
                    <b-form-timepicker v-model="jobForm.scheduleTime" show-seconds locale="en"></b-form-timepicker>
                </b-form-group>
            </form>
        </b-modal>
        <b-toast id="my-toast" variant="warning" solid>
            <template>
                <div class="d-flex flex-grow-1 align-items-baseline">
                    <b-img blank blank-color="#ff5555" class="mr-2" width="12" height="12"></b-img>
                    <strong class="mr-auto">Notice!</strong>
                    <small class="text-muted mr-2">42 seconds ago</small>
                </div>
            </template>
            This is the content of the toast.
            It is short and to the point.
        </b-toast>
    </div>
</template>

<script>
   import firebase from "firebase/app";
    import { EventBus } from '../router/bus'

    const separator = {
        template: `<hr style="border-color: rgba(0, 0, 0, 0.1); margin: 20px;">`
    };

    export default {
        name: 'Home',
        components: {
            // HelloWorld,
        }, created() {
            EventBus.$on('project_data', data => {
                var currentProjectData = [];
                data.forEach(function (obj) {
                    currentProjectData.push(obj.project_name);
                });

                this.projectOptions = currentProjectData;
                if (this.projectOptions.length !== 0) {
                    this.jobForm.projectName = this.projectOptions[currentProjectData.length - 1]
                }
            });
        },
        computed: {
            projectNameState() {
                return this.projectForm.projectName.length > 0
            },
            urlsState() {
                let regex = new RegExp(/^(http|https):\/\/[^ "]+$/);
                if (this.jobForm.urlValue.length > 0) {
                    var isValidUrl = true;
                    this.jobForm.urlValue.forEach(function (obj) {
                        if (!regex.test(obj.toString())) {
                            isValidUrl = false;
                        }
                    });
                    return isValidUrl;
                }

                return false;
            },
            jobNameState() {
                return this.jobForm.jobName.length > 0
            }
        },
        data() {
            return {
                jobForm: {
                    jobName: '',
                    crawler: 'crawlerx',
                    projectName: null,
                    urlValue: [],
                    scheduleDate: '',
                    scheduleTime: ''
                },
                projectForm: {
                    projectName: '',
                    description: ''
                },
                user_id: '',
                menu: [
                    {
                        header: true,
                        title: 'Configurations',
                        hiddenOnCollapse: true
                    },
                    {
                        href: '/dashboard',
                        title: 'Dashboard',
                        icon: 'fa fa-download'
                    },
                    {
                        header: true,
                        title: 'Features',
                        hiddenOnCollapse: true
                    },
                    {
                        href: '/dashboard/projects',
                        title: 'Projects',
                        icon: 'fa fa-cogs'
                    },
                    {
                        href: '/dashboard/jobs',
                        title: 'Jobs',
                        icon: 'fa fa-bell'
                    },
                    {
                        component: separator
                    },
                    {
                        header: true,
                        title: 'Analysis',
                        hiddenOnCollapse: true
                    },
                    {
                        href: '/dashboard/analysis',
                        title: 'ELK Analysis',
                        icon: 'fa fa-bell'
                    }
                ],
                collapsed: false,
                selectedTheme: 'Default theme',
                isOnMobile: false,
                projectOptions: [],
                selectedProject: null,
                crawlerOptions: ["crawlerx", "stackoverflow", "wikipedia", "reddit"]
            }
        },
        mounted() {
            this.onResize();
            window.addEventListener('resize', this.onResize);
            this.getProjects();
        },
        methods: {
            logout: function () {
                firebase.auth().signOut().then(() => {
                    this.$router.replace('login');
                })
            },
            onToggleCollapse(collapsed) {
                this.collapsed = collapsed;
            },
            onResize() {
                if (window.innerWidth <= 767) {
                    this.isOnMobile = true;
                    this.collapsed = true;
                } else {
                    this.isOnMobile = false;
                    this.collapsed = false;
                }
            },
            checkProjectCreateFormValidity() {
                return this.projectForm.projectName.length > 0;
            },
            resetProjectCreateModal() {
                this.projectForm.projectName = '';
                this.projectForm.description = '';
            },
            handleProjectCreateOk(bvModalEvt) {
                // Prevent modal from closing
                bvModalEvt.preventDefault();
                // Trigger submit handler
                this.createProject()
            },
            createProject: function() {
                // Exit when the form isn't valid
                if (!this.checkProjectCreateFormValidity()) {
                    return
                }

                this.$http.post('http://localhost:8000/api/project/create',
                    JSON.stringify({'user_id': this.$USER_ID, 'project_name': this.projectForm.projectName,
                        'project_description': this.projectForm.description }),
                    { headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Token': this.$TOKEN_ID }})
                .then(response => {
                    this.$bvToast.toast(response.data['message'], {
                        title: 'Project Creation',
                        toaster: 'b-toaster-top-right',
                        solid: true,
                        variant: 'success',
                        appendToast: false
                    });

                    this.emitGlobalClickEventWhenProjectCreated()
                })
                .catch(e => {
                    this.$bvToast.toast(e.getError().toString(), {
                        title: 'Project Creation',
                        toaster: 'b-toaster-top-right',
                        solid: true,
                        variant: 'danger',
                        appendToast: false
                    });
                });

                // Hide the modal manually
                this.$nextTick(() => {
                    this.$bvModal.hide('modal-new-project')
                })
            },
            checkJobCreateFormValidity() {
                return !(!this.jobForm.jobName.length > 0 || !this.jobForm.crawler.length > 0
                    || !this.jobForm.projectName.length > 0 || !this.jobForm.urlValue.length > 0);
            },
            resetJobCreateModal() {
                this.jobForm.jobName = '';
                this.jobForm.urlValue = [];
            },
            handleJobCreateOk(bvModalEvt) {
                // Prevent modal from closing
                bvModalEvt.preventDefault();
                // Trigger submit handler
                this.createJob()
            },
            createJob: function() {
                // Exit when the form isn't valid
                if (!this.checkJobCreateFormValidity()) {
                    return
                }

                this.$http.post('http://localhost:8000/api/crawl/new',
                    JSON.stringify({'user_id': this.$USER_ID, 'project_name': this.jobForm.projectName,
                        'urls': this.jobForm.urlValue, 'crawler_name': this.jobForm.crawler,
                        'job_name': this.jobForm.jobName, 'schedule_date': this.jobForm.scheduleDate,
                        'schedule_time': this.jobForm.scheduleTime }),
                    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }})
                    .then(response => {
                        this.$bvToast.toast(response.data['message'], {
                            title: 'Crawl Job Schedule',
                            toaster: 'b-toaster-top-right',
                            solid: true,
                            variant: 'success',
                            appendToast: false
                        });

                        this.emitGlobalClickEventWhenJobCreated();
                    })
                    .catch(e => {
                        this.$bvToast.toast(e.getError().toString(), {
                            title: 'Crawl Job Schedule',
                            toaster: 'b-toaster-top-right',
                            solid: true,
                            variant: 'danger',
                            appendToast: false
                        });
                    });

                // Hide the modal manually
                this.$nextTick(() => {
                    this.$bvModal.hide('modal-new-job')
                })
            },
            getProjects() {
                if (this.projectOptions.length === 0) {
                    this.$http.post('http://localhost:8000/api/projects',
                        JSON.stringify({'user_id': this.$USER_ID}),
                        {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
                        .then(response => {
                            var projects = [];
                            response.data.data.forEach(function(obj) {
                                projects.push(obj.project_name)
                            });
                            this.projects = projects;
                            this.projectOptions = projects;
                            if (this.projectOptions.length !== 0) {
                                this.jobForm.projectName = this.projectOptions[projects.length - 1]
                            }
                        })
                        .catch(e => {
                            alert(e.getError().toString())
                        });
                }
            },
            emitGlobalClickEventWhenProjectCreated() {
                EventBus.$emit('project_created', 'data');
            },
            emitGlobalClickEventWhenJobCreated() {
                EventBus.$emit('job_created', 'data');
            },
            loadTextFromFile(ev) {
                const file = ev.target.files[0];
                const reader = new FileReader();
                reader.readAsText(file);
                reader.onload =  evt => {
                    var read = evt.target.result;
                    var links = read.split("\n");
                    let regex = new RegExp(/^(http|https):\/\/[^ "]+$/);
                    var loadedUrls = this.jobForm.urlValue;
                    links.forEach(function(url) {
                        url = url.trim();
                        var isValidUrl = regex.test(url);
                        if (isValidUrl) {
                            loadedUrls.push(url);
                        }

                    });

                    this.jobForm.urlValue = loadedUrls;
                }
            }
        }
    }
</script>

<style lang="scss">
    body {
        font-family: 'Source Sans Pro', sans-serif;
        background-color: #f2f4f7;
    }

    #demo {
        padding-left: 350px;
        transition: 0.3s ease;
    }
    #demo.collapsed {
        padding-left: 50px;
    }
    #demo.onmobile {
        padding-left: 50px;
    }

    .sidebar-overlay {
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        background-color: #000;
        opacity: 0.5;
        z-index: 900;
    }

    /*.demo {*/
        /*padding: 50px;*/
    /*}*/

    .container {
        max-width: 900px;
    }

    pre {
        font-family: Consolas, monospace;
        color: #000;
        background: #fff;
        border-radius: 2px;
        padding: 15px;
        line-height: 1.5;
        overflow: auto;
    }
</style>