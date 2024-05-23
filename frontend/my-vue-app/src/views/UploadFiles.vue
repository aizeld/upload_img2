<template>
    <div>
      <form @submit.prevent="handleSubmit" class="form-container">
        <label for="company_id">Company ID:</label>
        <input
          type="text"
          id="company_id"
          v-model="companyId"
          placeholder="Enter company ID"
          required
        />
        <button type="button" @click="open()">Выбрать файлы</button>
        <button type="button" :disabled="!files" @click="reset()">Отменить</button>
        <button type="submit">Отправить</button>
      </form>
      <div v-if="files" class="files-container">
        <p>
          Вы выбрали:
          <b>{{ `${files.length} ${files.length === 1 ? "file" : "files"}` }}</b>
        </p>
        <ul>
          <li v-for="file of files" :key="file.name">
            {{ file.name }}
          </li>
        </ul>
      </div>
      <div v-if="uploadResponse !== null" class="upload-response">
        <p v-if="uploadResponse.status_code === 200" class="success">Успешно отправлено!</p>
        <p v-else class="error">Ошибка {{ uploadResponse.error.error }}</p>
        <p>Статус код : {{ uploadResponse.status_code }}</p>
      </div>
    </div>
  </template>
  <script setup>
  import  axios from "axios";
  import { ref } from "vue";
  import { useFileDialog } from "@vueuse/core";
  
  const { files, open, reset } = useFileDialog();
  
  const companyId = ref("");
  const uploadResponse = ref(null);
  
  const handleSubmit = async () => {
  
    if (!files) { // Check if files is null or no files selected
      uploadResponse.value = { status_code: 400, eror: "Нет файлов" }; // Set status code 400 for no file selected
      return;
    }
    const formData = new FormData();
  
    for (let i = 0; i < files.value.length; i++) {
      formData.append("files", files.value[i]);
    }
    formData.append("company_id", companyId.value);
  
    try {
      const response = await axios.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      uploadResponse.value = {
        status_code: response.status_code,
        data: response.data,
      };
      files.value = [];
    } catch (error) {
      if (error.response && error.response.data) {
        uploadResponse.value = {
          status_code: error.response.status,
          error: error.response.data,
        };
      } else {
        uploadResponse.value = { status_code: 500, error: "Upload failed" };
      }
    }
  };
  </script>
  <style>
  
  .form-container {
    margin-bottom: 20px;
  }
  
  .files-container {
    margin-bottom: 20px;
  }
  
  
  .error {
    color: red;
    animation: shake 0.5s ease-in-out;
  }
  
  @keyframes shake {
    0% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    50% { transform: translateX(5px); }
    75% { transform: translateX(-5px); }
    100% { transform: translateX(0); }
  }
  </style>