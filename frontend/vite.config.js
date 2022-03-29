import { defineConfig } from "vite"
import vue from '@vitejs/plugin-vue'




export default defineConfig({
  plugins: [vue()],
  css: 
    { preprocessorOptions:
      { css: 
        { 
          charset: false 
        } 
      } 
    },
  build: {
      assetsInlineLimit: '2048' // 2kb
  },
  server: {
    host: "0.0.0.0",
    proxy: {
      "/api": {
        target: "http://localhost:8002",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});