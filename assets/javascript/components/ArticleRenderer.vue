<template>
    <div
        id="rendered"
        v-cloak
    >
        <h2
            class="piquant"
            id="article-title">{{ article.title }}
        </h2>

        <template v-for="(section, index) in article.components">
            <body-component
                :body="section.body"
                v-if="section.type === 'body'"
                :key="index"
            />
        </template>
    </div>
</template>

<script>
import ArticleRendererBodyComponent from './ArticleRendererBodyComponent'

export default {
    name: 'ArticleRenderer',
    props: {
        article: {
            type: Object,
            required: true
        }
    },
    components: {
        'body-component': ArticleRendererBodyComponent
    }
}
</script>