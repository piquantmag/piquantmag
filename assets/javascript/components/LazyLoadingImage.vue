<template>
    <img
        :src="src"
        :alt="alt"
        v-show="isLoaded"
        @load="loaded"
    >
</template>

<script>
export default {
    name: 'LazyLoadingImage',
    props: {
        src: {
            type: String,
            required: true
        },
        alt: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            isLoaded: false
        }
    },
    methods: {
        loaded() {
            this.isLoaded = true
        }
    }
}
</script>