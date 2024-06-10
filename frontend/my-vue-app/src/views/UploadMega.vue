<template>
    <div class="container my-5">
      <form @submit.prevent="handleSubmit" class="form-container mb-4">
        <div class="mb-3">
          <label for="company_id" class="form-label">Company ID:</label>
          <input type="text" id="company_id" v-model="companyId" class="form-control" placeholder="Enter company ID"
            required />
        </div>
        <div class="mb-3">
          <button type="button" class="btn btn-primary me-2" @click="open()">Выбрать снимки</button>
          <button type="button" class="btn btn-primary me-2" @click="openFieldsModal">Выбрать Поля</button>
          <button type="button" class="btn btn-secondary me-2" :disabled="!files" @click="reset()">Отменить</button>
          <button type="submit" class="btn btn-success me-2" :disabled="!files">Отправить</button>
        </div>
        <input type="file" ref="fileInput" id="file_input" accept=".json" style="display: none" @change="handleFileUpload">

      </form>
      
      <div v-if="selectedField" class="mb-4">Field ID: {{selectedField.id}}</div>

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
            <button type="button" class="btn btn-primary me-2" @click="openFileInput()">Выгрузить json</button>
            <div class="mb-3">
                <label for="json_data" class="form-label">JSON Data:</label>
                <textarea id="json_data" v-model="jsonData" class="form-control" placeholder="Enter JSON data" required></textarea>
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
  const jsonData = ref("");


  watch(files, () => {
    uploadResponse.value = null;
  });
  




  const openFileInput = () => {
  // Trigger file input click 
  const fileInput = document.getElementById("file_input");
  fileInput.click();
};

const handleFileUpload = (event) => {
  const uploadedFiles = event.target.files;
  // Update files value with uploaded files
  files.value = uploadedFiles;
  const jsonFile = Array.from(uploadedFiles).find(file => file.type === "application/json");
  if (jsonFile) {
    uploadResponse.value = null;
    const reader = new FileReader();
    reader.onload = (e) => {
      jsonData.value = e.target.result;
    };
    reader.readAsText(jsonFile);
    
  }else{
    uploadResponse.value = {status_code : 400, error: "Неправильный json"}
  }
 
};





  const handleSubmit = async () => {

    console.log(jsonData.value)
    if (!files.value) { // Check if files is null or no files selected
  
      uploadResponse.value = { status_code: 400, error: "Нет файлов" };
      return;
    }

    if (!selectedField.value) {
      uploadResponse.value = {status_code: 400, error: "Выберите поля"}
    return;
    }

    if(!jsonData.value){
      uploadResponse.value = {status_code: 400, error: "Нет json"}
      return;
    }
  
    
    

    uploadResponse.value = null;
    
    
    const formData = new FormData();
    
    for (let i = 0; i < files.value.length; i++) {
      formData.append("files", files.value[i]);
    }


    let parsedJsonData;
  try {
    parsedJsonData = JSON.parse(jsonData.value);
  } catch (error) {
    uploadResponse.value = { status_code: 400, error: "Неправильный формат JSON" };
    return;
  }

    for (const key in parsedJsonData) {
    if (parsedJsonData.hasOwnProperty(key)) {
      const value = parsedJsonData[key];
      if (typeof value === "object") {
        // If the value is an object, we need to stringify it
        formData.append(key, JSON.stringify(value));
      } else {
        formData.append(key, value);
      }
    }
  }

    formData.append("company_id", companyId.value);
    formData.append("context", JSON.stringify({"field_id" : selectedField.value.id}))
    
    console.log(formData)

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
      // Fetch fields only if company ID has changed since the last fetch, it saves so much resourcec
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