<template>
    <div
        id="editor"
        v-cloak
    >
        <label for="article-title-input">Title</label>
        <input
            id="article-title-input"
            type="text"
            v-model="article.title"
            placeholder="Article title"
        >

        <label for="article-synopsis-input">Synopsis</label>
        <textarea
            id="article-synopsis-input"
            v-model="article.synopsis"
            placeholder="Article synopsis"
        />

        <article-editor-section-list :sections="article.components" />
    </div>
</template>

<script>
import ArticleEditorSectionList from '@/components/ArticleEditorSectionList'

export default {
    name: 'ArticleEditor',
    components: {
        ArticleEditorSectionList
    },
    props: {
        article: {
            type: Object,
            required: true
        }
    }
}
</script>