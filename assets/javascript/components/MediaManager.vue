<template>
    <div class="media-manager">
        <div class="media-manager__toggle">
            <button @click="isOpen = !isOpen">
                <i class="far fa-images" />
            </button>
        </div>
        <transition
            name="pane"
            @before-enter="fetchImages"
        >
            <div
                v-show="isOpen"
                class="media-manager__pane"
                tabindex="0"
            >
                <image-upload-previewer
                    :input-id="'image-previewer-' + (this.$vnode.key + 1)"
                />
                <div v-if="imagesLoading">Loading...</div>
                <div v-else>
                    <div v-if="images.length">
                        <ul class="inline-list">
                            <li
                                v-for="(image, index) in images"
                                :key="index"
                            >
                                <lazy-loading-image
                                    class="media-manager__pane__image"
                                    :src="image.image"
                                    :alt="image.alt_text"
                                />
                            </li>
                        </ul>
                    </div>
                    <div v-else>There are no images yet!</div>
                    <div v-show="error">{{ error }}</div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
import axios from 'axios'
import LazyLoadingImage from '@/components/LazyLoadingImage'
import ImageUploadPreviewer from '@/components/ImageUploadPreviewer'

export default {
    name: 'MediaManager',
    components: {
        LazyLoadingImage,
        ImageUploadPreviewer
    },
    data() {
        return {
            images: [],
            imagesLoading: false,
            error: null,
            isOpen: false
        }
    },
    methods: {
        fetchImages() {
            if (!this.images.length) {
                this.imagesLoading = true

                axios.get(
                    '/api/images/'
                ).then((response) => {
                    this.imagesLoading = false
                    this.images = response.data
                }).catch((err) => {
                    this.error = `Could not load images: ${err}`
                })
            }
        }
    }
}
</script>

<style lang="scss" scoped>
    @import '../../stylesheets/settings';

    .media-manager__pane {
        background: #EEEEEE;
        position: absolute;
        z-index: 100;
        padding: $base-spacing * 5;
        box-shadow: 5px 5px 10px -5px rgba(0, 0, 0, 0.25);

        ul {
            display: flex;

            li {
                height: 200px;
                align-items: center;

                &:not(:first-child):not(:last-child) img {
                    margin: 0 $base-spacing;
                }
            }
        }
    }

    .media-manager__pane__image {
        max-width: 200px;
        max-height: 200px;
        margin: 0;
    }

    .pane-enter-active, .pane-leave-active {
        transition: opacity 500ms;
    }

    .pane-enter, .pane-leave-to {
        opacity: 0;
    }
</style>