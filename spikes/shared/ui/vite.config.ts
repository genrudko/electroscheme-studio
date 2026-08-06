import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";

const uiRoot = fileURLToPath(new URL(".", import.meta.url));

export default defineConfig({
  root: uiRoot,
  plugins: [vue()],
  base: "./",
  resolve: {
    alias: {
      "@core": fileURLToPath(new URL("../core/src/index.ts", import.meta.url))
    }
  },
  build: {
    outDir: fileURLToPath(new URL("./dist", import.meta.url)),
    emptyOutDir: true
  }
});
