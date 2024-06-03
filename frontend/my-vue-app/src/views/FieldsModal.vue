<template>
    <div class="modal fade" id="fieldsModal" tabindex="-1" aria-labelledby="fieldsModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="fieldsModalLabel">Fields Data</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="fields">
              <div class="row">
                <div class="col">
                  <ul class="list-group">
                    <li v-for="field in fields" :key="field.id" class="list-group-item">
                      <p class="mb-1"><strong>ID:</strong> {{ field.id }}</p>                
                      <p class="mb-1"><strong>Title:</strong> {{ field.title }}</p>
                      <p class="mb-1"><strong>Type:</strong> {{ field.field_type }}</p>
                      <p class="mb-1"><strong>Cluster:</strong> {{ field.cluster }}</p>
                      <p class="mb-1"><strong>Legal Entity:</strong> {{ field.legal_entity }}</p>
                      <p class="mb-1"><strong>Document Area:</strong> {{ field.document_area }}</p>
                      <p class="mb-1"><strong>Fact Area:</strong> {{ field.fact_area }}</p>
                      <p class="mb-1"><strong>Soil Type:</strong> {{ field.soil_type }}</p>
                      <p class="mb-1"><strong>Quality:</strong> {{ field.quality }}</p>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div v-else>
              <p>No fields data available.</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="hide">Close</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue';
  import { Modal } from 'bootstrap';
  
  const props = defineProps(['fields']);
  const modalInstance = ref(null);
  
  watch(() => props.fields, () => {
    if (modalInstance.value) {
      modalInstance.value.show();
    }
  });
  
  const show = () => {
    if (!modalInstance.value) {
      modalInstance.value = new Modal(document.getElementById('fieldsModal'), {});
    }
    modalInstance.value.show();
  };
  
  const hide = () => {
    if (modalInstance.value) {
      modalInstance.value.hide();
    }
  };
  
  defineExpose({ show });
  </script>
  
  <style scoped>
  </style>
  