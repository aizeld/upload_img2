<template>

  <div class="container my-5">
    <form @submit.prevent="handleSubmit" class="form-container mb-4">
      <div class="mb-3">
      <label for="company_id">Enter Company ID</label> 
      <input type="text" id="company_id" v-model="companyId" class="form-control" placeholder="Введите ID компании" requiered>
      </div>
  
      <div class="mm-3">
        <button type="button" class="btn btn-primary me-2" @click="open()">Выбрать Файлы</button>
        <button type="button" class="btn btn-primary me-2" @click="openFieldsModal()">Выбрать Поля Компании</button>
        <button type="button" class="btn btn-secondary me-2" @disabled="!files" @click="reset()">Отменить</button>
        <button type="submit" class="btn btn-secondary me-2" @disabled="!files">Отправить</button>
      </div>    
  
    </form>
  
  
    
  
      <div v-if="selectedField" class="mb-4">Field ID: {{selectedField.id}}</div>
  
  
      <div v-if="pairedfiles" class="files-container mb-3">
        <p>Вы выбрали <b>{{`${pairedfiles.length} ${pairedfiles.length === 1 ? "Пару" : "Пар"} `}}</b></p> 
  
        <ul class="list-group">
  
          <li 
          v-for="(pair, index) in pairedfiles"  
          :key="index" 
          class="list-group-item d-flex justify-content-between align-items-center">
  
          {{pair.png.name}}
          <div class="loading-bar"
          :class="[uploadResponse && uploadResponse.status_code === 201 ? 'upload-complete' : (uploadResponse && uploadResponse.status_code !== 201 ? 'upload-error' : '')]">
        </div>
        
      
          <label >JSON {{pair.json.name}}</label>
          
          <button type="button" class="btn btn-info btn-sm" @click="showJson(pair.jsonContent)">Show JSON</button>
  
          </li> 
  
        </ul>
      </div>
  
  
      <div v-if="uploadResponse !== null" class="upload-response">
        <p v-if="uploadResponse.status_code === 201" class="alert alert-success">Успешно отправлено!</p>
        <p v-else class="alert alert-danger">Ошибка {{ uploadResponse.message }}</p>
        <p>Статус код : {{ uploadResponse.status_code }}</p>
      </div>
      <FieldsModal :fields="fields" ref="fieldsModal" @fieldSelected="handleFieldsSelected" />
      <JSONModal v-if="jsonModalVisible" :jsonContent="jsonModalContent" :showModal="jsonModalVisible" @close="jsonModalVisible = false" @save="saveJsonContent" />
  
  </div>
  
  
  </template>    
  
  
  <script setup>
  
    import axios from 'axios';
    import {ref, watch, computed} from "vue"
    import { useFileDialog } from '@vueuse/core';
    import FieldsModal from './FieldsModal.vue';  
    import JSONModal from './JSONModal.vue';
    const {files, open, reset} = useFileDialog();
    const companyId = ref("");
    const lastFetchedCompanyId = ref(null)
    const uploadResponse = ref(null)
  
    const fields = ref(null);
    const fieldsModal = ref(null);
    const selectedField = ref(null);
  
    const pairedfiles = ref([]);
  
    const jsonModalVisible = ref(false);
  const jsonModalContent = ref("");
  
  
    watch(files, async ()=>{
      uploadResponse.value = null;
  
      if (files.value.length > 0) {
        pairedfiles.value = await pairFiles(files.value);
        console.log("paired files", pairedfiles.value)
      }
  
    })
    
  
    const pairFiles = async (files) => {
      const fileArray = Array.from(files);
      const pairs = {}
  
      fileArray.forEach(file => {
        const basename = file.name.split(".").slice(0, -1).join(".");
        
        if(file.name.toLowerCase().endsWith(".png")){
          if(!pairs[basename]){
            pairs[basename] = {};
          }
          pairs[basename].png = file;
        }
  
        else if(file.name.toLowerCase().endsWith(".json")){
          if(!pairs[basename]){
            pairs[basename] = {};
          }
          const jsonBasename = basename.endsWith("_meta") ? basename.substring(0, basename.length - 5) : basename;
  
          if (!pairs[jsonBasename]){
            pairs[jsonBasename] = {};
        }
          pairs[jsonBasename].json = file;
          
          readFileContent(file).then(content => {
            pairs[jsonBasename].jsonContent = content;
          }).catch(() => {
            pairs[jsonBasename].jsonContent = "Failed to read JSON content";
          });
      }}
    
    );
    const paired = Object.values(pairs).filter(pair => pair.png && pair.json)
  
    return paired;
  
    }
  
    const readFileContent = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (event) => {
        resolve(event.target.result);
      };
      reader.onerror = (error) => {
        reject(error);
      };
      reader.readAsText(file);
    });
  };
  
  
  
    const handleSubmit = async () => {
  
     if(!pairedfiles.value){
      uploadResponse.value = {message : "Нет пар файлов", status_code : 400}
      return;
     }
  
     if(!companyId.value){
      uploadResponse.value = {message: "Не выбран company_id", status_code : 400}
      return;
    }
    
     if(!selectedField.value){
      uploadResponse.value = {message: "Не выбраны поля", status_code : 400}
      return;
    }
  
  
    uploadResponse.value = null;
    const formData = new FormData();
    let jsonContents = [];
      pairedfiles.value.forEach(pair => {
         formData.append("files", pair.png);
         jsonContents.push(pair.jsonContent);    
         });
     
  
  
         formData.append("json", JSON.stringify(jsonContents));
         console.log(formData)
       formData.append("company_id", companyId.value);
       formData.append("context", JSON.stringify({ "field_id": selectedField.value.id }));
     
       formData.append("shape", JSON.stringify({
         "type": selectedField.value.shape_gis.type,
         "coordinates": selectedField.value.shape_gis.coordinates
       }));
     
       try {
         const response = await axios.post("/upload", formData, {
           headers: {
             "Content-Type": "multipart/form-data",
           },
         });
     
         uploadResponse.value = {
           status_code: response.status,
           data: response.message,
         };
         files.value = [];
       } catch (error) {
         if (error.response && error.response.data) {
           uploadResponse.value = {
             status_code: error.response.status || 500,
             message: error.response.message || "Не удалось отправить файл",
           };
         } else {
           uploadResponse.value = { status_code: 500, error: "Не удалось отправить файл" };
         }
       }
  
    }
  
  
  
  
    const fetchFields = async() =>{
      try{
        const response = await axios.get("/get_fields", {
          headers: { "Content-Type": "application/json", },
          params: {
            company_id: companyId.value,
          },
        });
        
        if (response.status === 200){
          fields.value = response.data.data;
          lastFetchedCompanyId.value = companyId.value;
        }
        else{
          fields.value = [];
          uploadResponse = {message: "Can't fetch fields", status_code: response.status}
        }
      }catch(error){
        fields.value = [];
          uploadResponse = {message: "Can't fetch fields", status_code: response.status}
      }
    }
  
    const showJson = (jsonContent) => {
    jsonModalContent.value = jsonContent;
    jsonModalVisible.value = true;
  };
    const openFieldsModal = async()=>{
      if (companyId.value !== lastFetchedCompanyId.value) {
        // Fetch fields only if company ID has changed since the last fetch, it saves so much resourcec
        await fetchFields();
      }
      fieldsModal.value.show();
    }
    const handleFieldsSelected = async(field) =>{
      selectedField.value = field
      console.log(selectedField.value)
    }
  
  
    const saveJsonContent = (editedjson) => {
      pairedfiles.value.find(pair => pair.jsonContent === jsonModalContent.value).jsonContent = editedjson
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