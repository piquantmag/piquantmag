/* global articleId */

import Vue from 'vue'
import Authorer from '@/Authorer'

new Vue({
    el: '#article-manager',
    components: {
        Authorer
    },
    data: {
        articleId: articleId
    },
    template: '<Authorer :articleId="articleId" />'
})