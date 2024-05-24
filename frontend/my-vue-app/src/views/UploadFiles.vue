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
          <b>{{ `${files.length} ${files.length === 1 ? "Файл" : "Файлов"}` }}</b>
        </p>
        <ul>

          <li v-for="file of files" :key="file.name">
            {{ file.name }}
            <div class="loading-bar" :class="[uploadResponse && uploadResponse.status_code === 201 ? 'upload-complete' : (uploadResponse && uploadResponse.status_code !== 201 ? 'upload-error' : '')]"></div>
          </li>
        </ul>
      </div>



      <!-- <div v-if="files" class="files-container">
        <p>
          You have selected:
          <b>{{ `${files.length} ${files.length === 1 ? "file" : "files"}` }}</b>
        </p>
        <ul>
          <li v-for="(file, index) in files" :key="file.name">
            {{ file.name }}
            <div class="loading-bar" :class="{ 'upload-complete': uploadResponses[index] && uploadResponses[index].status_code === 201 }"></div>
          </li>
        </ul>
      </div> -->



      <div v-if="uploadResponse !== null" class="upload-response">
        <p v-if="uploadResponse.status_code === 201" class="success">Успешно отправлено!</p>
        <p v-else class="error">Ошибка {{ uploadResponse.error }}</p>
        <p>Статус код : {{ uploadResponse.status_code }}</p>
      </div>
    </div>
  </template>
  <script setup>
  import  axios from "axios";
  import { ref, watch } from "vue";
  import { useFileDialog } from "@vueuse/core";
  
  const { files, open, reset } = useFileDialog();
  
  const companyId = ref("");
  const uploadResponse = ref(null);
  


  watch(files, () => {
  // Clear the upload response when new files are selected
  uploadResponse.value = null;
});

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
    0% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    50% { transform: translateX(5px); }
    75% { transform: translateX(-5px); }
    100% { transform: translateX(0); }
  }

.loading-bar {
  width: 0%;
  height: 5px;
  background-color: #666;
  border-radius: 2px;
  transition: width 0.5s ease-in-out;
  width: 40px;
}

.upload-complete {
  width: 40%;
  background-color: #4CAF50;
}

.upload-error {
  width: 20%;
  height: 5px;
  background-color: #ff7b07;
  border-radius: 2px;
  transition: width 0.5s ease-in-out;
}
  </style>