<template>
    <div
        v-if="articleLoaded"
        id="article-manager"
    >
        <article-editor :article="article" />
        <article-renderer :article="article" />
    </div>
    <div v-else>Loading...</div>
</template>

<script>
import axios from 'axios'
import ArticleEditor from '@/components/ArticleEditor'
import ArticleRenderer from '@/components/ArticleRenderer'

export default {
    name: 'Authorer',
    components: {
        ArticleEditor,
        ArticleRenderer,
    },
    props: {
        articleId: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            article: {
                title: '',
                synopsis: '',
                components: []
            },
            articleLoaded: false
        }
    },
    created() {
        if (this.articleId >= 0) {
            this.fetchArticle()
        } else {
            this.articleLoaded = true
        }
    },
    methods: {
        fetchArticle() {
            axios.get(`/api/articles/${this.articleId}/`).then(response => {
                this.article = response.data
                this.articleLoaded = true
            })
        }
    }
}
</script>