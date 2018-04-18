<template>
    <span v-html="renderedBody" />
</template>

<script>
import marked from 'marked'

export default {
    name: 'ArticleRendererBodyComponent',
    props: {
        body: {
            type: String,
            default: ''
        }
    },
    computed: {
        renderedBody: function () {
            return marked(this.body)
        }
    }
}
</script>