// vite.config.js
import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "file:///home/nuoai/dev/WEB-sydney-rental-hub/node_modules/vite/dist/node/index.js";
import vue from "file:///home/nuoai/dev/WEB-sydney-rental-hub/node_modules/@vitejs/plugin-vue/dist/index.js";
import vueDevTools from "file:///home/nuoai/dev/WEB-sydney-rental-hub/node_modules/vite-plugin-vue-devtools/dist/vite.js";
import path from "node:path";
var __vite_injected_original_dirname = "/home/nuoai/dev/WEB-sydney-rental-hub/apps/web";
var __vite_injected_original_import_meta_url = "file:///home/nuoai/dev/WEB-sydney-rental-hub/apps/web/vite.config.js";
var dirname = typeof __vite_injected_original_dirname !== "undefined" ? __vite_injected_original_dirname : path.dirname(fileURLToPath(__vite_injected_original_import_meta_url));
var isStorybook = process.env.STORYBOOK === "true";
var viteInspectCompatPatch = {
  name: "vite-plugin-inspect-compat-patch",
  enforce: "pre",
  configureServer(server) {
    if (server && server.environments == null) {
      server.environments = {};
    }
  }
};
var enableVueDevTools = process.env.ENABLE_VUE_DEVTOOLS === "true";
var vite_config_default = defineConfig(async () => {
  const plugins = [vue()];
  if (!isStorybook && enableVueDevTools) {
    plugins.unshift(viteInspectCompatPatch);
    plugins.push(vueDevTools());
  }
  let testConfig;
  if (isStorybook) {
    const { storybookTest } = await import("@storybook/addon-vitest/vitest-plugin");
    testConfig = {
      projects: [
        {
          extends: true,
          plugins: [
            storybookTest({
              configDir: path.join(dirname, ".storybook")
            })
          ],
          test: {
            name: "storybook",
            browser: {
              enabled: true,
              headless: true,
              provider: "playwright",
              instances: [
                {
                  browser: "chromium"
                }
              ]
            },
            setupFiles: [".storybook/vitest.setup.js"]
          }
        }
      ]
    };
  }
  return {
    plugins,
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", __vite_injected_original_import_meta_url))
      }
    },
    server: {
      // 固定端口，避免 Google Maps API 限制问题
      port: 5174,
      strictPort: true,
      // 如果端口被占用则报错，而不是尝试下一个端口
      host: true,
      // 监听所有地址
      // 允许通过 ngrok 访问（解决 403 Forbidden / Host 校验）
      // 也可设置为 true 完全放开（仅开发环境使用）：
      // allowedHosts: true,
      allowedHosts: [".ngrok-free.app"],
      // 可选：若需要稳定 HMR，通过 ngrok 的 wss 连接（演示可不配置）
      // hmr: {
      //   host: 'YOUR_SUBDOMAIN.ngrok-free.app', // 替换为实际 ngrok 子域名
      //   protocol: 'wss',
      //   clientPort: 443,
      // },
      proxy: {
        "/api": {
          // 本地后端（通过 Vite 代理转发），更稳：统一指向 localhost
          target: "http://localhost:8000",
          changeOrigin: true,
          secure: false
        }
      }
    },
    // 仅在 Storybook 环境下加载测试配置
    test: testConfig
  };
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvaG9tZS9udW9haS9kZXYvV0VCLXN5ZG5leS1yZW50YWwtaHViL2FwcHMvd2ViXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvaG9tZS9udW9haS9kZXYvV0VCLXN5ZG5leS1yZW50YWwtaHViL2FwcHMvd2ViL3ZpdGUuY29uZmlnLmpzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9ob21lL251b2FpL2Rldi9XRUItc3lkbmV5LXJlbnRhbC1odWIvYXBwcy93ZWIvdml0ZS5jb25maWcuanNcIjsvLy8gPHJlZmVyZW5jZSB0eXBlcz1cInZpdGVzdC9jb25maWdcIiAvPlxuaW1wb3J0IHsgZmlsZVVSTFRvUGF0aCwgVVJMIH0gZnJvbSAnbm9kZTp1cmwnXG5pbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJ1xuaW1wb3J0IHZ1ZSBmcm9tICdAdml0ZWpzL3BsdWdpbi12dWUnXG5pbXBvcnQgdnVlRGV2VG9vbHMgZnJvbSAndml0ZS1wbHVnaW4tdnVlLWRldnRvb2xzJ1xuXG4vLyBodHRwczovL3ZpdGUuZGV2L2NvbmZpZy9cbmltcG9ydCBwYXRoIGZyb20gJ25vZGU6cGF0aCdcbmNvbnN0IGRpcm5hbWUgPVxuICB0eXBlb2YgX19kaXJuYW1lICE9PSAndW5kZWZpbmVkJyA/IF9fZGlybmFtZSA6IHBhdGguZGlybmFtZShmaWxlVVJMVG9QYXRoKGltcG9ydC5tZXRhLnVybCkpXG5cbi8vIE1vcmUgaW5mbyBhdDogaHR0cHM6Ly9zdG9yeWJvb2suanMub3JnL2RvY3MvbmV4dC93cml0aW5nLXRlc3RzL2ludGVncmF0aW9ucy92aXRlc3QtYWRkb25cbmNvbnN0IGlzU3Rvcnlib29rID0gcHJvY2Vzcy5lbnYuU1RPUllCT09LID09PSAndHJ1ZSdcblxuY29uc3Qgdml0ZUluc3BlY3RDb21wYXRQYXRjaCA9IHtcbiAgbmFtZTogJ3ZpdGUtcGx1Z2luLWluc3BlY3QtY29tcGF0LXBhdGNoJyxcbiAgZW5mb3JjZTogJ3ByZScsXG4gIGNvbmZpZ3VyZVNlcnZlcihzZXJ2ZXIpIHtcbiAgICBpZiAoc2VydmVyICYmIHNlcnZlci5lbnZpcm9ubWVudHMgPT0gbnVsbCkge1xuICAgICAgLy8gVml0ZSA3IHJlbW92ZWQgdGhlIGBzZXJ2ZXIuZW52aXJvbm1lbnRzYCBwcm9wZXJ0eSB0aGF0XG4gICAgICAvLyBgdml0ZS1wbHVnaW4taW5zcGVjdGAgZXhwZWN0cy4gVGhlIHBsdWdpbiBpcyBidW5kbGVkIHdpdGhcbiAgICAgIC8vIGB2aXRlLXBsdWdpbi12dWUtZGV2dG9vbHNgIGFuZCBjcmFzaGVzIHdoZW4gaXQgdHJpZXMgdG8gYWNjZXNzXG4gICAgICAvLyB0aGUgbWlzc2luZyBwcm9wZXJ0eS4gUHJvdmlkaW5nIGFuIGVtcHR5IG9iamVjdCBrZWVwcyB0aGVcbiAgICAgIC8vIHBsdWdpbiBvcGVyYXRpb25hbCB3aXRob3V0IGFsdGVyaW5nIGFueSBiZWhhdmlvdXIuXG4gICAgICBzZXJ2ZXIuZW52aXJvbm1lbnRzID0ge31cbiAgICB9XG4gIH0sXG59XG5cbmNvbnN0IGVuYWJsZVZ1ZURldlRvb2xzID0gcHJvY2Vzcy5lbnYuRU5BQkxFX1ZVRV9ERVZUT09MUyA9PT0gJ3RydWUnXG5cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyhhc3luYyAoKSA9PiB7XG4gIGNvbnN0IHBsdWdpbnMgPSBbdnVlKCldXG4gIGlmICghaXNTdG9yeWJvb2sgJiYgZW5hYmxlVnVlRGV2VG9vbHMpIHtcbiAgICBwbHVnaW5zLnVuc2hpZnQodml0ZUluc3BlY3RDb21wYXRQYXRjaClcbiAgICBwbHVnaW5zLnB1c2godnVlRGV2VG9vbHMoKSlcbiAgfVxuXG4gIGxldCB0ZXN0Q29uZmlnXG4gIGlmIChpc1N0b3J5Ym9vaykge1xuICAgIGNvbnN0IHsgc3Rvcnlib29rVGVzdCB9ID0gYXdhaXQgaW1wb3J0KCdAc3Rvcnlib29rL2FkZG9uLXZpdGVzdC92aXRlc3QtcGx1Z2luJylcbiAgICB0ZXN0Q29uZmlnID0ge1xuICAgICAgcHJvamVjdHM6IFtcbiAgICAgICAge1xuICAgICAgICAgIGV4dGVuZHM6IHRydWUsXG4gICAgICAgICAgcGx1Z2luczogW1xuICAgICAgICAgICAgc3Rvcnlib29rVGVzdCh7XG4gICAgICAgICAgICAgIGNvbmZpZ0RpcjogcGF0aC5qb2luKGRpcm5hbWUsICcuc3Rvcnlib29rJyksXG4gICAgICAgICAgICB9KSxcbiAgICAgICAgICBdLFxuICAgICAgICAgIHRlc3Q6IHtcbiAgICAgICAgICAgIG5hbWU6ICdzdG9yeWJvb2snLFxuICAgICAgICAgICAgYnJvd3Nlcjoge1xuICAgICAgICAgICAgICBlbmFibGVkOiB0cnVlLFxuICAgICAgICAgICAgICBoZWFkbGVzczogdHJ1ZSxcbiAgICAgICAgICAgICAgcHJvdmlkZXI6ICdwbGF5d3JpZ2h0JyxcbiAgICAgICAgICAgICAgaW5zdGFuY2VzOiBbXG4gICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgYnJvd3NlcjogJ2Nocm9taXVtJyxcbiAgICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICBdLFxuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIHNldHVwRmlsZXM6IFsnLnN0b3J5Ym9vay92aXRlc3Quc2V0dXAuanMnXSxcbiAgICAgICAgICB9LFxuICAgICAgICB9LFxuICAgICAgXSxcbiAgICB9XG4gIH1cblxuICByZXR1cm4ge1xuICAgIHBsdWdpbnMsXG4gICAgcmVzb2x2ZToge1xuICAgICAgYWxpYXM6IHtcbiAgICAgICAgJ0AnOiBmaWxlVVJMVG9QYXRoKG5ldyBVUkwoJy4vc3JjJywgaW1wb3J0Lm1ldGEudXJsKSksXG4gICAgICB9LFxuICAgIH0sXG4gICAgc2VydmVyOiB7XG4gICAgLy8gXHU1NkZBXHU1QjlBXHU3QUVGXHU1M0UzXHVGRjBDXHU5MDdGXHU1MTREIEdvb2dsZSBNYXBzIEFQSSBcdTk2NTBcdTUyMzZcdTk1RUVcdTk4OThcbiAgICBwb3J0OiA1MTc0LFxuICAgIHN0cmljdFBvcnQ6IHRydWUsXG4gICAgLy8gXHU1OTgyXHU2NzlDXHU3QUVGXHU1M0UzXHU4OEFCXHU1MzYwXHU3NTI4XHU1MjE5XHU2MkE1XHU5NTE5XHVGRjBDXHU4MDBDXHU0RTBEXHU2NjJGXHU1QzFEXHU4QkQ1XHU0RTBCXHU0RTAwXHU0RTJBXHU3QUVGXHU1M0UzXG4gICAgaG9zdDogdHJ1ZSxcbiAgICAvLyBcdTc2RDFcdTU0MkNcdTYyNDBcdTY3MDlcdTU3MzBcdTU3NDBcblxuICAgIC8vIFx1NTE0MVx1OEJCOFx1OTAxQVx1OEZDNyBuZ3JvayBcdThCQkZcdTk1RUVcdUZGMDhcdTg5RTNcdTUxQjMgNDAzIEZvcmJpZGRlbiAvIEhvc3QgXHU2ODIxXHU5QThDXHVGRjA5XG4gICAgLy8gXHU0RTVGXHU1M0VGXHU4QkJFXHU3RjZFXHU0RTNBIHRydWUgXHU1QjhDXHU1MTY4XHU2NTNFXHU1RjAwXHVGRjA4XHU0RUM1XHU1RjAwXHU1M0QxXHU3M0FGXHU1ODgzXHU0RjdGXHU3NTI4XHVGRjA5XHVGRjFBXG4gICAgLy8gYWxsb3dlZEhvc3RzOiB0cnVlLFxuICAgIGFsbG93ZWRIb3N0czogWycubmdyb2stZnJlZS5hcHAnXSxcbiAgICAvLyBcdTUzRUZcdTkwMDlcdUZGMUFcdTgyRTVcdTk3MDBcdTg5ODFcdTdBMzNcdTVCOUEgSE1SXHVGRjBDXHU5MDFBXHU4RkM3IG5ncm9rIFx1NzY4NCB3c3MgXHU4RkRFXHU2M0E1XHVGRjA4XHU2RjE0XHU3OTNBXHU1M0VGXHU0RTBEXHU5MTREXHU3RjZFXHVGRjA5XG4gICAgLy8gaG1yOiB7XG4gICAgLy8gICBob3N0OiAnWU9VUl9TVUJET01BSU4ubmdyb2stZnJlZS5hcHAnLCAvLyBcdTY2RkZcdTYzNjJcdTRFM0FcdTVCOUVcdTk2NDUgbmdyb2sgXHU1QjUwXHU1N0RGXHU1NDBEXG4gICAgLy8gICBwcm90b2NvbDogJ3dzcycsXG4gICAgLy8gICBjbGllbnRQb3J0OiA0NDMsXG4gICAgLy8gfSxcblxuICAgIHByb3h5OiB7XG4gICAgICAnL2FwaSc6IHtcbiAgICAgICAgLy8gXHU2NzJDXHU1NzMwXHU1NDBFXHU3QUVGXHVGRjA4XHU5MDFBXHU4RkM3IFZpdGUgXHU0RUUzXHU3NDA2XHU4RjZDXHU1M0QxXHVGRjA5XHVGRjBDXHU2NkY0XHU3QTMzXHVGRjFBXHU3RURGXHU0RTAwXHU2MzA3XHU1NDExIGxvY2FsaG9zdFxuICAgICAgICB0YXJnZXQ6ICdodHRwOi8vbG9jYWxob3N0OjgwMDAnLFxuICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWUsXG4gICAgICAgIHNlY3VyZTogZmFsc2UsXG4gICAgICB9LFxuICAgIH0sXG4gICAgfSxcbiAgICAvLyBcdTRFQzVcdTU3MjggU3Rvcnlib29rIFx1NzNBRlx1NTg4M1x1NEUwQlx1NTJBMFx1OEY3RFx1NkQ0Qlx1OEJENVx1OTE0RFx1N0Y2RVxuICAgIHRlc3Q6IHRlc3RDb25maWcsXG4gIH1cbn0pXG4iXSwKICAibWFwcGluZ3MiOiAiO0FBQ0EsU0FBUyxlQUFlLFdBQVc7QUFDbkMsU0FBUyxvQkFBb0I7QUFDN0IsT0FBTyxTQUFTO0FBQ2hCLE9BQU8saUJBQWlCO0FBR3hCLE9BQU8sVUFBVTtBQVBqQixJQUFNLG1DQUFtQztBQUEySixJQUFNLDJDQUEyQztBQVFyUCxJQUFNLFVBQ0osT0FBTyxxQ0FBYyxjQUFjLG1DQUFZLEtBQUssUUFBUSxjQUFjLHdDQUFlLENBQUM7QUFHNUYsSUFBTSxjQUFjLFFBQVEsSUFBSSxjQUFjO0FBRTlDLElBQU0seUJBQXlCO0FBQUEsRUFDN0IsTUFBTTtBQUFBLEVBQ04sU0FBUztBQUFBLEVBQ1QsZ0JBQWdCLFFBQVE7QUFDdEIsUUFBSSxVQUFVLE9BQU8sZ0JBQWdCLE1BQU07QUFNekMsYUFBTyxlQUFlLENBQUM7QUFBQSxJQUN6QjtBQUFBLEVBQ0Y7QUFDRjtBQUVBLElBQU0sb0JBQW9CLFFBQVEsSUFBSSx3QkFBd0I7QUFFOUQsSUFBTyxzQkFBUSxhQUFhLFlBQVk7QUFDdEMsUUFBTSxVQUFVLENBQUMsSUFBSSxDQUFDO0FBQ3RCLE1BQUksQ0FBQyxlQUFlLG1CQUFtQjtBQUNyQyxZQUFRLFFBQVEsc0JBQXNCO0FBQ3RDLFlBQVEsS0FBSyxZQUFZLENBQUM7QUFBQSxFQUM1QjtBQUVBLE1BQUk7QUFDSixNQUFJLGFBQWE7QUFDZixVQUFNLEVBQUUsY0FBYyxJQUFJLE1BQU0sT0FBTyx1Q0FBdUM7QUFDOUUsaUJBQWE7QUFBQSxNQUNYLFVBQVU7QUFBQSxRQUNSO0FBQUEsVUFDRSxTQUFTO0FBQUEsVUFDVCxTQUFTO0FBQUEsWUFDUCxjQUFjO0FBQUEsY0FDWixXQUFXLEtBQUssS0FBSyxTQUFTLFlBQVk7QUFBQSxZQUM1QyxDQUFDO0FBQUEsVUFDSDtBQUFBLFVBQ0EsTUFBTTtBQUFBLFlBQ0osTUFBTTtBQUFBLFlBQ04sU0FBUztBQUFBLGNBQ1AsU0FBUztBQUFBLGNBQ1QsVUFBVTtBQUFBLGNBQ1YsVUFBVTtBQUFBLGNBQ1YsV0FBVztBQUFBLGdCQUNUO0FBQUEsa0JBQ0UsU0FBUztBQUFBLGdCQUNYO0FBQUEsY0FDRjtBQUFBLFlBQ0Y7QUFBQSxZQUNBLFlBQVksQ0FBQyw0QkFBNEI7QUFBQSxVQUMzQztBQUFBLFFBQ0Y7QUFBQSxNQUNGO0FBQUEsSUFDRjtBQUFBLEVBQ0Y7QUFFQSxTQUFPO0FBQUEsSUFDTDtBQUFBLElBQ0EsU0FBUztBQUFBLE1BQ1AsT0FBTztBQUFBLFFBQ0wsS0FBSyxjQUFjLElBQUksSUFBSSxTQUFTLHdDQUFlLENBQUM7QUFBQSxNQUN0RDtBQUFBLElBQ0Y7QUFBQSxJQUNBLFFBQVE7QUFBQTtBQUFBLE1BRVIsTUFBTTtBQUFBLE1BQ04sWUFBWTtBQUFBO0FBQUEsTUFFWixNQUFNO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQSxNQU1OLGNBQWMsQ0FBQyxpQkFBaUI7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQSxNQVFoQyxPQUFPO0FBQUEsUUFDTCxRQUFRO0FBQUE7QUFBQSxVQUVOLFFBQVE7QUFBQSxVQUNSLGNBQWM7QUFBQSxVQUNkLFFBQVE7QUFBQSxRQUNWO0FBQUEsTUFDRjtBQUFBLElBQ0E7QUFBQTtBQUFBLElBRUEsTUFBTTtBQUFBLEVBQ1I7QUFDRixDQUFDOyIsCiAgIm5hbWVzIjogW10KfQo=
