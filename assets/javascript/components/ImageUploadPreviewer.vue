<template>
    <div class="image-previewer">
        <label :for="inputId">
            <template v-if="imageSrc">Change image</template>
            <template v-else>Upload image</template>
        </label>
        <input
            :id="inputId"
            ref="file"
            @change="handleFileChange"
            type="file"
            accept="image/*"
        >
        <img
            v-if="imageSrc"
            :src="imageSrc"
        >
    </div>
</template>

<script>
export default {
    name: 'ImageUploadPreviewer',
    props: {
        inputId: {
            type: String,
            default: 'image-previewer'
        }
    },
    data: function () {
        return {
            imageSrc: null
        }
    },
    methods: {
        handleFileChange() {
            let imageReader = new FileReader(),
                upload = null;

            imageReader.addEventListener('load', () => {
                this.imageSrc = imageReader.result
            }, false)

            upload = this.$refs.file.files[0]

            if (upload) {
                imageReader.readAsDataURL(upload)
            } else if (this.imageSrc) {
                this.imageSrc = null
            }
        }
    }
}
</script>