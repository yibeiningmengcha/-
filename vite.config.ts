// @ts-nocheck
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  build: {
    sourcemap: 'hidden',
  },
  plugins: [
    react(),
  ],
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
        additionalData: `@import "${path.resolve(__dirname, 'src/styles/variables.less')}"; @import "${path.resolve(__dirname, 'src/styles/mixins.less')}";`,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
})
