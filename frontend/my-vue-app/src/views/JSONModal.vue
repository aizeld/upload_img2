<template>
    <!-- Modal overlay -->
    <div class="modal-backdrop" v-if="showModal" @click="closeModal"></div>
  
    <!-- Modal dialog -->
    <div class="modal" tabindex="-1" :class="{ show: showModal }" v-if="showModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">JSON Content</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <textarea v-model="localJsonContent" class="form-control" rows="10"></textarea>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="saveJsonContent">Save</button>
            <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, defineProps, defineEmits } from 'vue';
  
  // Define the props the component will receive
  const props = defineProps({
    jsonContent: {
      type: String,
      required: true,
    },
    showModal: {
      type: Boolean,
      required: true,
    },
  });
  
  // Define the events the component will emit
  const emit = defineEmits(["close", "save"]);
  
  // Local state for JSON content
  const localJsonContent = ref(props.jsonContent);
  

  const saveJsonContent = () => {
    // Emit event to notify parent component of saved content
    emit('save', localJsonContent.value);
    closeModal();
  };
  // Watch for changes in the jsonContent prop and update local state accordingly
  watch(() => props.jsonContent, (newContent) => {
    localJsonContent.value = newContent;
  });
  
  // Function to close the modal and emit the 'close' event
  const closeModal = () => {
    emit("close");
  };
  </script>
  
  <style scoped>
  /* Modal background overlay */
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1040;
  }
  
  /* Modal container */
  .modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1050;
    display: block;
  }
  
  .modal.show {
    display: block;
  }
  
  /* Modal dialog box */
  .modal-dialog {
    max-width: 600px;
    margin: auto;
  }
  
  /* Modal content */
  .modal-content {
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
  }
  
  /* Modal header */
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #f5f5f5;
    border-bottom: 1px solid #dee2e6;
  }
  
  /* Modal title */
  .modal-title {
    margin: 0;
  }
  
  /* Close button */
  .btn-close {
    background: transparent;
    border: none;
    font-size: 1.25rem;
    line-height: 1;
    cursor: pointer;
  }
  
  /* Modal body */
  .modal-body {
    padding: 20px;
  }
  
  /* Modal footer */
  .modal-footer {
    display: flex;
    justify-content: flex-end;
    padding: 10px 20px;
    border-top: 1px solid #dee2e6;
  }
  </style>
  