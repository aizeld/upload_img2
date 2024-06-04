<template>
    <div class="container my-5">
      <form @submit.prevent="handleSubmit" class="form-container mb-4">
        <div class="mb-3">
          <label for="company_id" class="form-label">Company ID:</label>
          <input type="text" id="company_id" v-model="companyId" class="form-control" placeholder="Enter company ID"
            required />
        </div>
        <div class="mb-3">
          <button type="button" class="btn btn-primary me-2" @click="open()">Выбрать файлы</button>
          <button type="button" class="btn btn-primary me-2" @click="openFieldsModal">Посмотреть Поля</button>
          <button type="button" class="btn btn-secondary me-2" :disabled="!files" @click="reset()">Отменить</button>
          <button type="submit" class="btn btn-success me-2">Отправить</button>
        </div>
      </form>
  
      <div v-if="files" class="files-container mb-4">
        <p>
          Вы выбрали:
          <b>{{ `${files.length} ${files.length === 1 ? "Файл" : "Файлов"}` }}</b>
        </p>
        <ul class="list-group">
          <li v-for="file of files" :key="file.name"
            class="list-group-item d-flex justify-content-between align-items-center">
            {{ file.name }}
            <div class="loading-bar"
              :class="[uploadResponse && uploadResponse.status_code === 201 ? 'upload-complete' : (uploadResponse && uploadResponse.status_code !== 201 ? 'upload-error' : '')]">
            </div>
  
          </li>
        </ul>
      </div>
  
      <div v-if="uploadResponse !== null" class="upload-response">
        <p v-if="uploadResponse.status_code === 201" class="alert alert-success">Успешно отправлено!</p>
        <p v-else class="alert alert-danger">Ошибка {{ uploadResponse.error }}</p>
        <p>Статус код : {{ uploadResponse.status_code }}</p>
      </div>
  
      <FieldsModal :fields="fields" ref="fieldsModal" @fieldSelected="handleFieldsSelected" />
    </div>
  </template>
  <!-- https://blog.openreplay.com/vue-custom-drag-and-drop-file-uploading/
     -->
  
  
  <script setup>
  import axios from "axios";
  import { ref, watch } from "vue";
  import { useFileDialog } from "@vueuse/core";
  import FieldsModal from './FieldsModal.vue';
  const { files, open, reset } = useFileDialog();
  const lastFetchedCompanyId = ref(null);
  const companyId = ref("");
  const uploadResponse = ref(null);
  const fields = ref([]);
  const fieldsModal = ref(null);
  const selectedField = ref(null);
  
  watch(files, () => {
    uploadResponse.value = null;
  });
  
  const handleSubmit = async () => {
    if (!files.value) { // Check if files is null or no files selected
  
      uploadResponse.value = { status_code: 400, error: "Нет файлов" };
      return;
    }
    uploadResponse.value = null;
  
  
    const formData = new FormData();
  
    for (let i = 0; i < files.value.length; i++) {
      formData.append("files", files.value[i]);
    }
    formData.append("company_id", companyId.value);
    formData.append("context", JSON.stringify({"field_id" : selectedField.value.id}))
 
    formData.append("shape", JSON.stringify({"type": selectedField.value.shape_gis.type,
                             "coordinates": selectedField.value.shape_gis.coordinates}))
    
    
    try {
      const response = await axios.post("/upload_test", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      console.log(response);
  
  
      uploadResponse.value = {
        status_code: response.status,
        data: response.message,
      };
      files.value = [];
    } catch (error) {
      if (error.response && error.response.data) {
        uploadResponse.value = {
          status_code: error.response.status || 500,
          error: error.response.message || "Не удалось отправить файл",
        };
      } else {
        uploadResponse.value = { status_code: 500, error: "Не удалось отправить файл" };
      }
    }
  };
  
  
  const fetchFields = async () => {
    try {
      const response = await axios.get("/get_fields", {
        headers: {
          "Content-Type": "application/json",
        },
        params: { company_id: companyId.value },
      });
      if (response.status === 200) {
        fields.value = response.data.data;
        lastFetchedCompanyId.value = companyId.value;
      } else {
        fields.value = [];
        alert("Failed to fetch fields");
      }
    } catch (error) {
      fields.value = [];
      alert("Error fetching fields");
    }
  };
  
  const openFieldsModal = async () => {
    if (companyId.value !== lastFetchedCompanyId.value) {
      // Fetch fields only if company ID has changed since the last fetch
      await fetchFields();
    }
    fieldsModal.value.show();
  };
  
  const handleFieldsSelected = async(field) =>{
    selectedField.value = field
    console.log(selectedField.value)
  }
  
  
  
  
  </script>
  
  
  <style>
  .form-container {
    margin-bottom: 20px;
  }
  
  .files-container {
    margin-bottom: 20px;
  }
  
  .success {
    color: #28a745;
  }
  
  .error {
    color: red;
    animation: shake 0.5s ease-in-out;
  }
  
  @keyframes shake {
    0% {
      transform: translateX(0);
    }
  
    25% {
      transform: translateX(-5px);
    }
  
    50% {
      transform: translateX(5px);
    }
  
    75% {
      transform: translateX(-5px);
    }
  
    100% {
      transform: translateX(0);
    }
  }
  
  .loading-bar {
    width: 0%;
    height: 5px;
    background-color: #666;
    border-radius: 2px;
    transition: width 0.5s ease-in-out;
    width: 40px;
    max-width: 150px;
  }
  
  .upload-complete {
    width: 40%;
    background-color: #4CAF50;
  
  }
  
  .upload-error {
    width: 10%;
    height: 5px;
    background-color: #ff7b07;
    border-radius: 2px;
    transition: width 0.5s ease-in-out;
  }
  
  .loading-bar.hide {
    width: 0%;
    transition: width 0.1s ease-in-out;
    /* Fast disappearance */
  }
  </style>