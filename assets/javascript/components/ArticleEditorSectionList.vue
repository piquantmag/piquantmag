<template>
    <div>
        <ol class="no-bullet">
            <li
                v-for="(section, index) in sections"
                :id="index"
                :key="index"
            >
                <div class="flex">
                    <div class="fg1">
                        <template v-if="section.type === 'body'">
                            <label
                                class="sr-only"
                                :for="'section-' + (index + 1)"
                            >
                                Section {{ index + 1 }} of {{ sections.length }}
                            </label>
                            <textarea
                                :id="'section-' + (index + 1)"
                                v-model="sections[index].body"
                                placeholder="Section text"
                                ref="section-input"
                            />
                        </template>
                        <template v-if="section.type === 'image'">
                            <media-manager />
                        </template>
                    </div>
                    <div class="mlm mtn fg0">
                        <button
                            @click="deleteSection(index)"
                            :title="'Delete section ' + (index + 1) + ' of ' + sections.length"
                        >
                            <i class="far fa-trash-alt" />
                        </button>
                    </div>
                </div>
            </li>
        </ol>

        <button @click="addSection('body')">
            <span class="fa-layers fa-fw">
                <i class="fas fa-paragraph" />
                <i
                    class="fas fa-plus"
                    data-fa-transform="shrink-10 up-10 right-10"
                />
            </span>
        </button>

        <button @click="addSection('image')">
            <span class="fa-layers fa-fw">
                <i class="fas fa-image" />
                <i
                    class="fas fa-plus"
                    data-fa-transform="shrink-10 up-10 right-10"
                />
            </span>
        </button>
    </div>
</template>

<script>
import MediaManager from '@/components/MediaManager'

export default {
    name: 'ArticleEditorSectionList',
    props: {
        sections: {
            type: Array,
            required: true
        }
    },
    components: {
        MediaManager
    },
    methods: {
        addSection: function (type) {
            let section = null

            if (type === 'body') {
                section = {type: 'body', body: ''}
                this.sections.push(section)
            } else if (type === 'image') {
                section = {type: 'image', image: null}
                this.sections.push(section)
            }
        },
        deleteSection: function (index) {
            this.sections.splice(index, 1)
        }
    }
}
</script>