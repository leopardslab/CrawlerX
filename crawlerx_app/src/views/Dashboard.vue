<template>
    <div
            id="demo"
            :class="[{'collapsed' : collapsed}, {'onmobile' : isOnMobile}]"
    >
        <div class="">
            <md-toolbar md-get-palette-color="red" md-elevation="1">
                <h3 class="md-title" style="flex: 1"><b>CrawlerX</b> - Open-Source Crawling Platform</h3>
                <md-button>Refresh</md-button>
                <md-button class="md-primary" @click="logout">Logout</md-button>
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
    </div>

</template>

<script>
    const separator = {
        template: `<hr style="border-color: rgba(0, 0, 0, 0.1); margin: 20px;">`
    };

    // @ is an alias to /src
    // import HelloWorld from '@/components/HelloWorld.vue'
    import firebase from 'firebase'

    export default {
        name: 'Home',
        components: {
            // HelloWorld,
        },
        data() {
            return {
                menu: [
                    {
                        header: true,
                        title: 'Configurations',
                        hiddenOnCollapse: true
                    },
                    {
                        href: '/',
                        title: 'Dashboard',
                        icon: 'fa fa-download'
                    },
                    {
                        header: true,
                        title: 'Features',
                        hiddenOnCollapse: true
                    },
                    {
                        href: '/projects',
                        title: 'Projects',
                        icon: 'fa fa-cogs'
                    },
                    {
                        href: '/jobs',
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
                        href: '/analysis',
                        title: 'ELK Analysis',
                        icon: 'fa fa-bell'
                    }
                ],
                collapsed: false,
                selectedTheme: 'Default theme',
                isOnMobile: false
            }
        },
        mounted() {
            this.onResize()
            window.addEventListener('resize', this.onResize)
        },
        methods: {
            logout: function () {
                firebase.auth().signOut().then(() => {
                    this.$router.replace('login');
                })
            },
            onToggleCollapse(collapsed) {
                console.log(collapsed)
                this.collapsed = collapsed
            },
            onItemClick(event, item) {
                console.log('onItemClick')
                console.log(event)
                console.log(item)
            },
            onResize() {
                if (window.innerWidth <= 767) {
                    this.isOnMobile = true
                    this.collapsed = true
                } else {
                    this.isOnMobile = false
                    this.collapsed = false
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