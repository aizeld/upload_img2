<template>
    <div class="modal fade" id="fieldsModal" tabindex="-1" aria-labelledby="fieldsModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            
              <h5 class="modal-title" id="fieldsModalLabel">Fields Data</h5>
              <div class="ms-auto d-flex align-items-center">
                <button type="button" class="btn btn-primary me-2" @click="selectAll">Select All</button>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>

          </div>
          <div class="modal-body">
            <div v-if="fields">
              <div class="row">
                <div class="col">
                  <ul class="list-group">
                    <li
                      v-for="field in fields"
                      :key="field.id"
                      class="list-group-item"
                      :class="{ 'list-group-item-primary': selectedField === field }"
                      @click="selectField(field)"
                      style="cursor: pointer;"
                      @dblclick="confirmSelection(field)"
                    >
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
            <button type="button" class="btn btn-secondary" @click="terminate" >Отменить</button>
            <button type="button" class="btn btn-primary" :disabled="!selectedField" @click="confirmSelection">Select</button>
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
  const selectedField = ref(null);
  const emit = defineEmits(['fieldSelected']);

  
  watch(() => props.fields, () => {
    if (modalInstance.value) {
      modalInstance.value.show();
    }
  });
  
  const show = async () => {
    if (!modalInstance.value) {
      modalInstance.value = new Modal(document.getElementById('fieldsModal'), {});
    }
    modalInstance.value.show();
  };


  const terminate= async()=>{
    if (modalInstance.value){
      modalInstance.value.hide()
      selectedField.value = null;
    }
  }
  
  const hide = () => {
    if (modalInstance.value) {
      modalInstance.value.hide();
    }
  };
  const selectAll = () => {
  emit('fieldSelected', props.fields); 
  hide(); 
}
  const selectField = (field) => {
    selectedField.value = field;
  };
  
  const confirmSelection = () => {
    if (selectedField.value) {
      hide();
      emit('fieldSelected', selectedField.value);
    }
  };
  
  defineExpose({ show });
  </script>
  
  <style scoped>
  .list-group-item-primary {
    background-color: #cce5ff;
  }
  </style>
  